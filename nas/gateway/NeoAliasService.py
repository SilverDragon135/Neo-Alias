
from boa.blockchain.vm.Neo.Runtime import Notify
from nas.core.base import *
from nas.core.trade import *
from nas.common.util import list_slice


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
        if nargs < 1 and False:
            Notify("Not enough arguments provided for service call.")
            return False
        else:
            alias = args[0]
            sub_nas = None
            alias_name = alias
            """ #uncomment to enable sub-nas support
            if len(alias) > 1:
                sub_nas = alias[1]
            elif len(alias) == 0:
                Notify("Alias name not provided.")
                return False
            alias_name = alias[0]
            if not alias_name:
                Notify("Alias name not provided.")
                return False
            """
            args = list_slice(args,1,nargs)

            if operation == 'na_register':
                return register(alias_name, sub_nas, args)
            elif operation == 'na_renew':
                return renew(alias_name, sub_nas, args)
            elif operation == 'na_update_target':
                return update_target(alias_name, sub_nas, args)
            elif operation == 'na_transfer':
                return transfer(alias_name, sub_nas, args)
            elif operation == 'na_delete':
                return delete(alias_name, sub_nas, args)
            elif operation == 'na_query':
                return query(alias_name, sub_nas, args)
            elif operation == 'na_alias_data':
                return alias_data(alias_name, sub_nas, args)
            elif operation == 'na_offer_sell':
                return offer_sell(alias_name, sub_nas, args)
            elif operation == 'na_cancel_sale_offer':
                return cancel_sale_offer(alias_name, sub_nas, args)
            elif operation == 'na_offer_buy':
                return offer_buy(alias_name, sub_nas, args)
            elif operation == 'na_cancel_buy_offer':
                return cancel_buy_offer(alias_name, sub_nas, args)
