"""
: NA module
: basic methods for neo alias manipulation
"""
from boa.blockchain.vm.Neo.Runtime import Notify, CheckWitness
from boa.blockchain.vm.Neo.Action import RegisterAction
from nas.configuration.Service import ServiceConfiguration
from nas.common.Alias import Alias, load_alias
from nas.core.util import call_sub_nas, try_pay_holding_fee
from nas.common.util import get_header_timestamp, return_value
from boa.code.builtins import concat
from nas.wrappers.storage import Storage

RegisterAliasEvent = RegisterAction('configurationUpdated', 'name', 'type', 'owner', 'target', 'expiration')
RenewAliasEvent = RegisterAction('configurationUpdated', 'name', 'type', 'expiration')
UpdateAliasTargetEvent = RegisterAction('configurationUpdated', 'name', 'type', 'new_target')
TransferAliasEvent = RegisterAction('transferAlias', 'name', 'type', 'old_owner', 'new_owner')
DeleteAliasEvent = RegisterAction('deleteAlias', 'name', 'type')
QueryAliasEvent = RegisterAction('queryAlias', 'name', 'type', 'result')


def na_register(alias, sub_nas, args):
    """
    :param alias:
    :param sub_nas:
    \n:param args [owner, type, target, expiration]:
    \n:returns expiration if success or False if failed:
    \nif sub_nas defined passes call to sub_nas otherwise
    we try to register alias
    """
    # resolve sub_nas situation first
    nargs = len(args)
    if sub_nas:
        return call_sub_nas(sub_nas, "na_register", args)
    elif nargs < 4:
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

    configuration = ServiceConfiguration()
    if alias_expiration < get_header_timestamp():
        if not configuration.are_NEO_acc_free_of_charge() or alias_type != 4:
            msg = "You provided already expired alias_expiraton."
            Notify(msg)
            return return_value(False,msg)

    new_alias = Alias()
    new_alias.name = alias
    new_alias.atype = alias_type

   
    if new_alias.exists():
        new_alias = load_alias(new_alias)

        available = new_alias.available_for_registration()
        if not available:
            msg = "Alias is already in use. You can submit buy offer if you are interested."
            Notify(msg)
            return return_value(False,msg)
    
    new_alias.target = alias_target
    if not new_alias.is_valid():
        msg = "This alias cannot be registered. Invalid name or target property for given alias_type."
        Notify(msg)
        return return_value(False,msg)
    
    # check if the alias registration is not too long (to keep alias circulating)
    # adjust duration
    maximum_duration = configuration.get_maximum_registration_duration(alias_type)
    timestamp = get_header_timestamp()
    if alias_expiration - timestamp > maximum_duration:
        alias_expiration = timestamp + maximum_duration

    # calculate duration to pay
    duration_to_pay = alias_expiration - timestamp
    if not try_pay_holding_fee(alias_owner, alias_type, duration_to_pay):  # handles assets update
        msg = "Not enough assets to pay for alias."
        Notify(msg)
        return return_value(False,msg)

    new_alias.owner=alias_owner
    new_alias.owner_since=timestamp
    new_alias.expiration=alias_expiration
    new_alias.save()

    RegisterAliasEvent(alias, alias_type, alias_owner, alias_target, alias_expiration)
    msg = concat("Alias registered: ", alias)
    Notify(msg)
    return return_value(True,msg)


def na_renew(alias, sub_nas, args):
    """
    :param alias:
    :param sub_nas:
    \n:param args [expiration, type]:
    \n:returns new expiration if success or False if failed:
    \nif sub_nas defined passes call to sub_nas otherwise
    we try to renew alias
    """
    # handle sub_nas first
    nargs = len(args)
    if sub_nas:
        return call_sub_nas(sub_nas, "na_renew", args)

    configuration = ServiceConfiguration()
    if nargs < 1:
        msg = "Renew requires alias_expiration."
        Notify(msg)
        return return_value(False,msg)

    alias_expiration = args[0]
    if nargs > 1:
        alias_type = args[1]
    else:
        alias_type = 0

    configuration = ServiceConfiguration()
    NEO_acc_free_of_chage = configuration.are_NEO_acc_free_of_charge()
    if alias_expiration< get_header_timestamp():
        if not NEO_acc_free_of_chage or alias_type != 4:
            msg = "You provided already expired alias_expiraton."
            Notify(msg)
            return return_value(False,msg)

    alias_for_renewal = Alias()
    alias_for_renewal.name = alias
    alias_for_renewal.atype = alias_type

    if not alias_for_renewal.exists():
        msg = concat("Alias not found: ", alias)
        Notify(msg)
        return return_value(False,msg)
   
    alias_for_renewal = load_alias(alias_for_renewal)

    if alias_for_renewal.expired():
        msg = concat("Alias expired: ", alias)
        Notify(msg)
        return return_value(False,msg)

    if not CheckWitness(alias_for_renewal.owner):
        msg = "You do not own this alias, so you cannot invoke renew"
        Notify(msg)
        return return_value(False,msg)

    # check if the alias registration is not too long (to keep alias circulating)
    # adjust duration
    timestamp = get_header_timestamp()
    maximum_duration = configuration.get_maximum_registration_duration(alias_type)
    if alias_expiration - timestamp > maximum_duration:
        alias_expiration = timestamp + maximum_duration

    # check if requested expiration not already payed

    if NEO_acc_free_of_chage and alias_type == 4:
        msg = "Alias already payed for requested or maximum duration."
        Notify(msg)
        return return_value(False,msg)
        
    if alias_for_renewal.expiration >= alias_expiration:
        msg = "Alias already payed for requested or maximum duration."
        Notify(msg)
        return return_value(False,msg)

    # calculate duration to pay
    duration_to_pay = alias_expiration - alias_for_renewal.expiration

    if not try_pay_holding_fee(alias_for_renewal.owner, alias_type, duration_to_pay):  # handles assets update
        msg = "Not enough assets to pay for alias."
        Notify(msg)
        return return_value(False,msg)

    # renew alias
    alias_for_renewal.expiration = alias_expiration
    alias_for_renewal.save()

    RenewAliasEvent(alias, alias_type, alias_expiration)
    msg = concat("Alias renew success. New expiration: ", alias_expiration)
    Notify(msg)
    return return_value(alias_expiration,msg)


def na_update_target(alias, sub_nas, args):
    """
    :param alias:
    :param sub_nas:
    \n:param args [target, type]:
    \n:returns True if success or False if failed:
    \nif sub_nas defined passes call to sub_nas otherwise
    we try to setup new target
    """
    nargs = len(args)
    if sub_nas:
        return call_sub_nas(sub_nas, "na_update_target", args)

    if nargs < 1:
        Notify("update_target requires alias_target.")
        return False
    alias_target = args[0]
    if nargs > 1:
        alias_type = args[1]
    else:
        alias_type = 0

    alias_to_update = Alias()
    alias_to_update.name = alias
    alias_to_update.atype = alias_type

    if not alias_to_update.exists():
        msg = concat("Alias not found: ", alias)
        Notify(msg)
        return return_value(False,msg)
   
    alias_to_update = load_alias(alias_to_update)

    if alias_to_update.expired():
        msg = concat("Alias expired: ", alias)
        Notify(msg)
        return return_value(False,msg)       

    if not CheckWitness(alias_to_update.owner):
        msg = "You do not own this alias, so you cannot update target"
        Notify(msg)
        return return_value(False,msg)

    alias_to_update.target=alias_target
    if not alias_to_update.target_valid():
        msg = "Not valid target for this alias type."
        Notify(msg)
        return return_value(False,msg)      

    alias_to_update.save()
    UpdateAliasTargetEvent(alias, alias_type, alias_target)
    msg = concat("Alias target updated: ", alias_target)
    Notify(msg)
    return return_value(True,msg)


def na_transfer(alias, sub_nas, args):
    """
    :param alias:
    :param sub_nas:
    \n:param args [new_owner, type]:
    \n:returns True if success or False if failed:
    \nif sub_nas defined passes call to sub_nas otherwise
    we try to transfer alias
    """
    # handle sub_nas first
    nargs = len(args)
    if sub_nas:
        return call_sub_nas(sub_nas, "na_transfer", args)

    if nargs < 1:
        msg = concat("Transfer requires new_alias_owner.")
        Notify(msg)
        return return_value(False,msg)

    new_alias_owner = args[0]
    if nargs > 1:
        alias_type = args[1]
    else:
        alias_type = 0

    alias_to_transfer = Alias()
    alias_to_transfer.name = alias
    alias_to_transfer.atype = alias_type

    if not alias_to_transfer.exists():
        msg = concat("Alias not found: ", alias)
        Notify(msg)
        return return_value(False,msg)
   
    alias_to_transfer = load_alias(alias_to_transfer)
    if alias_to_transfer.expired():
        msg = concat("Alias expired: ", alias)
        Notify(msg)
        return return_value(False,msg)       

    if len(new_alias_owner) != 20:
        msg = "Invalid new owner address. Must be exactly 20 bytes"
        Notify(msg)
        return return_value(False,msg)

    old_owner = alias_to_transfer.owner
    if not CheckWitness(old_owner):
        msg = "You do not own this alias, so you cannot invoke transfer"
        Notify(msg)
        return return_value(False,msg)

    # transfer alias
    alias_to_transfer.owner = new_alias_owner
    alias_to_transfer.save()
    msg = concat("Alias ", alias_to_transfer.name)
    msg = concat(msg, " transfered to: ")
    msg = concat(msg, alias_to_transfer.owner)
    Notify(msg)
    TransferAliasEvent(alias, alias_type, old_owner, new_alias_owner)
    return return_value(True,msg)


def na_delete(alias, sub_nas, args):
    """
    :param alias:
    :param sub_nas:
    \n:param args [type]:
    \n:returns True if success or False if failed:
    \nif sub_nas defined passes call to sub_nas otherwise
    we try to delete alias
    """
    nargs = len(args)
    if sub_nas:
        return call_sub_nas(sub_nas, "na_delete", args)
    if nargs > 0:
        alias_type = args[0]
    else:
        alias_type = 0

    alias_to_delete = Alias()
    alias_to_delete.name = alias
    alias_to_delete.atype = alias_type
    
    if not alias_to_delete.exists():
        msg = concat("Alias not found: ", alias)
        Notify(msg)
        return return_value(False,msg)

    alias_to_delete = load_alias(alias_to_delete)
    # no need to store expired aliases, so in case there will be service for automatic
    # deletion, I let possible to delete expired alias for all callers
    available = alias_to_delete.available_for_registration()
    if CheckWitness(alias_to_delete.owner) or available:
        # delete record
        alias_to_delete.delete()
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


def na_query(alias, sub_nas, args):
    """
    :param alias:
    :param sub_nas:
    \n:param args [type]:
    \n:returns alias target if success or False if failed:
    \nif sub_nas defined passes call to sub_nas otherwise
    we try to query alias target
    """
    # handle sub_nas first
    nargs = len(args)
    if sub_nas:
        return call_sub_nas(sub_nas, "na_query", args)

    if nargs > 0:
        alias_type = args[0]
    else:
        alias_type = 0

    stored_alias = Alias()
    stored_alias.name = alias
    stored_alias.atype = alias_type
    
    if stored_alias.exists():
        stored_alias = load_alias(stored_alias)
        if not stored_alias.expired():
            target = stored_alias.target
            msg = concat("Query resolved: ", target)
            Notify(msg)
            QueryAliasEvent(alias, alias_type, target)
            return target

    msg = concat("Alias ", alias)
    msg = concat(msg, " not found or expired.")
    Notify(msg)
    return return_value(False,msg)


def na_alias_data(alias, sub_nas, args):
    """
    :param alias:
    :param sub_nas:
    \n:param args [type]:
    \n:returns alias data as array if success or None if failed:
    \nif sub_nas defined passes call to sub_nas otherwise
    we try to get alias data
    """
    # handle sub_nas first
    nargs = len(args)
    if sub_nas:
        return call_sub_nas(sub_nas, "na_alias_data", args)

    if nargs > 0:
        alias_type = args[0]
    else:
        alias_type = 0

    stored_alias = Alias()
    stored_alias.name = alias
    stored_alias.atype = alias_type
    if stored_alias.exists() :
        stored_alias = load_alias(stored_alias)
        if not stored_alias.expired():
            return stored_alias.get_data()
    msg = concat("Alias ", alias)
    msg = concat(msg, " not found or expired.")
    Notify(msg)
    return return_value(False,msg)
