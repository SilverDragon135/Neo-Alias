from boa.blockchain.vm.Neo.Runtime import Notify, GetTrigger, CheckWitness, Log
from boa.blockchain.vm.Neo.Action import RegisterAction
from boa.blockchain.vm.Neo.TriggerType import Application, Verification
from boa.blockchain.vm.Neo.App import DynamicAppCall

from nas.gateway.NEP5 import NEP5Gateway
from nas.gateway.SmartNEP5 import SmartNEP5Gateway
from nas.gateway.NeoAliasService import NeoAliasGateway
from nas.configuration.Administration import AdminConfiguration
from nas.configuration.Service import ServiceConfiguration
from nas.core.na import na_query
from nas.common.util import list_slice

def Main(operation, args):
    """
    :Entry point of NA SmartContract:
    \n NA SmartContract has to conform to this conditions in final implementations:
    \n - configurated trough voting mechanism
    \n - pure dapp - belongs to community
    \n - open source 
    \n - updates managed by group of elected (by other community admins) 
    community admins, propably under control of CoZ if they are interested 
    """
    trigger = GetTrigger()
    if trigger == Verification:
        # check if the invoker is the owner of this contract
        configuration = AdminConfiguration()
        is_owner = CheckWitness(configuration.root_admin)
        # If owner, proceed
        if is_owner:
            return True
        return False

    elif trigger == Application:
        nargs = len(args)
        if operation != None:

            configuration = ServiceConfiguration()
            if not configuration.initialized():
                if operation == 'init':
                    return configuration.init()
                Notify("NASC is not yet initialized.")
                return False

            # just for testing
            if operation == 'na_test':
                Notify("Test Smart Contract Success!")
                return "NASC is up!"

            nep5_gateway = NEP5Gateway()
            for op in nep5_gateway.get_methods():
                if operation == op:
                    return nep5_gateway.handle_NEP5_call(operation, args)

            smart_nep5_gateway = SmartNEP5Gateway()
            for op in smart_nep5_gateway.get_methods():
                if operation == op:
                    return smart_nep5_gateway.handle_NEP5_call(operation, args)

            nas_gateway = NeoAliasGateway()
            methods = nas_gateway.get_methods()
            for op in methods:
                if operation == op:
                    return nas_gateway.handle_service_call(operation, args)
            
            if nargs >= 1:
                alias = args[0]
                sub_nas = None
                alias_name = alias
                """ #uncomment for sub_nas testing
                if len(alias) > 1:
                    sub_nas = alias[1]
                elif len(alias) == 0:
                    Notify("Alias name not provided.")
                    return False
                alias_name = alias[0]
                """
                if not alias_name:
                    Notify("Alias name not provided.")
                    return False
                args = list_slice(args,1,nargs)
                sc = na_query(alias_name, sub_nas, args)
                if sc:
                    return DynamicAppCall(sc, operation, args)
                else:
                    Notify("SC call failed. Possible reasons: no exists or expired, not in provided NA.")
                    return False

        return "Uknown operation"
