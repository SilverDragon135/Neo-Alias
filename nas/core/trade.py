"""
Module Trade - alias trading implementation
"""
from boa.blockchain.vm.Neo.Runtime import Notify, CheckWitness
from boa.blockchain.vm.Neo.Action import RegisterAction
from boa.code.builtins import concat
from nas.core.util import call_sub_nas, get_header_timestamp
from nas.configuration.NeoAlias import NeoAliasConfiguration
from nas.common.Account import Account
from nas.core.fee_pool import FeesPool
from nas.common.Alias import Alias
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
        Notify("Not enough args provided. Requres prices.")
        return False
    elif nargs > 1:
        alias_type = args[1]
    else:
        alias_type = 0
    price = args[0]
    if price < 0:
        Notify("Price lower than 0.")
        return False
    alias_to_sell = Alias()
    alias_to_sell.name = alias
    alias_to_sell.atype = alias_type

    exists = alias_to_sell.exists()
    expired = False
    if exists:
        expired = alias_to_sell.expired()

    if not exists or expired:
        Notify("Alias not found or expired.")
        return False

    owner = alias_to_sell.owner() 
    if not CheckWitness(owner):
        Notify("This operation can invoke only alias owner.")
        return False

    buy_offer_expiration = alias_to_sell.buy_offer_expiration()
    alias_to_sell_buy_offer_price = alias_to_sell.buy_offer_price()
    if alias_to_sell_buy_offer_price >= price and get_header_timestamp() < buy_offer_expiration:
        # sell
        new_alias_owner = alias_to_sell.buy_offer_owner()
        new_alias_target = alias_to_sell.buy_offer_target()
        configuration = NeoAliasConfiguration()
        configured_commission = configuration.get_trade_commission()
        service_fee_part = (price * configured_commission) / 100
        alias_owner_part = price - service_fee_part

        seller_account = Account()
        seller_account.address = alias_to_sell.owner()
        seller_account.add_available_assets(alias_owner_part)
        fee_pool = FeesPool()
        fee_pool.add_fee_to_pool(service_fee_part)

        old_owner = alias_to_sell.owner()
        data = alias_to_sell.get_data()
        data[0] = new_alias_target
        data[1] = new_alias_owner
        data[4] = None
        data[5] = 0
        alias_to_sell.save_data(data)

        TradeSuccesfullEvent(alias, alias_type, old_owner, new_alias_owner, price)
        Notify("Sold.")
        return True
    
    data = alias_to_sell.get_data()
    data[8] = 1
    data[9] = price
    alias_to_sell.save_data(data)
    SellOfferEvent(alias, alias_type, price)
    Notify("Put on sale.")
    return True


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

    exists = alias_on_sale.exists()
    expired = False
    if exists:
        expired = alias_on_sale.expired()

    if not exists or expired:
        Notify("Alias not found or expired.")
        return False
    owner = alias_on_sale.owner()
    if not CheckWitness(owner):
        Notify("This operation can invoke only alias owner.")
        return False

    data = alias_on_sale.get_data()
    data[8] = 0
    data[9] = 0
    alias_on_sale.save_data(data)
    CancelSellOfferEvent(alias, alias_type)
    Notify("Sale offer canceled.")
    return True


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
    
    exists = alias_to_buy.exists()
    expired = alias_to_buy.expired()

    if not exists or expired:
        Notify("Alias not found int database.")
        return False
    
    if not CheckWitness(buy_offer_owner):
        Notify("You can offer buy only for yourself.")
        return False

    owner = alias_to_buy.owner()
    if owner == buy_offer_owner:
        Notify("You already own this alias.")
        return False

    timestamp = get_header_timestamp()
    if buy_offer_expiration < timestamp:
        Notify("Cannot put expired offer.")
        return False

    buyer_account = Account()
    buyer_account.address = buy_offer_owner
    # check if enough assets for offer
    offerer_available_assets = buyer_account.available_assets()
    offerer_available_assets += gas_attached()
    if offerer_available_assets < buy_offer_price:
        Notify("Not enough assets provided.")
        return False

    other_buy_offer_expiration = alias_to_buy.buy_offer_expiration()
    alias_to_buy_buy_offer_price = alias_to_buy.buy_offer_price()
    if alias_to_buy_buy_offer_price > buy_offer_price and other_buy_offer_expiration > timestamp:
        Notify("There is higher offer.")
        return False
    else:
        # refund assets to stored_buy_offer_owner
        old_buyer_acc = Account()
        old_buyer_acc.address = alias_to_buy.buy_offer_owner()
        old_buyer_acc.add_available_assets(alias_to_buy_buy_offer_price)

    is_for_sale = alias_to_buy.is_for_sale()
    sell_offer_price = alias_to_buy.sell_offer_price()

    if is_for_sale and sell_offer_price <= buy_offer_price:
        # perform trade
        buyer_account.sub_available_assets(sell_offer_price)
        configuration = NeoAliasConfiguration()
        configured_commission = configuration.get_trade_commission()
        service_fee_part = (sell_offer_price * configured_commission) / 100
        alias_owner_part = sell_offer_price - service_fee_part

        alias_owner_acc = Account()
        alias_owner_acc.address = alias_to_buy.owner()
        alias_owner_acc.add_available_assets(alias_owner_part)
        fee_pool = FeesPool()
        fee_pool.add_fee_to_pool(service_fee_part)
        old_owner = alias_to_buy.owner()
        data = alias_to_buy.get_data()
        data[0] = buy_offer_target
        data[1] = buy_offer_owner
        data[4] = 0
        data[5] = 0
        alias_to_buy.save_data(data)

        TradeSuccesfullEvent(alias, alias_type, old_owner, buy_offer_owner, buy_offer_price)
        Notify("Sold.")
        return True
    
    data = alias_to_buy.get_data()
    data[4] = buy_offer_owner
    data[5] = buy_offer_price
    data[6] = buy_offer_expiration
    data[7] = buy_offer_target
    alias_to_buy.save_data(data)

    BuyOfferEvent(alias, alias_type, buy_offer_owner, buy_offer_price)
    Notify("Buy offer submitted.")
    return True


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

    exists = alias_with_buy_offer.exists()
    expired = alias_with_buy_offer.expired()

    if not exists or expired:
        Notify("Alias not found or expired.")
        return False
    buy_offer_owner = alias_with_buy_offer.buy_offer_owner()
    if not CheckWitness(buy_offer_owner):
        Notify("This operation can invoke only buy offer owner.")
        return False

    # refund
    buyer_acc = Account()
    buyer_acc.address = alias_with_buy_offer.buy_offer_owner()
    assets = alias_with_buy_offer.buy_offer_price()
    buyer_acc.add_available_assets(assets)

    data = alias_with_buy_offer.get_data()
    data[4] = 0
    data[5] = 0
    data[6] = 0
    alias_with_buy_offer.save_data(data)

    CancelBuyOfferEvent(alias, alias_type, buy_offer_owner)
    Notify("Buy offer canceled.")
    return True
