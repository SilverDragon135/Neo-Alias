
from boa.blockchain.vm.Neo.Runtime import Notify
from boa.blockchain.vm.Neo.App import DynamicAppCall
from boa.interop.System.ExecutionEngine import GetExecutingScriptHash
from nas.core.na import *
from nas.core.na_trade import *
from nas.common.util import list_slice, return_value
from nas.configuration.Service import ServiceConfiguration


class NeoAliasGateway():

    def get_methods(self):
        """
        :returns neo alias base and trade methods:
        """
        methods = ['na_register', 'na_renew', 'na_update_target','na_transfer', 'na_delete', 'na_query', 'na_alias_data','na_offer_sell', 'na_cancel_sale_offer', 'na_offer_buy','na_cancel_buy_offer']
        return methods

    def handle_service_call(self, operation, args):
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
            alias = args[0]
            if not alias:
                return False

            sub_nas = b''
            configuration = ServiceConfiguration()

            if configuration.SUPPORT_SUB_NAS:
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
