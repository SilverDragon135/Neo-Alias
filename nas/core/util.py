"""
Modul util - contains derived methods for calculation
"""

from boa.blockchain.vm.Neo.App import DynamicAppCall
from boa.blockchain.vm.Neo.Runtime import Notify
from boa.builtins import list
from nas.core.na_fee_pool import FeesPool
from nas.configuration.Service import ServiceConfiguration
from nas.common.Account import Account
from nas.common.util import get_header_timestamp, return_value
from nas.common.Alias import Alias,init_alias, load_alias

from boa.builtins import concat

def call_remote_smart_contract(alias_info, operation, args):
    """
    :param alias_info:
    :param operation:
    \n:param args []:
    \n:returns True if success or False if failed:
    \ntryes to resolve alias_info and pass call to resolved smartcontract
    \nin case of sub_nas support alias_info is array [alias, sub_nas]
    """
    
    sc = nas_gateway.handle_service_call("na_query",query_args)
                
    if sc:
        return DynamicAppCall(sc, operation, args)
    else:
        Notify("SC call failed. Possible reasons: no exists or expired, not in provided NA.")
        return False


    if nargs >= 1:
        alias = args[0]
        sub_nas = None

    if configuration.support_sub_nas_call:
        if len(alias) > 1:
            sub_nas = alias[1]
        elif len(alias) == 0:
            Notify("Alias name not provided.")
            return False
        alias_name = alias[0]
    else:
        alias_name = alias

    if not alias_name:
        Notify("Alias name not provided.")
        return False
    args = list_slice(args,1,nargs)
    sc = alias
    #sc = na_query(alias_name, sub_nas, args)
    if sc:
        return DynamicAppCall(sc, operation, args)
    else:
        Notify("SC call failed. Possible reasons: no exists or expired, not in provided NA.")
        return False

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

    if available_assets >= to_pay:
        # update account assets
        account.sub_available_assets(to_pay)
    else:
        return False

    fee_pool = FeesPool()
    fee_pool.add_fee_to_pool(to_pay)
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
