
from boa.interop.Neo.App import DynamicAppCall
from boa.interop.System.ExecutionEngine import GetExecutingScriptHash
from nas.core.na import *
from nas.core.na_trade import *
from nas.core.na_nep5 import *
from nas.common.token_info import TOKEN_NAME, TOKEN_SYMBOL, TOKEN_DECIMALS, TOKEN_TOTAL_SUPPLY
from nas.common.util import list_slice
# enables/disables sub_nas support
#SUPPORT_SUB_NAS = True

NA_METHODS = ['na_register', 'na_renew', 'na_update_target','na_transfer', 'na_delete', 'na_query', 'na_alias_data','na_offer_sell', 'na_cancel_sale_offer', 'na_offer_buy','na_cancel_buy_offer']
NEP5_methods = ['name', 'symbol', 'decimals', 'totalSupply', 'balanceOf', 'transfer', 'transferFrom', 'approve', 'allowance']
SMART_NEP5_METHODS = ['smart_balanceOf', 'smart_transfer', 'smart_transferFrom', 'smart_approve', 'smart_allowance']

def sc_call(alias_info, operation, args):
    """
    :param alias_info:
    :param operation:
    \n:param args []:
    \n:returns True if success or False if failed:
    \ntryes to resolve alias_info and pass call to resolved smartcontract
    \nin case of sub_nas support alias_info is array [alias, sub_nas]
    """
    two = 2 # this is interesting, contract fails if [acc_alias, 4]
    query_args = [alias_info, two]
    sc = na_call("na_query",query_args)
    if sc:
        return DynamicAppCall(sc, operation, args)
    else:
        Notify("SC call failed. Possible reasons: no exists or expired, not in provided NA.")
        return False

def na_call(operation, args):
    """
    :param operation:
    :param args [ [alias_name, sub_nas],... ]:
    \nhandles NA service calls
    """
    nargs = len(args)
    if nargs < 1:
        msg = "Not enough arguments provided for service call."
        Notify(msg)
        return return_value(False,msg)
    else:
        sub_nas = False       
        alias = args[0]

        if not alias:
            return False
        
        if sub_nas:
            if len(alias) > 1:
                sub_nas = alias[1]
            elif len(alias) == 0:
                Notify("Alias name not provided.")
                return False
            alias_name = alias[0]
            if not alias_name:
                Notify("Alias name not provided.")
                return False
        else:
            alias_name = alias    

        if not alias_name:
            return False

        if sub_nas:
            target = na_query(sub_nas,2)
            script_hash = GetExecutingScriptHash()
            if target != script_hash: # do not pass in case we are target
                if target:
                    return DynamicAppCall(target, operation, args)
                else:
                    msg = concat("Failed to resolve: ", sub_nas)
                    Notify(msg)
                    return return_value(False,msg)
        
        args = list_slice(args,1,nargs)
        print(operation)
        if operation == 'na_register':
            return na_register(alias_name, args)
        elif operation == 'na_renew':
            return na_renew(alias_name, args)
        elif operation == 'na_update_target':
            return na_update_target(alias_name, args)
        elif operation == 'na_transfer':
            return na_transfer(alias_name, args)
        elif operation == 'na_delete':
            return na_delete(alias_name, args)
        elif operation == 'na_query':
            return na_query(alias_name, args)
        elif operation == 'na_alias_data':
            return na_alias_data(alias_name, args)
        elif operation == 'na_offer_sell':
            return offer_sell(alias_name, args)
        elif operation == 'na_cancel_sale_offer':
            return cancel_sale_offer(alias_name, args)
        elif operation == 'na_offer_buy':
            return offer_buy(alias_name, args)
        elif operation == 'na_cancel_buy_offer':
            return cancel_buy_offer(alias_name, args)

def dynamic_NEP5_call(operation, args):
    """
    :param operation:
    :param args [ [alias_name, sub_nas],... ]:
    \n tryes to resolve alias_name in specified sub_nas and 
    passes invoke call to resolved alias_target
    """
    nargs = len(args)
    alias = args[0]
    args = list_slice(args, 1, nargs)
    return sc_call(alias,operation,args)

def NEP5_call(operation, args):
    """
    :param operation:
    :param args [...]:
    \nhandles 2 scenarios based on parameters call:
    \n - returns values for NAC token, if standard parameter count
    \n - passes NEP5 call to other asset based on added parameter(args[0]) [alias_name, sub_nas] 
    """
    nargs = len(args)
    if operation == 'name' or operation == 'decimals' or operation == 'symbol' or operation == 'totalSupply':
        
        if nargs == 1:
            return dynamic_NEP5_call(operation, args)

        if operation == 'name':
            return TOKEN_NAME
        if operation == 'decimals':
            return TOKEN_DECIMALS
        if operation == 'symbol':
            return TOKEN_SYMBOL
        if operation == 'totalSupply':
            print(TOKEN_TOTAL_SUPPLY)
            return TOKEN_TOTAL_SUPPLY
    
    arg_error = "Not enough or too many arguments provided."

    if operation == 'balanceOf':
        if nargs == 2:
            return dynamic_NEP5_call(operation, args)
        elif nargs == 1:
            address = args[0]
            return balanceOf(address)
        return arg_error

    elif operation == 'transfer' or operation == 'approve':
        if nargs == 4:
            return dynamic_NEP5_call(operation, args)
        if nargs == 3:
            t_from = args[0]
            t_to = args[1]
            t_amount = args[2]

            if operation == 'transfer':
                return transfer(t_from, t_to, t_amount)

            if operation == 'approve':
                return approve(t_from, t_to, t_amount) # t_from => t_owner, t_to => t_spender
        return arg_error
    
    elif operation == 'transferFrom':
        if nargs == 5:
            return dynamic_NEP5_call(operation, args)
        if nargs == 4:
            t_originator = args[0]
            t_from = args[1]
            t_to = args[2]
            t_amount = args[3]

            if operation == 'transferFrom':
                return transfer_from(t_originator, t_from, t_to, t_amount)
        return arg_error

    elif operation == 'allowance':
        if nargs == 3:
            return dynamic_NEP5_call(operation, args)
        elif nargs == 2:
            t_owner = args[0]
            t_spender = args[1]
            return allowance(t_owner, t_spender)
        return arg_error
    
def smart_NEP5_call(operation, args):
    """
    :param operation:
    :param args [...]:
    \nhandles parameters translation from alias_names to targets
    \n:all parameters are considered NEO accounts - type 4:
    """
    arg_error = "Not enough arguments provided."
    nargs = len(args)
    
    if operation == 'smart_balanceOf':
        index_last = nargs-1
        if nargs == 2 or nargs == 1:
            acc_alias = args[index_last]
            if not acc_alias:
                msg = "Acc alias name not provided."
                Notify(msg)
                return return_value(False,msg)
        else:
            return arg_error
        
        four = 4 # this is interesting, contract fails if [acc_alias, 4]
        query_args = [acc_alias,four]
        address = na_call("na_query",query_args)

        if address:
            args[index_last] = address
            return NEP5_call('balanceOf', args)
        return arg_error

    elif operation == 'smart_transfer' or operation == 'smart_approve':
        index_3rd_to_last = nargs-3
        index_2nd_to_last = nargs-2
        if nargs == 3 or nargs == 4:
            t_from_alias = args[index_3rd_to_last]
            t_to_alias = args[index_2nd_to_last]
            if not t_from_alias or not t_to_alias:
                return arg_error
        else:
            return arg_error

        four = 4 # this is interesting, contract fails if [acc_alias, 4]
        query_args = [t_from_alias, four]
        address_from = na_call("na_query",query_args)
        query_args = [t_to_alias, four]
        address_to = na_call("na_query",query_args)

        if address_from and address_to:
            args[index_3rd_to_last] = address_from
            args[index_2nd_to_last] = address_to
            
            if operation == 'smart_transfer':
                return NEP5_call("transfer",args)

            return NEP5_call("approve",args)
    
    elif operation == 'smart_transferFrom':
        index_4th_to_last = nargs-4
        index_3rd_to_last = nargs-3
        index_2nd_to_last = nargs-2
        if nargs == 4 or nargs == 5:
            t_originator_alias = args[index_4th_to_last]
            t_from_alias = args[index_3rd_to_last]
            t_to_alias = args[index_2nd_to_last]
            if not t_originator_alias or not t_from_alias or not t_to_alias:
                return arg_error
        else:
            return arg_error

        four = 4 # this is interesting, contract fails if [acc_alias, 4]
        query_args = [t_originator_alias, four]
        address_originator = na_call("na_query",query_args)
        query_args = [t_from_alias, four]
        address_from = na_call("na_query",query_args)
        query_args = [t_to_alias, four]
        address_to = na_call("na_query",query_args)

        if address_originator and address_from and address_to:
            args[index_4th_to_last] = address_originator
            args[index_3rd_to_last] = address_from
            args[index_2nd_to_last] = address_to
            
            return NEP5_call("transferFrom",args)

    elif operation == 'smart_allowance':
        index_1st_to_last = nargs-1
        index_2nd_to_last = nargs-2
        if nargs == 2 or nargs == 3:
            t_from_alias = args[index_2nd_to_last]
            t_to_alias = args[index_1st_to_last]
            if not t_from_alias or not t_to_alias:
                return arg_error
        else:
            return arg_error

        four = 4 # this is interesting, contract fails if [acc_alias, 4]
        query_args = [t_from_alias, four]
        address_from = na_call("na_query",query_args)
        query_args = [t_to_alias, four]
        address_to = na_call("na_query",query_args)

        if address_from and address_to:
            args[index_2nd_to_last] = address_from
            args[index_1st_to_last] = address_to
            return NEP5_call("allowance",args)
    
    msg = "Smart NEP5 call failed."
    Notify(msg)
    return return_value(False,msg)
