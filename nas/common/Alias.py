"""
Holds Alias structures

- it shows, how it ends coding if you try OOP, but compiler support is very small
"""

from boa.builtins import concat
from boa.interop.Neo.Runtime import CheckWitness

from nas.wrappers.storage import storage_load, storage_save, storage_delete, serialize_array, deserialize_bytearray
from nas.common.util import get_header_timestamp

def init_alias(name,atype):
    alias =[[name, atype], [b'', b'', 0, 0, b'', 0, 0, b'', False, 0]]
    return alias

#region alias ID
def alias_get_name(alias):
    alias_id = alias[0]
    return alias_id[0]

def alias_set_name(alias, name):
    alias_id = alias[0]
    alias_id[0] = name

def alias_get_type(alias):
    alias_id = alias[0]
    return alias_id[1]

def alias_set_type(alias, atype):
    alias_id = alias[0]
    alias_id[1] = atype
#endregion alias ID

#region alias_data
def alias_get_target(alias):
    alias_data = alias[1]
    return alias_data[0]

def alias_set_target(alias, target):
    alias_data = alias[1]
    alias_data[0] = target

def alias_get_owner(alias):
    alias_data = alias[1]
    return alias_data[1]

def alias_set_owner(alias, owner):
    alias_data = alias[1]
    alias_data[1] = owner

def alias_get_expiration(alias):
    alias_data = alias[1]
    return alias_data[2]

def alias_set_expiration(alias, expiration):
    alias_data = alias[1]
    alias_data[2] = expiration

def alias_get_owner_since(alias):
    alias_data = alias[1]
    return alias_data[3]

def alias_set_owner_since(alias, owner_since):
    alias_data = alias[1]
    alias_data[3] = owner_since

def alias_get_buy_offer_owner(alias):
    alias_data = alias[1]
    return alias_data[4]

def alias_set_buy_offer_owner(alias, buy_offer_owner):
    alias_data = alias[1]
    alias_data[4] = buy_offer_owner

def alias_get_buy_offer_price(alias):
    alias_data = alias[1]
    return alias_data[5]

def alias_set_buy_offer_price(alias, buy_offer_price):
    alias_data = alias[1]
    alias_data[5] = buy_offer_price

def alias_get_buy_offer_expiration(alias):
    alias_data = alias[1]
    return alias_data[6]

def alias_set_buy_offer_expiration(alias, buy_offer_expiration):
    alias_data = alias[1]
    alias_data[6] = buy_offer_expiration

def alias_get_buy_offer_target(alias):
    alias_data = alias[1]
    return alias_data[7]

def alias_set_buy_offer_target(alias, buy_offer_target):
    alias_data = alias[1]
    alias_data[7] = buy_offer_target

def alias_get_for_sale(alias):
    alias_data = alias[1]
    return alias_data[8]

def alias_set_for_sale(alias, for_sale):
    alias_data = alias[1]
    alias_data[8] = for_sale

def alias_get_sell_offer_price(alias):
    alias_data = alias[1]
    return alias_data[9]

def alias_set_sell_offer_price(alias, sell_offer_price):
    alias_data = alias[1]
    alias_data[9] = sell_offer_price

#endregion alias_data

def alias_get_data(alias):
    data = alias[1]
    return data

def alias_is_valid(alias):
    """
    :returns True if alias is valid:
    """
    name_valid = alias_name_valid(alias)
    target_valid = alias_target_valid(alias)
    if name_valid and target_valid:
        return True
    return False

def alias_expired(alias):
    """
    : returns True if alias already expired:
    May be expired but not available for registrations, because of defined reservation
    """
    # if NEO accs free of charge
    # NEO account never expire, can be only sold
    free = storage_load(b'non_expirable_accs')
    if free and alias_get_type(alias) == 4:
        return False
    expiration = alias_get_expiration(alias)
    return expiration < get_header_timestamp()

def alias_available_for_registration(alias):
    """
    :returns true if alias is available for registration:
    Based on expiration of alias
    """
    owner = alias_get_owner(alias)
    for_sale = alias_get_for_sale(alias)
    if for_sale or CheckWitness(owner):
        alias_reservation = 0
    else:
        hard_coded_minimum = 0  # prevent negative reservation
        alias_reservation = storage_load(b'res_dur')
        if not alias_reservation or alias_reservation < hard_coded_minimum:
            alias_reservation = hard_coded_minimum


    expiration = alias_get_expiration(alias)
    end = expiration + alias_reservation
    timestamp = get_header_timestamp()
    
    free = storage_load(b'non_expirable_accs')
    if free and alias_get_type(alias) == 4:
        return False

    if end > timestamp:
        return False
    return True

def alias_name_valid(alias):
    """
    :returns true if name is valid for this alias type:
    """

    # Asset alias name format: "NEO, NAS, etc." (up to 4 characters)
    name = alias_get_name(alias)
    alias_type = alias_get_type(alias)
    if alias_type == 3 and len(name) > 4:
        return False
    # Account alias format string "NEO000000000001" (requires NEO Prefix)
    if alias_type == 4:
        acc = name
        acc_prefix = acc[0:3] 
        l = len(acc)
        if acc_prefix != "NEO" or l != 11:# prefix + 64-bit unsigned integer (8 bytes)
            return False
    return True

def alias_target_valid(alias):
    """
    :return True if target is valid for given alias type:
    """
    #if alias_type == 1 and len(alias.target) != 20:  # Adress - 20 bytes
    #    return False
    alias_type = alias_get_type(alias)
    target = alias_get_target(alias)
    if alias_type == 2 and len(target) != 20:  # ScriptHash - 20 bytes
        return False
    if alias_type == 3 and len(target) != 32:  # Aset symbol pointing to Asset Id - 32 bytes
        return False
    if alias_type == 4 and len(target) != 20:  # Account pointing to contract adress - 20 bytes
        return False
    return True

def alias_get_prefix(alias):
    """
    :returns alias type prefix for storing in storage:
    """
    #if alias_type == 1:  # Adress - 20 bytes # will be implemented later
    #    prefix = "adr_"
    alias_type = alias_get_type(alias)
    if alias_type == 2:  # ScriptHash - 20 bytes
        prefix = "sc_"
    elif alias_type == 3:  # Asset Id - 32 bytes
        prefix = "ast_"
    elif alias_type == 4:  # Account string NEO000000000001
        prefix = "acc_"
    else:  # all others is general
        prefix = "gen_"
    return prefix

def alias_save(alias):
    """
    Saves alias to storage
    """
    name = alias_get_name(alias)
    prefix = alias_get_prefix(alias)
    data = alias_get_data(alias)
    to_save = serialize_array(data)
    key = concat(prefix, name)
    dummy = storage_save(key, to_save)
    return True

def alias_exists(alias):  # just for better readability
    """
    :returns True if alias exists:
    it is based on ability to load alias
    """
    return alias_in_storage(alias)

def alias_in_storage(alias):
    """
    :returns True if alias inStorage:
    it is based on ability to load alias
    """
    name = alias_get_name(alias)
    prefix = alias_get_prefix(alias)
    key = concat(prefix, name)
    serialized = storage_load(key)
    if serialized:
        return True
    return False

def alias_delete(alias):
    """
    Removes alias
    """
    name = alias_get_name(alias)
    prefix = alias_get_prefix(alias)
    key = concat(prefix, name)
    dummy = storage_delete(key)

def alias_load(alias):
    """
    :param alias::: Alias:
    \n:returns alias::: Alias:
    \nLoads alias from storage, based on alias.name and alias.atype.load_alias
    """
    name = alias_get_name(alias)
    prefix = alias_get_prefix(alias)
    key = concat(prefix, name)
    
    serialized = storage_load(key)
    if serialized:
        deserialized = deserialize_bytearray(serialized)
        dummy = alias_set_target(alias, deserialized[0])
        dummy = alias_set_owner(alias, deserialized[1])
        dummy = alias_set_expiration(alias, deserialized[2])
        dummy = alias_set_owner_since(alias, deserialized[3])

        dummy = alias_set_buy_offer_owner(alias, deserialized[4])
        dummy = alias_set_buy_offer_price(alias, deserialized[5])
        dummy = alias_set_buy_offer_expiration(alias, deserialized[6])
        dummy = alias_set_buy_offer_target(alias, deserialized[7])

        dummy = alias_set_for_sale(alias, deserialized[8])
        dummy = alias_set_sell_offer_price(alias, deserialized[9])
    return alias