from boa.blockchain.vm.Neo.App import DynamicAppCall
from boa.blockchain.vm.Neo.Runtime import Notify
from nas.core.na import query
from nas.core.na_nep5 import *
from nas.configuration.TokenInfo import Token
from nas.common.Account import Account
from nas.common.util import list_slice



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
        sub_nas = None
        if alias and len(alias) > 1:
            sub_nas = alias[1]
        elif len(alias) == 0:
            Notify("Alias name not provided.")
            return False
        alias_name = alias[0]
        if not alias_name:
            Notify("Alias name not provided.")
            return False
        args = list_slice(args, 1, nargs)
        to_invoke = query(alias_name, sub_nas, 2)  # script hash or asset id ?
        if to_invoke:
            return DynamicAppCall(to_invoke, operation, args)
        else:
            Notify("NEP5 DynamicAppCall failed.")
            return False

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

        elif operation == 'transfer' or operation == 'transferFrom' or operation == 'approve':
            if nargs == 4:
                return self.dynamic_NEP5_call(operation, args)
            if nargs == 3:
                t_from = args[0]
                t_to = args[1]
                t_amount = args[2]
                if operation == 'transfer':
                    return transfer(t_from, t_to, t_amount)

                if operation == 'transferFrom':
                    return transfer_from(t_from, t_to, t_amount)

                if operation == 'approve':
                    return approve(t_from, t_to, t_amount) # t_from => t_owner, t_to => t_spender
            return arg_error

        elif operation == 'allowance':
            if nargs == 3:
                return self.dynamic_NEP5_call(operation, args)
            elif nargs == 2:
                t_owner = args[0]
                t_spender = args[1]
                return allowance(t_owner, t_spender)
            return arg_error
        
