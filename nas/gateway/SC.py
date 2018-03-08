from boa.blockchain.vm.Neo.Runtime import Notify
from boa.blockchain.vm.Neo.App import DynamicAppCall
from nas.gateway.NeoAliasService import NeoAliasGateway

def call_remote_smart_contract(alias_info, operation, args):
    """
    :param alias_info:
    :param operation:
    \n:param args []:
    \n:returns True if success or False if failed:
    \ntryes to resolve alias_info and pass call to resolved smartcontract
    \nin case of sub_nas support alias_info is array [alias, sub_nas]
    """
    nas_gateway = NeoAliasGateway()
    
    four = 4 # this is interesting, contract fails if [acc_alias, 4]
    query_args = [alias_info, four]
    sc = nas_gateway.handle_service_call("na_query",query_args)
    if sc:
        return DynamicAppCall(sc, operation, args)
    else:
        Notify("SC call failed. Possible reasons: no exists or expired, not in provided NA.")
        return False