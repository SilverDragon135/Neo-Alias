from boa.interop.Neo.TriggerType import Application, Verification
from boa.interop.Neo.Runtime import Notify, GetTrigger, CheckWitness
from boa.interop.Neo.App import DynamicAppCall
from nas.wrappers.storage import storage_load
from nas.common.constants import ROOT_ADMIN
from core_nas.config import init

def Main(operation, args):
    """
    :Entry point of Core_NA SmartContract:
    """

    trigger = GetTrigger()
    if trigger == Verification():
        # check if the invoker is the owner of this contract
        is_owner = CheckWitness(ROOT_ADMIN)
        # If owner, proceed
        if is_owner:
            return True
        return False
    elif trigger == Application():
        if operation == 'init':
            initialized = storage_load("Core_NASC_initialized")
            if not initialized:
                return init()

        root_na = storage_load("root_NA")
        if root_na:
            return DynamicAppCall(root_na, operation, args)
        else:
            Notify("DynamicAppCall failed.")
            return False