from nas.configuration.Administration import AdminConfiguration
from boa.blockchain.vm.Neo.Runtime import Notify, CheckWitness
from nas.wrappers.storage import Storage

def init():
    storage = Storage()
    configuration = AdminConfiguration()

    if not CheckWitness(configuration.root_admin):
        Notify("Only root_admin can initialize NASC.")
        return False

    root_na_hash = ""
    storage.save("root_NA", root_na_hash)
    storage.save("Core_NASC_initialized",True)
    return True

