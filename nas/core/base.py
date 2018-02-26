"""
: NA module
: basic methods for neo alias manipulation
"""
from boa.blockchain.vm.Neo.Runtime import Notify, CheckWitness
from boa.blockchain.vm.Neo.Action import RegisterAction
from nas.configuration.NeoAlias import NeoAliasConfiguration
from nas.common.Alias import Alias, get_alias_target
from nas.core.util import call_sub_nas, try_pay_holding_fee
from nas.common.util import get_header_timestamp
from boa.code.builtins import concat

RegisterAliasEvent = RegisterAction('configurationUpdated', 'name', 'type', 'owner', 'target', 'expiration')
RenewAliasEvent = RegisterAction('configurationUpdated', 'name', 'type', 'expiration')
UpdateAliasTargetEvent = RegisterAction('configurationUpdated', 'name', 'type', 'new_target')
TransferAliasEvent = RegisterAction('transferAlias', 'name', 'type', 'old_owner', 'new_owner')
DeleteAliasEvent = RegisterAction('deleteAlias', 'name', 'type')
QueryAliasEvent = RegisterAction('queryAlias', 'name', 'type', 'result')


def register(alias, sub_nas, args):
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
        Notify("You can register alias only for yourself.")
        return False

    configuration = NeoAliasConfiguration()
    if alias_expiration < get_header_timestamp():
        if not configuration.are_NEO_acc_free_of_chage() or alias_type != 4:
            Notify("You provided already expired alias_expiraton.")
            return False

    new_alias = Alias()
    new_alias.name = alias
    new_alias.atype = alias_type
  
    available = new_alias.is_available_for_registration()

    if not available:
        Notify("Alias is already in use. You can submit buy offer if you are interested.")
        return False

    new_alias._target = alias_target
    valid = new_alias.is_valid()

    if not valid:
        Notify("This alias cannot be registered. Invalid name or target property for given alias_type.")
        return False
    # round duration

    maximum_duration = configuration.get_maximum_registration_duration(alias_type)
    timestamp = get_header_timestamp()
    if alias_expiration - timestamp > maximum_duration:
        alias_expiration = timestamp + maximum_duration

    # calculate duration to pay
    duration_to_pay = alias_expiration - timestamp
    payed = try_pay_holding_fee(alias_owner, alias_type, duration_to_pay)

    if not payed:  # handles assets update
        return False

    new_alias._owner = alias_owner
    new_alias._owner_since = timestamp
    new_alias._expiration = alias_expiration
    # for some reason save does not work direclty ... sad :(
    data = new_alias.get_assigned_data()
    new_alias.save_data(data)
    RegisterAliasEvent(alias, alias_type, alias_owner, alias_target, alias_expiration)
    #new_alias_data = new_alias.get_data()
    return True


def renew(alias, sub_nas, args):
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

    configuration = NeoAliasConfiguration()
    if nargs < 1:
        Notify("Renew requires alias_expiration.")
        return False

    alias_expiration = args[0]
    if nargs > 1:
        alias_type = args[1]
    else:
        alias_type = 0

    configuration = NeoAliasConfiguration()
    NEO_acc_free_of_chage = configuration.are_NEO_acc_free_of_chage()
    if alias_expiration< get_header_timestamp():
        if not NEO_acc_free_of_chage or alias_type != 4:
            Notify("You provided already expired alias_expiraton.")
            return False

    alias_for_renewal = Alias()
    alias_for_renewal.name = alias
    alias_for_renewal.atype = alias_type

    exists = alias_for_renewal.exists() 
    expired = False 
    if exists:
        expired = alias_for_renewal.expired()           

    if not exists or expired:
        msg = concat("Alias not found or expired: ", alias)
        Notify(msg)
        return False

    owner = alias_for_renewal.owner()
    if not CheckWitness(owner):
        Notify("You do not own this alias, so you cannot invoke renew")
        return False

    # check if the alias registration is not too long (to keep alias circulating)
    # round duration

    timestamp = get_header_timestamp()
    maximum_duration = configuration.get_maximum_registration_duration(alias_type)
    if alias_expiration - timestamp > maximum_duration:
        alias_expiration = timestamp + maximum_duration

    # check if requested expiration not already payed

    if NEO_acc_free_of_chage and alias_type == 4:
        Notify("Alias already payed for requested or maximum duration.")
        return False
        
    alias_for_renewal_expiration = alias_for_renewal.expiration()
    if alias_for_renewal_expiration >= alias_expiration:
        Notify("Alias already payed for requested or maximum duration.")
        return False

    # calculate duration to pay
    duration_to_pay = alias_expiration - alias_for_renewal_expiration

    if not try_pay_holding_fee(owner, alias_type, duration_to_pay):  # handles assets update
        return False

    # renew alias
    data = alias_for_renewal.get_data()
    data[2] = alias_expiration
    alias_for_renewal.save_data(data)
    RenewAliasEvent(alias, alias_type, alias_expiration)
    return alias_expiration


def update_target(alias, sub_nas, args):
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

    exists = alias_to_update.exists() 
    expired = False 
    if exists:
        expired = alias_to_update.expired()           

    if not exists or expired:
        msg = concat("Alias not found or expired: ", alias)
        Notify(msg)
        return False

    owner = alias_to_update.owner()
    if not CheckWitness(owner):
        Notify("You do not own this alias, so you cannot update target")
        return False

    alias_to_update._target=alias_target 
    if not alias_to_update.is_target_valid():
        Notify("Not valid target for this alias type.")
        return False

    data = alias_to_update.get_data()
    data[0] = alias_target
    alias_to_update.save_data(data)
    UpdateAliasTargetEvent(alias, alias_type, alias_target)
    msg = concat("Alias target updated: ", alias_target)
    Notify(msg)
    return True


def transfer(alias, sub_nas, args):
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
        Notify("Transfer requires new_alias_owner.")
        return False
    new_alias_owner = args[0]
    if nargs > 1:
        alias_type = args[1]
    else:
        alias_type = 0

    alias_to_transfer = Alias()
    alias_to_transfer.name = alias
    alias_to_transfer.atype = alias_type

    exists = alias_to_transfer.exists()
    expired = False 
    if exists:
        expired = alias_to_transfer.expired()           

    if not exists or expired:
        msg = concat("Alias not found or expired: ", alias)
        Notify(msg)
        return False

    if len(new_alias_owner) != 20:
        Notify("Invalid new owner address. Must be exactly 20 bytes")
        return False

    old_owner = alias_to_transfer.owner()
    if not CheckWitness(old_owner):
        Notify("You do not own this alias, so you cannot invoke renew")
        return False

    # transfer alias
    data = alias_to_transfer.get_data()
    data[1] = new_alias_owner
    alias_to_transfer.save_data(data)
    TransferAliasEvent(alias, alias_type, old_owner, new_alias_owner)
    return True


def delete(alias, sub_nas, args):
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
    exists = alias_to_delete.exists()
    
    if not exists:
        msg = ["Alias not found: ", alias]
        Notify(msg)
        return False

    expired = alias_to_delete.is_available_for_registration()
    # no need to store expired aliases, so in case there will be service for automatic
    # deletion, I let possible to delete expired alias for all callers
    owner = alias_to_delete.owner()

    if CheckWitness(owner) or expired:
        # delete record
        alias_to_delete.delete()
        DeleteAliasEvent(alias, alias_type)
        return True
    Notify("You do not own this alias and it is not expired, so you cannot delete it")
    return False


def query(alias, sub_nas, args):
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
    
    exists = stored_alias.exists() 
    if exists:
        expired = stored_alias.expired()
        if not expired:
            target = stored_alias.target()
            msg = concat("Query resolved: ", target)
            Notify(msg)
            QueryAliasEvent(alias, alias_type, target)
            return target

    msg = concat("Alias not found or expired: ", alias)
    Notify(msg)
    return None


def alias_data(alias, sub_nas, args):
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

    exists = stored_alias.exists() 

    if exists:
        expired = stored_alias.expired()
        if not expired:
            return stored_alias.get_data()
    msg = concat("Alias not found or expired: ", alias)
    Notify(msg)
    return "not found"
