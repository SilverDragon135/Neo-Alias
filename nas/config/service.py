"""
Module configuration - contains NA root configuration
"""
from boa.interop.Neo.Runtime import Notify, CheckWitness
from boa.interop.Neo.Action import RegisterAction
from nas.common.constants import *
from nas.common.acc import add_account_available_assets

ConfigurationUpdatedEvent = RegisterAction('configurationUpdated', 'option', 'value')


"""
:Interface to access NEO Alias configuration:
\n :Configuration will be determined based on voting mechanism, that will be implemented later:
\n Final implementation will prevent centralized control and except init() method for initial
setup, configuration is going to be controloble only trough voting
"""

def init_NA_service():
    """
    :Initializes dapp NASC:
    """
    if not CheckWitness(ROOT_ADMIN):
        msg = "Only root_admin can initialize NASC."
        Notify(msg)
        return msg
    
    # initialize
    dummy = storage_save("NASC_initialized", True)
    #init for testing
    if DEBUG:
        dummy = add_account_available_assets(ROOT_ADMIN,10000)

    msg="NASC initialized."
    Notify(msg)
    return msg

def NA_service_initialized():
    return storage_load("NASC_initialized")

# registration configuration

def get_maximum_registration_duration(alias_type):
    """
    :param type:
    \n:returns maximum alias duration for given type:
    """
    key = concat(b'max_reg_dur', alias_type)
    hard_coded_minimum = 604800  # week
    
    maximum_registration_duration = storage_load(key)
    if not maximum_registration_duration or maximum_registration_duration < hard_coded_minimum:
        return hard_coded_minimum
    else:
        return maximum_registration_duration

def set_maximum_registration_duration(duration, alias_type):
    """
    :param duration:
    \n:param type:
    \nsets maximum alias registration duration for given type
    """
    key = b'max_reg_dur'
    key = concat(key, alias_type)
    storage_delete(key)
    storage_save(key, duration)
    ConfigurationUpdatedEvent(key, duration)
    return True

def get_reservation_duration():
    """
    :returns reservation duration:
    """
    hard_coded_minimum = 0  # prevent negative reservation
    key = b'res_dur'
    reservation_duration = storage_load(key)
    if not reservation_duration or reservation_duration < hard_coded_minimum:
        return hard_coded_minimum
    else:
        return reservation_duration

def set_reservation_duration(duration):
    """
    :param duration:
    \nsets reservation duration
    """
    key = b'res_dur'
    storage_delete(key)
    storage_save(key, duration)
    ConfigurationUpdatedEvent(key, duration)
    return True
# fee configuration

def get_fee_per_period(alias_type):
    """
    :param type:
    \n:returns fee per period for given type:
    """
    neo_accs_free_of_charge = are_NEO_acc_free_of_charge()
    if alias_type == 4 and neo_accs_free_of_charge:
        return 0
    key = concat(b'fee_per_period', alias_type)
    hard_coded_minimum = 0  # prevent negative fee
    fee_per_period = storage_load(key)
    if not fee_per_period or fee_per_period < hard_coded_minimum:
        return hard_coded_minimum
    else:
        return fee_per_period

def set_fee_per_period(fee, alias_type):
    """
    :param fee:
    \n:param type:
    \nsets fee per period for given type
    """
    key = concat(b'fee_per_period', alias_type)
    storage_delete(key)
    storage_save(key, fee)
    ConfigurationUpdatedEvent(key, fee)
    return True

def get_fee_period():
    """
    :returns fee_period:
    """
    hard_coded_minimum = 86400  # minimum fee period can be 1 day
    key = b'fee_period'
    fee_period = storage_load(key)
    if not fee_period or fee_period < hard_coded_minimum:
        return hard_coded_minimum
    else:
        return fee_period

def set_fee_period(period):
    """
    :param period:
    \nsets fee period
    """
    key = b'fee_period'
    storage_delete(key)
    storage_save(key, period)
    ConfigurationUpdatedEvent(key, period)
    return True

# commissions
def get_trade_commission():
    """
    :returns trade commission:
    """
    hard_coded_minimum = 0  # prevent negative bonus
    hard_coded_maximum = 50
    key = b'trade_commission'
    trade_commission = storage_load(key)
    if not trade_commission or trade_commission < hard_coded_minimum:
        return hard_coded_minimum
    elif trade_commission > hard_coded_maximum:
        return hard_coded_maximum
    else:
        return trade_commission

def set_trade_commission(trade_commission):
    """
    :param trade_commission:
    sets trade commission
    """
    key = b'trade_commission'
    storage_delete(key)
    storage_save(key, trade_commission)
    ConfigurationUpdatedEvent(key, trade_commission)
    return True

def set_are_NEO_acc_free_of_charge(free):
    """
    :param free:
    \nenalbles/disables free NEO accs (NEO564522165)
    """
    key = b'non_expirable_accs'
    storage_delete(key)
    storage_save(key,free)
    ConfigurationUpdatedEvent(key, free)
    return True

def are_NEO_acc_free_of_charge():
    """
    :returns True/False:
    \nmens NEO accs (NEO564522165) are free
    """
    key = b'non_expirable_accs'
    stored = storage_load(key)
    if not stored:
        return True
    return stored