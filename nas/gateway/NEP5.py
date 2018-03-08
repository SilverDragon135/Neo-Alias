from boa.blockchain.vm.Neo.App import DynamicAppCall
from boa.blockchain.vm.Neo.Runtime import Notify
from nas.core.na import na_query
from nas.core.na_nep5 import *
from nas.configuration.TokenInfo import Token
from nas.common.Account import Account
from nas.common.util import list_slice
from nas.gateway.SC import call_remote_smart_contract



class NEP5Gateway():

    def get_methods(self):
        """
        \nreturns NEP5 methods as array
        """
        methods = ['name', 'symbol', 'decimals', 'totalSupply', 'balanceOf', 'transfer', 'transferFrom', 'approve', 'allowance']
        return methods

    def dynamic_NEP5_call(self, operation, args):
        """
        :param operation:
        :param args [ [alias_name, sub_nas],... ]:
        \n tryes to resolve alias_name in specified sub_nas and 
        passes invoke call to resolved alias_target
        """
        nargs = len(args)
        alias = args[0]
        args = list_slice(args, 1, nargs)
        return call_remote_smart_contract(alias,operation,args)

    def handle_NEP5_call(self, operation, args):
        """
        :param operation:
        :param args [...]:
        \nhandles 2 scenarios based on parameters call:
        \n - returns values for NAC token, if standard parameter count
        \n - passes NEP5 call to other asset based on added parameter(args[0]) [alias_name, sub_nas] 
        """
        nargs = len(args)
        NAC = Token()
        if operation == 'name' or operation == 'decimals' or operation == 'symbol' or operation == 'totalSupply':
            if nargs == 1:
                return self.dynamic_NEP5_call(operation, args)

            if operation == 'name':
                return NAC.name
            if operation == 'decimals':
                return NAC.decimals
            if operation == 'symbol':
                return NAC.symbol
            if operation == 'totalSupply':
                return NAC.total_supply
        
        arg_error = "Not enough or too many arguments provided."

        if operation == 'balanceOf':
            if nargs == 2:
                return self.dynamic_NEP5_call(operation, args)
            elif nargs == 1:
                address = args[0]
                return balanceOf(address)
            return arg_error

        elif operation == 'transfer' or operation == 'approve':
            if nargs == 4:
                return self.dynamic_NEP5_call(operation, args)
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
                return self.dynamic_NEP5_call(operation, args)
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
                return self.dynamic_NEP5_call(operation, args)
            elif nargs == 2:
                t_owner = args[0]
                t_spender = args[1]
                return allowance(t_owner, t_spender)
            return arg_error
        
