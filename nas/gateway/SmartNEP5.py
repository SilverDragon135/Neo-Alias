from boa.blockchain.vm.Neo.Runtime import Notify
from nas.gateway.NEP5 import NEP5Gateway
from nas.common.util import return_value
from nas.configuration.Service import ServiceConfiguration
from nas.gateway.NeoAliasService import NeoAliasGateway


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
        nas_gateway = NeoAliasGateway()
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
            
            four = 4 # this is interesting, contract fails if [acc_alias, 4]
            query_args = [acc_alias,four]
            address = nas_gateway.handle_service_call("na_query",query_args)

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

            four = 4 # this is interesting, contract fails if [acc_alias, 4]
            query_args = [t_from_alias, four]
            address_from = nas_gateway.handle_service_call("na_query",query_args)
            query_args = [t_to_alias, four]
            address_to = nas_gateway.handle_service_call("na_query",query_args)

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

            four = 4 # this is interesting, contract fails if [acc_alias, 4]
            query_args = [t_originator_alias, four]
            address_originator = nas_gateway.handle_service_call("na_query",query_args)
            query_args = [t_from_alias, four]
            address_from = nas_gateway.handle_service_call("na_query",query_args)
            query_args = [t_to_alias, four]
            address_to = nas_gateway.handle_service_call("na_query",query_args)

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

            four = 4 # this is interesting, contract fails if [acc_alias, 4]
            query_args = [t_from_alias, four]
            address_from = nas_gateway.handle_service_call("na_query",query_args)
            query_args = [t_to_alias, four]
            address_to = nas_gateway.handle_service_call("na_query",query_args)

            if address_from and address_to:
                args[index_2nd_to_last] = address_from
                args[index_1st_to_last] = address_to
                return nep5_service.handle_NEP5_call("allowance",args)
        
        msg = "Smart NEP5 call failed."
        Notify(msg)
        return return_value(False,msg)
