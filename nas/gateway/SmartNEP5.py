from boa.blockchain.vm.Neo.Runtime import Notify
from nas.core.na import query
from nas.gateway.NEP5 import NEP5Gateway


class SmartNEP5Gateway():
    """
    Handles aliases resolving for NEP5 transactions
    """

    def get_methods(self):
        """
        :returns methods supported by Smart NEP5:
        """
        methods = ['smart_balanceOf', 'smart_transfer', 'smart_transferFrom', 'smart_approve', 'smart_allowance']
        return methods

    def handle_NEP5_call(self, operation, args):
        """
        :param operation:
        :param args [...]:
        \nhandles parameters translation from alias_names to targets
        \n:all parameters are considered NEO accounts - type 4:
        """
        nep5_service = NEP5Gateway()
        arg_error = "Not enough arguments provided."
        nargs = len(args)

        if operation == 'smart_balanceOf':
            if nargs == 2:
                acc_alias = args[1]
            elif nargs == 1:
                acc_alias = args[0]
            else:
                return arg_error
            nargs = len(args)
            sub_nas = None
            if len(acc_alias) > 1:
                sub_nas = acc_alias[1]
            elif not acc_alias or not acc_alias[0]:
                Notify("Acc alias name not provided.")
                return False
            acc_alias_name = acc_alias[0]

            qargs = [4]
            address = query(acc_alias_name, sub_nas, qargs)
            if address:
                if nargs == 1:
                    args[0] = address
                else:
                    args[1] == address
                return nep5_service.handle_NEP5_call('balanceOf', args)
            return arg_error

        elif operation == 'smart_transfer' or operation == 'smart_transferFrom' or operation == 'smart_approve' or operation == 'allowance':
            if nargs == 3:
                t_from_alias = args[0]
                t_to_alias = args[1]
            elif nargs == 4:
                t_from_alias = args[1]
                t_to_alias = args[2]
            else:
                return arg_error

            sub_nas_from = None
            sub_nas_to = None
            if len(t_from_alias) > 1:
                sub_nas_from = t_from_alias[1]
            if len(t_to_alias) > 1:
                sub_nas_to = t_to_alias[1]
            elif not t_from_alias or not t_from_alias[0] or not t_to_alias or not t_to_alias[0]:
                Notify("Acc alias name not provided.")
                return False
            from_alias_name = t_from_alias[0]
            to_alias_name = t_to_alias[0]

            qargs = [4]
            address_from = query(from_alias_name, sub_nas_from, qargs)
            address_to = query(to_alias_name, sub_nas_to, qargs)
            if address_from and address_to:

                if nargs == 3:
                    args[0] = address_from
                    args[1] = address_to
                else: 
                    args[1] = address_from
                    args[2] = address_to
                
                if operation == 'smart_transfer':
                    return nep5_service.handle_NEP5_call("transfer",args)
                elif operation == 'smart_transferFrom':
                    return nep5_service.handle_NEP5_call("transferFrom",args)
                elif operation == 'smart_approve':
                    return nep5_service.handle_NEP5_call("approve",args)
                else:
                    return nep5_service.handle_NEP5_call("allowance",args)

            return arg_error
