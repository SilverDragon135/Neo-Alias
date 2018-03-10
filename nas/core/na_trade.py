"""
Module Trade - alias trading implementation
"""
from boa.interop.Neo.Runtime import Notify, CheckWitness
from boa.interop.Neo.Action import RegisterAction
from boa.builtins import concat
from nas.config.service import *
from nas.common.fee_pool import add_fee_to_pool, get_collected_fees
from nas.common.alias import *
from nas.common.util import return_value, get_header_timestamp

SellOfferEvent = RegisterAction('putOnSale', 'alias_name', 'alias_type', 'price')
CancelSellOfferEvent = RegisterAction('cancelOnSale', 'alias_name', 'alias_type')
BuyOfferEvent = RegisterAction('buyOffer', 'alias_name', 'alias_type', 'offer_owner', 'price')
CancelBuyOfferEvent = RegisterAction('cancelBuyOffer', 'alias_name', 'alias_type', 'offer_owner')

TradeSuccesfullEvent = RegisterAction('trade', 'alias_name', 'alias_type', 'old_owne', 'new_owner', 'price')



def offer_sell(alias, args):
    """
    :param alias:
    \n:param args [price, type]:
    \n:returns True if success or False if failed:
    """
    nargs = len(args)
    if nargs < 1:
        msg = "Not enough args provided. Requres prices."
        Notify(msg)
        return msg
    elif nargs > 1:
        alias_type = args[1]
    else:
        alias_type = 0
    price = args[0]
    if price < 0:
        msg = "Price lower than 0."
        Notify(msg)
        return msg

    alias_to_sell = init_alias(alias,alias_type)

    if not alias_exists(alias_to_sell):
        msg = concat("Alias not found: ", alias)
        Notify(msg)
        return return_value(False, msg)

    alias_to_sell = alias_load(alias_to_sell)

    if alias_expired(alias_to_sell):
        msg = concat("Alias expired: ", alias)
        Notify(msg)
        return return_value(False, msg)

    alias_owner = alias_get_owner(alias_to_sell)
    if not CheckWitness(alias_owner):
        msg = "This operation can invoke only alias owner."
        Notify(msg)
        return return_value(False, msg)

    timestamp = get_header_timestamp()
    buy_offer_expiration = alias_get_buy_offer_expiration(alias_to_sell)
    alias_to_sell_buy_offer_price = alias_get_buy_offer_price(alias_to_sell)
    if alias_to_sell_buy_offer_price >= price and timestamp < buy_offer_expiration:
        # sell
        new_alias_owner = alias_get_buy_offer_owner(alias_to_sell)
        new_alias_target = alias_get_buy_offer_target(alias_to_sell)
        
        configured_commission =get_trade_commission()
        service_fee_part = (price * configured_commission) / 100
        alias_owner_part = price - service_fee_part

        add_account_available_assets(alias_owner,alias_owner_part)

        add_fee_to_pool(service_fee_part)

        alias_set_target(alias_to_sell, new_alias_target)
        alias_set_owner(alias_to_sell, new_alias_owner)
        alias_set_owner_since(alias_to_sell, timestamp)

        alias_set_buy_offer_owner(alias_to_sell, b'')
        alias_set_buy_offer_price(alias_to_sell,0)
        alias_set_buy_offer_expiration(alias_to_sell,0)

        alias_save(alias_to_sell)

        TradeSuccesfullEvent(alias, alias_type, alias_owner, new_alias_owner, price)
        msg = "Sold."
        Notify(msg)
        return return_value(True, msg)

    alias_set_for_sale(alias_to_sell, 1)
    alias_set_sell_offer_price(alias_to_sell, price)

    alias_save(alias_to_sell)
    SellOfferEvent(alias, alias_type, price)
    msg = "Put on sale."
    Notify(msg)
    return return_value(True, msg)


def cancel_sale_offer(alias, args):
    """
    :param alias:
    \n:param args [type]:
    \n:returns True if success or False if failed:
    """
    if len(args) > 0:
        alias_type = args[0]
    else:
        alias_type = 0

    alias_on_sale = init_alias(alias,alias_type)

    if not alias_exists(alias_on_sale):
        msg = concat("Alias not found: ", alias)
        Notify(msg)
        return return_value(False, msg)

    alias_on_sale = alias_load(alias_on_sale)

    if alias_expired(alias_on_sale):
        msg = concat("Alias expired: ", alias)
        Notify(msg)
        return return_value(False, msg)

    owner = alias_get_owner(alias_on_sale)
    if not CheckWitness(owner):
        msg = "This operation can invoke only alias owner."
        Notify(msg)
        return return_value(False, msg)

    alias_set_for_sale(alias_on_sale, 0)
    alias_set_sell_offer_price(alias_on_sale, 0)

    alias_save(alias_on_sale)
    CancelSellOfferEvent(alias, alias_type)
    msg = "Sale offer canceled."
    Notify(msg)
    return return_value(True, msg)


def offer_buy(alias, args):
    """
    :param alias:
    \n:param args [owner, target, price, expiration]:
    \n:returns True if success or False if failed:
    """
    nargs = len(args)
    if nargs < 4:
        Notify("Not enough args provided. Requres buy_offer_owner,buy_offer_target,buy_offer_price, buy_offer_expiration.")
        return False
    elif nargs > 4:
        alias_type = args[4]
    else:
        alias_type = 0
    buy_offer_owner = args[0]
    buy_offer_target = args[1]
    buy_offer_price = args[2]
    buy_offer_expiration = args[3]

    alias_to_buy = init_alias(alias,alias_type)

    if not alias_exists(alias_to_buy):
        msg = concat("Alias not found: ", alias)
        Notify(msg)
        return return_value(False, msg)

    alias_to_buy = alias_load(alias_to_buy)

    if alias_expired(alias_to_buy):
        msg = concat("Alias expired: ", alias)
        Notify(msg)
        return return_value(False, msg)

    if not CheckWitness(buy_offer_owner):
        msg = "You can offer buy only for yourself."
        Notify(msg)
        return return_value(False, msg)

    alias_owner = alias_get_owner(alias_to_buy)
    if buy_offer_owner == alias_owner:
        msg = "You already own this alias."
        Notify(msg)
        return return_value(False, msg)

    timestamp = get_header_timestamp()
    if buy_offer_expiration < timestamp:
        msg = "Cannot put expired offer."
        Notify(msg)
        return return_value(False, msg)

    # check if enough assets for offer
    offerer_available_assets = available_account_assets(buy_offer_owner)

    if offerer_available_assets < buy_offer_price:
        msg = "Not enough assets provided."
        Notify(msg)
        return return_value(False, msg)

    other_buy_offer_expiration = alias_get_buy_offer_expiration(alias_to_buy)
    alias_to_buy_buy_offer_price = alias_get_buy_offer_price(alias_to_buy)

    if alias_to_buy_buy_offer_price > buy_offer_price and other_buy_offer_expiration > timestamp:
        msg = "There is higher offer."
        Notify(msg)
        return return_value(False, msg)
    else:
        # refund assets to stored_buy_offer_owner
        old_buy_offer_owner = alias_get_buy_offer_owner(alias_to_buy)
        add_account_available_assets(old_buy_offer_owner, alias_to_buy_buy_offer_price)

    for_sale = alias_get_for_sale(alias_to_buy)
    sell_offer_price = alias_get_sell_offer_price(alias_to_buy)

    if for_sale and sell_offer_price <= buy_offer_price:
        # perform trade
        sub_account_available_assets(buy_offer_owner, sell_offer_price)

        
        configured_commission =get_trade_commission()
        service_fee_part = (sell_offer_price * configured_commission) / 100
        alias_owner_part = sell_offer_price - service_fee_part

        old_owner = alias_get_owner(alias_to_buy)
        add_account_available_assets(old_owner, alias_owner_part)
        add_fee_to_pool(service_fee_part)

        alias_set_target(alias_to_buy, buy_offer_target)
        alias_set_owner(alias_to_buy, buy_offer_owner)
        alias_set_owner_since(alias_to_buy, timestamp)

        alias_set_for_sale(alias_to_buy, 0)
        alias_set_sell_offer_price(alias_to_buy,0)

        alias_save(alias_to_buy)

        TradeSuccesfullEvent(alias, alias_type, old_owner, buy_offer_owner, buy_offer_price)
        msg = "Sold."
        Notify(msg)
        return return_value(True, msg)

    alias_set_buy_offer_target(alias_to_buy, buy_offer_target)
    alias_set_buy_offer_owner(alias_to_buy, buy_offer_owner)
    alias_set_buy_offer_price(alias_to_buy,buy_offer_price)
    alias_set_buy_offer_expiration(alias_to_buy,buy_offer_expiration)

    alias_save(alias_to_buy)

    BuyOfferEvent(alias, alias_type, buy_offer_owner, buy_offer_price)
    msg = "Buy offer submitted."
    Notify(msg)
    return return_value(True, msg)


def cancel_buy_offer(alias, args):
    """
    :param alias:
    \n:param args [type]:
    \n:returns True if success or False if failed:
    """
    if len(args) > 0:
        alias_type = args[0]
    else:
        alias_type = 0
        
    alias_with_buy_offer = init_alias(alias,alias_type)

    if not alias_exists(alias_with_buy_offer):
        msg = concat("Alias not found: ", alias)
        Notify(msg)
        return return_value(False, msg)

    alias_with_buy_offer = alias_load(alias_with_buy_offer)

    owner = alias_get_owner(alias_with_buy_offer)
    if not CheckWitness(owner):
        msg = "This operation can invoke only buy offer owner."
        Notify(msg)
        return return_value(False, msg)

    # refund
    assets = alias_get_buy_offer_price(alias_with_buy_offer)
    add_account_available_assets(owner, assets)

    alias_set_buy_offer_owner(alias_with_buy_offer, b'')
    alias_set_buy_offer_price(alias_with_buy_offer, 0)
    alias_set_buy_offer_expiration(alias_with_buy_offer, 0)

    alias_save(alias_with_buy_offer)

    CancelBuyOfferEvent(alias, alias_type, owner)
    msg = "Buy offer canceled."
    Notify(msg)
    return return_value(True, msg)
