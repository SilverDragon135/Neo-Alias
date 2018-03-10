from nas.common.constants import ROOT_ADMIN
from boa.interop.Neo.Runtime import Notify, CheckWitness
from nas.wrappers.storage import storage_save

def init():

    if not CheckWitness(ROOT_ADMIN):
        Notify("Only root_admin can initialize NASC.")
        return False

    root_na_hash = "hash"
    dummy = storage_save("root_NA", root_na_hash)
    dummy = storage_save("Core_NASC_initialized",True)
    Notify("Core NA initialized.")
    return True