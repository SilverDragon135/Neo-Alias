"""
: NA module
: basic methods for neo alias manipulation
"""
from boa.interop.Neo.Runtime import Notify, CheckWitness
from boa.interop.Neo.Action import RegisterAction
from nas.config.service import are_NEO_acc_free_of_charge, get_maximum_registration_duration
from nas.common.alias import *
from nas.core.util import try_pay_holding_fee
from nas.common.util import get_header_timestamp, return_value
from boa.builtins import concat

RegisterAliasEvent = RegisterAction('registerAlias', 'name', 'type', 'owner', 'target', 'expiration')
RenewAliasEvent = RegisterAction('renewAlias', 'name', 'type', 'expiration')
UpdateAliasTargetEvent = RegisterAction('updateAlias', 'name', 'type', 'new_target')
TransferAliasEvent = RegisterAction('transferAlias', 'name', 'type', 'old_owner', 'new_owner')
DeleteAliasEvent = RegisterAction('deleteAlias', 'name', 'type')
QueryAliasEvent = RegisterAction('queryAlias', 'name', 'type', 'result')


def na_register(alias, args):
    """
    :param alias:
    \n:param args [owner, type, target, expiration]:
    \n:returns expiration if success or False if failed:
    \nif sub_nas defined passes call to sub_nas otherwise
    we try to register alias
    """
    if len(args) < 4:
        Notify("Not enough arguments provided. Requires: alias_owner, alias_type, alias_target, alias_expiration")
        return False
    
    alias_owner = args[0]
    alias_type = args[1]
    alias_target = args[2]
    alias_expiration = args[3]


    if not CheckWitness(alias_owner):
        msg = "You can register alias only for yourself." 
        Notify(msg)
        return return_value(False,msg)

    timestamp = get_header_timestamp()
    if alias_expiration < timestamp:
        free_neo_acc = are_NEO_acc_free_of_charge()
        if not free_neo_acc or alias_type != 4:
            msg = "You provided already expired alias_expiraton."
            Notify(msg)
            return return_value(False,msg)

    new_alias = init_alias(alias,alias_type)    

    if alias_exists(new_alias):

        new_alias = alias_load(new_alias)

        available = alias_available_for_registration(new_alias)
        if not available:
            msg = "Alias is already in use. You can submit buy offer if you are interested."
            Notify(msg)
            return return_value(False,msg)
      
    dummy = alias_set_target(new_alias, alias_target)

    if not alias_is_valid(new_alias):
        msg = "This alias cannot be registered. Invalid name or target property for given alias_type."
        Notify(msg)
        return return_value(False,msg)

    # check if the alias registration is not too long (to keep alias circulating)
    # adjust duration
    maximum_duration = get_maximum_registration_duration(alias_type)
    if alias_expiration - timestamp > maximum_duration:
        alias_expiration = timestamp + maximum_duration

    # calculate duration to pay
    duration_to_pay = alias_expiration - timestamp

    if not try_pay_holding_fee(alias_owner, alias_type, duration_to_pay):  # handles assets update
        msg = "Not enough assets to pay for alias."
        Notify(msg)
        return return_value(False,msg)

    dummy = alias_set_owner(new_alias, alias_owner)
    dummy = alias_set_owner_since(new_alias, timestamp)
    dummy = alias_set_expiration(new_alias,alias_expiration)

    dummy = alias_save(new_alias)

    RegisterAliasEvent(alias, alias_type, alias_owner, alias_target, alias_expiration)
    msg = concat("Alias registered: ", alias)
    Notify(msg)
    return return_value(True,msg)


def na_renew(alias, args):
    """
    :param alias:
    \n:param args [expiration, type]:
    \n:returns new expiration if success or False if failed:
    \nif sub_nas defined passes call to sub_nas otherwise
    we try to renew alias
    """
    nargs = len(args)

    if nargs < 1:
        msg = "Renew requires alias_expiration."
        Notify(msg)
        return return_value(False,msg)

    alias_expiration = args[0]
    if nargs > 1:
        alias_type = args[1]
    else:
        alias_type = 0
    
    NEO_acc_free_of_chage = are_NEO_acc_free_of_charge()
    if alias_expiration< get_header_timestamp():
        if not NEO_acc_free_of_chage or alias_type != 4:
            msg = "You provided already expired alias_expiraton."
            Notify(msg)
            return return_value(False,msg)

    alias_for_renewal = init_alias(alias,alias_type)

    if not alias_exists(alias_for_renewal):
        msg = concat("Alias not found: ", alias)
        Notify(msg)
        return return_value(False,msg)
   
    alias_for_renewal = alias_load(alias_for_renewal)

    if alias_expired(alias_for_renewal):
        msg = concat("Alias expired: ", alias)
        Notify(msg)
        return return_value(False,msg)

    owner = alias_get_owner(alias_for_renewal)
    if not CheckWitness(owner):
        msg = "You do not own this alias, so you cannot invoke renew"
        Notify(msg)
        return return_value(False,msg)

    # check if the alias registration is not too long (to keep alias circulating)
    # adjust duration
    timestamp = get_header_timestamp()
    maximum_duration = get_maximum_registration_duration(alias_type)
    if alias_expiration - timestamp > maximum_duration:
        alias_expiration = timestamp + maximum_duration

    # check if requested expiration not already payed

    if NEO_acc_free_of_chage and alias_type == 4:
        msg = "Alias already payed for requested or maximum duration."
        Notify(msg)
        return return_value(False,msg)

    current_alias_expiration = alias_get_expiration(alias_for_renewal)
    if current_alias_expiration >= alias_expiration:
        msg = "Alias already payed for requested or maximum duration."
        Notify(msg)
        return return_value(False,msg)

    # calculate duration to pay
    duration_to_pay = alias_expiration - current_alias_expiration

    if not try_pay_holding_fee(owner, alias_type, duration_to_pay):  # handles assets update
        msg = "Not enough assets to pay for alias."
        Notify(msg)
        return return_value(False,msg)

    # renew alias
    dummy = alias_set_expiration(alias_for_renewal,alias_expiration)
    
    dummy = alias_save(alias_for_renewal)

    RenewAliasEvent(alias, alias_type, alias_expiration)
    msg = concat("Alias renew success. New expiration: ", alias_expiration)
    Notify(msg)
    return return_value(alias_expiration,msg)


def na_update_target(alias, args):
    """
    :param alias:
    \n:param args [target, type]:
    \n:returns True if success or False if failed:
    \nif sub_nas defined passes call to sub_nas otherwise
    we try to setup new target
    """
    nargs = len(args)

    if nargs < 1:
        Notify("update_target requires alias_target.")
        return False
    alias_target = args[0]
    if nargs > 1:
        alias_type = args[1]
    else:
        alias_type = 0

    alias_to_update = init_alias(alias,alias_type)

    if not alias_exists(alias_to_update):
        msg = concat("Alias not found: ", alias)
        Notify(msg)
        return return_value(False,msg)
   
    alias_to_update = alias_load(alias_to_update)

    if alias_expired(alias_to_update):
        msg = concat("Alias expired: ", alias)
        Notify(msg)
        return return_value(False,msg)       

    owner = alias_get_owner(alias_to_update)
    if not CheckWitness(owner):
        msg = "You do not own this alias, so you cannot update target"
        Notify(msg)
        return return_value(False,msg)

    dummy = alias_set_target(alias_to_update, alias_target)
    if not alias_target_valid(alias_to_update):
        msg = "Not valid target for this alias type."
        Notify(msg)
        return return_value(False,msg)      

    dummy = alias_save(alias_to_update)
    UpdateAliasTargetEvent(alias, alias_type, alias_target)
    msg = concat("Alias target updated: ", alias_target)
    Notify(msg)
    return return_value(True,msg)


def na_transfer(alias, args):
    """
    :param alias:
    \n:param args [new_owner, type]:
    \n:returns True if success or False if failed:
    \nif sub_nas defined passes call to sub_nas otherwise
    we try to transfer alias
    """
    nargs = len(args)

    if nargs < 1:
        msg = concat("Transfer requires new_alias_owner.")
        Notify(msg)
        return return_value(False,msg)

    new_alias_owner = args[0]
    if nargs > 1:
        alias_type = args[1]
    else:
        alias_type = 0

    alias_to_transfer = init_alias(alias,alias_type)

    if not alias_exists(alias_to_transfer):
        msg = concat("Alias not found: ", alias)
        Notify(msg)
        return return_value(False,msg)
   
    alias_to_transfer = alias_load(alias_to_transfer)
    if alias_expired(alias_to_transfer):
        msg = concat("Alias expired: ", alias)
        Notify(msg)
        return return_value(False,msg)       

    if len(new_alias_owner) != 20:
        msg = "Invalid new owner address. Must be exactly 20 bytes"
        Notify(msg)
        return return_value(False,msg)

    old_owner = alias_get_owner(alias_to_transfer)
    if not CheckWitness(old_owner):
        msg = "You do not own this alias, so you cannot invoke transfer"
        Notify(msg)
        return return_value(False,msg)

    # transfer alias
    dummy = alias_set_owner(alias_to_transfer, new_alias_owner)    
    dummy = alias_save(alias_to_transfer)
    
    msg = concat("Alias ", alias)
    msg = concat(msg, " transfered to: ")
    msg = concat(msg, new_alias_owner)
    Notify(msg)
    TransferAliasEvent(alias, alias_type, old_owner, new_alias_owner)
    return return_value(True,msg)


def na_delete(alias, args):
    """
    :param alias:
    \n:param args [type]:
    \n:returns True if success or False if failed:
    \nif sub_nas defined passes call to sub_nas otherwise
    we try to delete alias
    """
    if len(args) > 0:
        alias_type = args[0]
    else:
        alias_type = 0

    alias_to_delete = init_alias(alias,alias_type)
    
    if not alias_exists(alias_to_delete):
        msg = concat("Alias not found: ", alias)
        Notify(msg)
        return return_value(False,msg)

    alias_to_delete = alias_load(alias_to_delete)
    # no need to store expired aliases, so in case there will be service for automatic
    # deletion, I let possible to delete expired alias for all callers
    available = alias_available_for_registration(alias_to_delete)
    owner = alias_get_owner(alias_to_delete)
    if CheckWitness(owner) or available:
        # delete record
        dummy = alias_delete(alias_to_delete)
        msg = concat("Alias ", alias)
        msg = concat(msg, " type ")
        msg = concat(msg, alias_type)
        msg = concat(msg, " deleted.")
        Notify(msg)
        DeleteAliasEvent(alias, alias_type)
        return return_value(True,msg)

    msg = "You do not own this alias and it is not expired, so you cannot delete it"
    Notify(msg)
    return return_value(False,msg)


def na_query(alias, args):
    """
    :param alias:
    \n:param args [type]:
    \n:returns alias target if success or False if failed:
    \nif sub_nas defined passes call to sub_nas otherwise
    we try to query alias target
    """
    if len(args) > 0:
        alias_type = args[0]
    else:
        alias_type = 0

    stored_alias = init_alias(alias,alias_type)
    
    if alias_exists(stored_alias):
        stored_alias = alias_load(stored_alias)
        if not alias_expired(stored_alias):
            target = alias_get_target(stored_alias)
            msg = concat("Query resolved: ", target)
            Notify(msg)
            QueryAliasEvent(alias, alias_type, target)
            return target

    msg = concat("Alias ", alias)
    msg = concat(msg, " not found or expired.")
    Notify(msg)
    return return_value(False,msg)


def na_alias_data(alias, args):
    """
    :param alias:
    \n:param args [type]:
    \n:returns alias data as array if success or None if failed:
    \nif sub_nas defined passes call to sub_nas otherwise
    we try to get alias data
    """

    if len(args) > 0:
        alias_type = args[0]
    else:
        alias_type = 0

    stored_alias = init_alias(alias,alias_type)

    if alias_exists(stored_alias) :
        stored_alias = alias_load(stored_alias)
        if not alias_expired(stored_alias):
            data = alias_get_data(stored_alias)
            Notify(data)
            return data
    msg = concat("Alias ", alias)
    msg = concat(msg, " not found or expired.")
    Notify(msg)
    return return_value(False,msg)

