"""
Module Trade - alias trading implementation
"""
from boa.blockchain.vm.Neo.Runtime import Notify, CheckWitness
from boa.blockchain.vm.Neo.Action import RegisterAction
from boa.code.builtins import concat
from nas.core.util import call_sub_nas, get_header_timestamp
from nas.configuration.Service import ServiceConfiguration
from nas.common.Account import Account
from nas.core.na_fee_pool import FeesPool
from nas.common.Alias import Alias, load_alias
from nas.common.util import return_value
from nas.wrappers.tx_info import gas_attached

SellOfferEvent = RegisterAction('putOnSale', 'alias_name', 'alias_type', 'price')
CancelSellOfferEvent = RegisterAction('cancelOnSale', 'alias_name', 'alias_type')
BuyOfferEvent = RegisterAction('buyOffer', 'alias_name', 'alias_type', 'offer_owner', 'price')
CancelBuyOfferEvent = RegisterAction('cancelBuyOffer', 'alias_name', 'alias_type', 'offer_owner')

TradeSuccesfullEvent = RegisterAction('trade', 'alias_name', 'alias_type', 'old_owne', 'new_owner', 'price')


def offer_sell(alias, sub_nas, args):
    """
    :param alias:
    :param sub_nas:
    \n:param args [price, type]:
    \n:returns True if success or False if failed:
    \nif sub_nas defined passes call to sub_nas otherwise
    we try to put alias on sale
    """
    nargs = len(args)
    if sub_nas:
        return call_sub_nas(sub_nas, "offer_sell", args)
    elif nargs < 1:
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
    alias_to_sell = Alias()
    alias_to_sell.name = alias
    alias_to_sell.atype = alias_type

    if not alias_to_sell.exists():
        msg = concat("Alias not found: ", alias)
        Notify(msg)
        return return_value(False, msg)

    alias_to_sell = load_alias(alias_to_sell)

    if alias_to_sell.expired():
        msg = concat("Alias expired: ", alias)
        Notify(msg)
        return return_value(False, msg)

    if not CheckWitness(alias_to_sell.owner):
        msg = "This operation can invoke only alias owner."
        Notify(msg)
        return return_value(False, msg)

    buy_offer_expiration = alias_to_sell.buy_offer_expiration
    alias_to_sell_buy_offer_price = alias_to_sell.buy_offer_price
    if alias_to_sell_buy_offer_price >= price and get_header_timestamp() < buy_offer_expiration:
        # sell
        new_alias_owner = alias_to_sell.buy_offer_owner
        new_alias_target = alias_to_sell.buy_offer_target
        configuration = ServiceConfiguration()
        configured_commission = configuration.get_trade_commission()
        service_fee_part = (price * configured_commission) / 100
        alias_owner_part = price - service_fee_part

        seller_account = Account()
        seller_account.address = alias_to_sell.owner
        seller_account.add_available_assets(alias_owner_part)
        fee_pool = FeesPool()
        fee_pool.add_fee_to_pool(service_fee_part)

        old_owner = alias_to_sell.owner

        alias_to_sell.target = new_alias_target
        alias_to_sell.owner = new_alias_owner
        alias_to_sell.buy_offer_owner = b''
        alias_to_sell.buy_offer_price = 0
        alias_to_sell.buy_offer_expiration = 0
        alias_to_sell.save()

        TradeSuccesfullEvent(alias, alias_type, old_owner, new_alias_owner, price)
        msg = "Sold."
        Notify(msg)
        return return_value(True, msg)

    alias_to_sell.for_sale = 1
    alias_to_sell.sell_offer_price = price
    alias_to_sell.save()
    SellOfferEvent(alias, alias_type, price)
    msg = "Put on sale."
    Notify(msg)
    return return_value(True, msg)


def cancel_sale_offer(alias, sub_nas, args):
    """
    :param alias:
    :param sub_nas:
    \n:param args [type]:
    \n:returns True if success or False if failed:
    \nif sub_nas defined passes call to sub_nas otherwise
    we try to cancel alias on sale
    """
    nargs = len(args)
    if sub_nas:
        return call_sub_nas(sub_nas, "cancel_sale_offer", args)
    elif nargs > 0:
        alias_type = args[0]
    else:
        alias_type = 0
    alias_on_sale = Alias()
    alias_on_sale.name = alias
    alias_on_sale.atype = alias_type

    if not alias_on_sale.exists():
        msg = concat("Alias not found: ", alias)
        Notify(msg)
        return return_value(False, msg)

    alias_on_sale = load_alias(alias_on_sale)

    if alias_on_sale.expired():
        msg = concat("Alias expired: ", alias)
        Notify(msg)
        return return_value(False, msg)

    if not CheckWitness(alias_on_sale.owner):
        msg = "This operation can invoke only alias owner."
        Notify(msg)
        return return_value(False, msg)

    alias_on_sale.for_sale = 0
    alias_on_sale.sell_offer_price = 0
    alias_on_sale.save()
    CancelSellOfferEvent(alias, alias_type)
    msg = "Sale offer canceled."
    Notify(msg)
    return return_value(True, msg)


def offer_buy(alias, sub_nas, args):
    """
    :param alias:
    :param sub_nas:
    \n:param args [owner, target, price, expiration]:
    \n:returns True if success or False if failed:
    \nif sub_nas defined passes call to sub_nas otherwise
    we try to place buy offer for alias
    """
    nargs = len(args)
    if sub_nas:
        return call_sub_nas(sub_nas, "offer_buy", args)
    elif nargs < 4:
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

    alias_to_buy = Alias()
    alias_to_buy.name = alias
    alias_to_buy.atype = alias_type

    if not alias_to_buy.exists():
        msg = concat("Alias not found: ", alias)
        Notify(msg)
        return return_value(False, msg)

    alias_to_buy = load_alias(alias_to_buy)

    if alias_to_buy.expired():
        msg = concat("Alias expired: ", alias)
        Notify(msg)
        return return_value(False, msg)

    if not CheckWitness(buy_offer_owner):
        msg = "You can offer buy only for yourself."
        Notify(msg)
        return return_value(False, msg)

    if alias_to_buy.buy_offer_owner == alias_to_buy.owner:
        msg = "You already own this alias."
        Notify(msg)
        return return_value(False, msg)

    timestamp = get_header_timestamp()
    if buy_offer_expiration < timestamp:
        msg = "Cannot put expired offer."
        Notify(msg)
        return return_value(False, msg)

    buyer_account = Account()
    buyer_account.address = buy_offer_owner
    # check if enough assets for offer
    offerer_available_assets = buyer_account.available_assets()
    offerer_available_assets += gas_attached()
    if offerer_available_assets < buy_offer_price:
        msg = "Not enough assets provided."
        Notify(msg)
        return return_value(False, msg)

    other_buy_offer_expiration = alias_to_buy.buy_offer_expiration
    alias_to_buy_buy_offer_price = alias_to_buy.buy_offer_price
    if alias_to_buy_buy_offer_price > buy_offer_price and other_buy_offer_expiration > timestamp:
        msg = "There is higher offer."
        Notify(msg)
        return return_value(False, msg)
    else:
        # refund assets to stored_buy_offer_owner
        old_buyer_acc = Account()
        old_buyer_acc.address = alias_to_buy.buy_offer_owner
        old_buyer_acc.add_available_assets(alias_to_buy_buy_offer_price)

    for_sale = alias_to_buy.for_sale
    sell_offer_price = alias_to_buy.sell_offer_price

    if for_sale and sell_offer_price <= buy_offer_price:
        # perform trade
        buyer_account.sub_available_assets(sell_offer_price)
        configuration = ServiceConfiguration()
        configured_commission = configuration.get_trade_commission()
        service_fee_part = (sell_offer_price * configured_commission) / 100
        alias_owner_part = sell_offer_price - service_fee_part

        alias_owner_acc = Account()
        alias_owner_acc.address = alias_to_buy.owner
        alias_owner_acc.add_available_assets(alias_owner_part)
        fee_pool = FeesPool()
        fee_pool.add_fee_to_pool(service_fee_part)
        old_owner = alias_to_buy.owner

        alias_to_buy.target = buy_offer_target
        alias_to_buy.owner = buy_offer_owner
        alias_to_buy.for_sale = 0
        alias_to_buy.sell_offer_price = 0
        alias_to_buy.save()

        TradeSuccesfullEvent(alias, alias_type, old_owner, buy_offer_owner, buy_offer_price)
        msg = "Sold."
        Notify(msg)
        return return_value(True, msg)

    alias_to_buy.buy_offer_target = buy_offer_target
    alias_to_buy.buy_offer_owner = buy_offer_owner
    alias_to_buy.buy_offer_price = buy_offer_price
    alias_to_buy.buy_offer_expiration = buy_offer_expiration

    alias_to_buy.save()

    BuyOfferEvent(alias, alias_type, buy_offer_owner, buy_offer_price)
    msg = "Buy offer submitted."
    Notify(msg)
    return return_value(True, msg)


def cancel_buy_offer(alias, sub_nas, args):
    """
    :param alias:
    :param sub_nas:
    \n:param args [type]:
    \n:returns True if success or False if failed:
    \nif sub_nas defined passes call to sub_nas otherwise
    we try to cancel buy offer
    """
    nargs = len(args)
    if sub_nas:
        return call_sub_nas(sub_nas, "cancel_sale_offer", args)
    elif nargs > 0:
        alias_type = args[0]
    else:
        alias_type = 0
    alias_with_buy_offer = Alias()
    alias_with_buy_offer.name = alias
    alias_with_buy_offer.atype = alias_type

    if not alias_with_buy_offer.exists():
        msg = concat("Alias not found: ", alias)
        Notify(msg)
        return return_value(False, msg)

    alias_with_buy_offer = load_alias(alias_with_buy_offer)

    if alias_with_buy_offer.expired():
        msg = concat("Alias expired: ", alias)
        Notify(msg)
        return return_value(False, msg)

    if not CheckWitness(alias_with_buy_offer.buy_offer_owner):
        msg = "This operation can invoke only buy offer owner."
        Notify(msg)
        return return_value(False, msg)

    # refund
    buyer_acc = Account()
    buyer_acc.address = alias_with_buy_offer.buy_offer_owner
    assets = alias_with_buy_offer.buy_offer_price
    buyer_acc.add_available_assets(assets)

    alias_with_buy_offer.buy_offer_owner = b''
    alias_with_buy_offer.buy_offer_price = 0
    alias_with_buy_offer.expiration = 0
    alias_with_buy_offer.save()

    CancelBuyOfferEvent(alias, alias_type, alias_with_buy_offer.buy_offer_owner)
    msg = "Buy offer canceled."
    Notify(msg)
    return return_value(True, msg)
