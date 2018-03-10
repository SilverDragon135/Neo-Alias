from boa.interop.Neo.Runtime import Notify, GetTrigger, CheckWitness, Log
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.TriggerType import Application, Verification
from boa.builtins import range

from nas.common.util import list_slice
from nas.common.alias import *
from nas.common.acc import *
from nas.config.service import *
from nas.common.token_info import *
from nas.gateway.na import *
#from nas.configuration.Service import init_NA_service, NA_service_initialized

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
    if trigger == Verification():
        # check if the invoker is the owner of this contract
        if CheckWitness(ROOT_ADMIN):
            return True
        return False

    elif trigger == Application():
        if operation != None:
            
            if NA_service_initialized():
                # just for testing
                if operation == 'na_test':
                    Notify("Test Smart Contract Success!")
                    return "NASC is up!"
            
                for op in NEP5_methods:
                    if op == operation:
                        return NEP5_call(operation, args)
                
                for op in SMART_NEP5_METHODS:
                    if op == operation:
                        return smart_NEP5_call(operation, args)

                for op in NA_METHODS:
                    if op == operation:
                        return na_call(operation, args)
                
                nargs = len(args)
                if nargs >= 1:
                    alias = args[0]
                    args = list_slice(args,1,nargs)

                    return sc_call(alias,operation,args)
            else: 
                if operation == 'init':
                    return init_NA_service()
                Notify("NASC is not yet initialized.")
                return False

                
        return "Uknown operation"

