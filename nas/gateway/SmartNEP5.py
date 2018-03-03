from boa.blockchain.vm.Neo.Runtime import Notify
from nas.core.na import na_query
from nas.gateway.NEP5 import NEP5Gateway
from nas.common.util import return_value
from nas.configuration.Service import ServiceConfiguration


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
        configuration = ServiceConfiguration()
        
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

            nargs = len(args)
            sub_nas = b''

            if configuration.support_sub_nas_call and len(acc_alias) > 1:
                sub_nas = acc_alias[1]
                acc_alias_name = acc_alias[0]
            else:
                acc_alias_name = acc_alias

            if not acc_alias_name:
                msg = "Acc alias name not provided."
                Notify(msg)
                return return_value(False,msg)
            
            alias_type_arg = [4]
            address = na_query(acc_alias_name, sub_nas, alias_type_arg)

            if address:
                args[index_last] = address
                return nep5_service.handle_NEP5_call('balanceOf', args)
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


            sub_nas_from = b''
            sub_nas_to = b''

            if configuration.support_sub_nas_call:
                # check if sub_nas_query needed
                if len(t_from_alias) > 1:
                    sub_nas_from = t_from_alias[1]
                if len(t_to_alias) > 1:
                    sub_nas_to = t_to_alias[1]

                from_alias_name = t_from_alias[0]
                to_alias_name = t_to_alias[0]
            else:
                from_alias_name = t_from_alias
                to_alias_name = t_to_alias

            if not from_alias_name or not to_alias_name:
                Notify("Acc alias name not provided.")
                return False

            alias_type_arg = [4]
            address_from = na_query(from_alias_name, sub_nas_from, alias_type_arg)
            address_to = na_query(to_alias_name, sub_nas_to, alias_type_arg)

            if address_from and address_to:
                args[index_3rd_to_last] = address_from
                args[index_2nd_to_last] = address_to
                
                if operation == 'smart_transfer':
                    return nep5_service.handle_NEP5_call("transfer",args)

                return nep5_service.handle_NEP5_call("approve",args)
        
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

            sub_nas_originator=b''
            sub_nas_from = b''
            sub_nas_to = b''

            if configuration.support_sub_nas_call:
                # check if sub_nas_query needed
                if len(t_originator_alias) > 1:
                    sub_nas_originator = t_originator_alias[1]
                if len(t_from_alias) > 1:
                    sub_nas_from = t_from_alias[1]
                if len(t_to_alias) > 1:
                    sub_nas_to = t_to_alias[1]

                originator_alias_name = t_originator_alias[0]
                from_alias_name = t_from_alias[0]
                to_alias_name = t_to_alias[0]
            else:
                originator_alias_name = t_originator_alias
                from_alias_name = t_from_alias
                to_alias_name = t_to_alias

            if not originator_alias_name or not from_alias_name or not to_alias_name:
                Notify("Acc alias name not provided.")
                return False

            alias_type_arg = [4]
            address_originator = na_query(originator_alias_name, sub_nas_originator, alias_type_arg)
            address_from = na_query(from_alias_name, sub_nas_from, alias_type_arg)
            address_to = na_query(to_alias_name, sub_nas_to, alias_type_arg)

            if address_originator and address_from and address_to:
                args[index_4th_to_last] = address_originator
                args[index_3rd_to_last] = address_from
                args[index_2nd_to_last] = address_to
                
                return nep5_service.handle_NEP5_call("transferFrom",args)

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


            sub_nas_from = b''
            sub_nas_to = b''

            if configuration.support_sub_nas_call:
                # check if sub_nas_query needed
                if len(t_from_alias) > 1:
                    sub_nas_from = t_from_alias[1]
                if len(t_to_alias) > 1:
                    sub_nas_to = t_to_alias[1]

                from_alias_name = t_from_alias[0]
                to_alias_name = t_to_alias[0]
            else:
                from_alias_name = t_from_alias
                to_alias_name = t_to_alias

            if not from_alias_name or not to_alias_name:
                Notify("Acc alias name not provided.")
                return False

            alias_type_arg = [4]
            address_from = na_query(from_alias_name, sub_nas_from, alias_type_arg)
            address_to = na_query(to_alias_name, sub_nas_to, alias_type_arg)

            if address_from and address_to:
                args[index_2nd_to_last] = address_from
                args[index_1st_to_last] = address_to
                return nep5_service.handle_NEP5_call("allowance",args)
        
        return "One or both accounts not resolved."
