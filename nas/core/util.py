"""
Modul util - contains derived methods for calculation
"""

from boa.blockchain.vm.Neo.App import DynamicAppCall
from boa.blockchain.vm.Neo.Runtime import Notify
from boa.code.builtins import list
from nas.core.na_fee_pool import FeesPool
from nas.configuration.Service import ServiceConfiguration
from nas.common.Account import Account
from nas.wrappers.tx_info import gas_attached
from nas.common.util import get_header_timestamp, debug_message
from nas.common.Alias import Alias, load_alias

from boa.code.builtins import concat

def call_sub_nas(sub_nas, operation, args):
    """
    :param sub_nas:
    :param operation:
    \n:param args []:
    \n:returns True if success or False if failed:
    \ntryes to resolve sub_nas alias and pass call to resolved sub_nas
    """
    sub_nas_alias = Alias()
    sub_nas_alias.name = sub_nas
    sub_nas_alias.atype = 2

    if not sub_nas_alias.exists():
        msg = concat("Alias not found: ", sub_nas)
        Notify(msg)
        return debug_message(False,msg)
   
    sub_nas_alias = load_alias(sub_nas_alias)

    if sub_nas_alias.expired():
        msg = concat("Alias expired: ", sub_nas)
        Notify(msg)
        return debug_message(False,msg)

    # pass register call tu sub Neo alias service
    target = sub_nas_alias.target
    return DynamicAppCall(target, operation, args)

def try_pay_holding_fee(owner, alias_type, duration_to_pay):
    """
    :param owner:
    :param alias_type:
    :param duration_to_pay:
    \n:returns True if success or False if failed:
    \nchecks if owner provided enough assets to hold alias and if so 
    adds fee to fee pool
    """
    configuration = ServiceConfiguration()
    # get fee info
    fee = configuration.get_fee_per_period(alias_type)
    fee_period = configuration.get_fee_period()
    
    # calculate to pay * 100000000 to handle decimals
    periods_to_pay = (duration_to_pay * 100000000) / fee_period
    to_pay = (periods_to_pay * fee) / 100000000

    # check if enough assets
    account = Account()
    account.address = owner

    available_assets = account.available_assets()
    
    attached_assets = gas_attached()
    available_assets = available_assets + attached_assets

    if available_assets >= to_pay:
        assets_to_store = to_pay - available_assets
    else:
        return False

    fee_pool = FeesPool()
    fee_pool.add_fee_to_pool(to_pay)
    # update account assets
    account.update_available_assets(assets_to_store)
    return True


# not used - will be implemented with free aliases
def add_loyality_bonus_to_fee(alias_owner_since, alias_fee):
    """
    :param alias_owner_since:
    :param alias_fee:
    \n:returns fee multiplied with bonus:
    \nnot implemented
    """
    if not alias_fee:
        return 0
    loyality_bonus = 100000000
    configuration = ServiceConfiguration()
    maximum_loyality_bonus = configuration.get_maximum_loyalty_bonus()
    loyality_bonus_period = configuration.get_loyality_bonus_per_period()
    loyality_bonus_per_period = configuration.get_loyality_bonus_period()
    alias_under_owner_duration = alias_owner_since - get_header_timestamp()
    loyality_bonus = loyality_bonus + \
        ((alias_under_owner_duration / loyality_bonus_period)
            * loyality_bonus_per_period)
    if loyality_bonus > maximum_loyality_bonus:
        loyality_bonus = maximum_loyality_bonus
    return (alias_fee * loyality_bonus) / 100000000
