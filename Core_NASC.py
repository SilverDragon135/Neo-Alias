from boa.blockchain.vm.Neo.TriggerType import Application, Verification
from boa.blockchain.vm.Neo.Runtime import Notify, GetTrigger, CheckWitness
from boa.blockchain.vm.Neo.App import DynamicAppCall
from nas.wrappers.storage import Storage
from boa.blockchain.vm.Neo.Runtime import Notify
from nas.configuration.Administration import AdminConfiguration
from core_nas.configuration import init

def Main(operation, args):
    """
    :Entry point of Core_NA SmartContract:
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
        storage = Storage()
        
        if operation == 'init':
            initialized = storage.load("Core_NASC_initialized")
            if not initialized:
                return init()

        root_na = storage.load("root_NA")
        if root_na:
            return DynamicAppCall(root_na, operation, args)
        else:
            Notify("DynamicAppCall failed.")
            return False