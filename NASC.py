from boa.blockchain.vm.Neo.Runtime import Notify, GetTrigger, CheckWitness, Log
from boa.blockchain.vm.Neo.Action import RegisterAction
from boa.blockchain.vm.Neo.TriggerType import Application, Verification

from nas.gateway.NEP5 import NEP5Gateway
from nas.gateway.SmartNEP5 import SmartNEP5Gateway
from nas.gateway.NeoAliasService import NeoAliasGateway
from nas.configuration.Administration import AdminConfiguration
from nas.configuration.Service import ServiceConfiguration
from nas.core.na import na_query
from nas.common.util import list_slice
from nas.gateway.SC import call_remote_smart_contract

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
            
            #if not configuration.initialized():
            #    if operation == 'init':
            #        return configuration.init()
            #    Notify("NASC is not yet initialized.")
            #    return False

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
                args = list_slice(args,1,nargs)
                
                sc = alias
                return call_remote_smart_contract(alias,operation,args)
                
        return "Uknown operation"
