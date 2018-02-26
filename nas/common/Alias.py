"""
Holds Alias structures

- it shows, how it ends coding if you try OOP, but compiler support is very small
"""


from nas.wrappers.storage import Storage
from boa.code.builtins import concat, list, range
from boa.blockchain.vm.Neo.Runtime import Notify, CheckWitness
from nas.configuration.NeoAlias import NeoAliasConfiguration
from nas.common.util import get_header_timestamp, list_slice, get_alias_prefix

def get_alias_target(name,atype):
    prefix = get_alias_prefix(atype)
    key = concat(prefix, name)
    storage = Storage()
    serialized = storage.load(key)
    if serialized:
        deserialized = storage.deserialize_bytearray(serialized)
        target = deserialized[0]
        return target
    return None

def get_alias_data(name,atype):
    prefix = get_alias_prefix(atype)
    key = concat(prefix, name)
    storage = Storage()
    serialized = storage.load(key)
    if not serialized:
        return False
    deserialized = storage.deserialize_bytearray(serialized)
    return deserialized

class Alias():
    """
    Alias class stores all information of an alias and handles alias storage management.
    """
    atype = 0
    name = "alias"  # to translate by alias service
    _target = None
    _owner = None
    _expiration = 0
    _owner_since = 0
    _buy_offer_owner = None
    _buy_offer_price = 0
    _buy_offer_expiration = 0
    _buy_offer_target = None
    _is_for_sale = False
    _sell_offer_price = 0

    def get_data(self):
        prefix = get_alias_prefix(self.atype)
        key = concat(prefix, self.name)
        storage = Storage()
        serialized = storage.load(key)
        if not serialized:
            return False
        deserialized = storage.deserialize_bytearray(serialized)
        return deserialized

    def save_data(self, data):
        prefix = get_alias_prefix(self.atype)
        storage = Storage()
        to_save = storage.serialize_array(data)
        key = concat(prefix, self.name)
        storage.save(key, to_save)
        return True

    def target(self):
        data = self.get_data()
        if data:
            value = data[0]
            return value
        return None

    def owner(self):
        data = self.get_data()
        if data:
            value = data[1]
            return value
        return None

    def expiration(self):
        data = self.get_data()
        if data:
            value = data[2]
            return value
        return None

    def owner_since(self):
        data = self.get_data()
        if data:
            value = data[3]
            return value
        return None


    def buy_offer_owner(self):
        data = self.get_data()
        if data:
            value = data[4]
            return value
        return None

    def buy_offer_price(self):
        data = self.get_data()
        if data:
            value = data[5]
            return value
        return None

    def buy_offer_expiration(self):
        data = self.get_data()
        if data:
            value = data[6]
            return value
        return None

    def buy_offer_target(self):
        data = self.get_data()
        if data:
            value = data[7]
            return value
        return None

    def is_for_sale(self):
        data = self.get_data()
        if data:
            value = data[8]
            return value
        return None

    def sell_offer_price(self):
        data = self.get_data()
        if data:
            value = data[9]
            return value
        return None

    def is_valid(self):
        """
        :returns True if alias is valid:
        """
        name = self.is_name_valid()
        target = self.is_target_valid()
        if name and target:
            return True
        return False

    def expired(self):
        """
        : returns True if alias already expired:
        May be expired but not available for registrations, because of defined reservation
        """
        # if NEO accs free of charge
        # NEO account never expire, can be only sold
        configuration = NeoAliasConfiguration()
        if configuration.are_NEO_acc_free_of_chage() and self.atype == 4:
            return False
        expiration = self.expiration()
        return expiration < get_header_timestamp()

    def is_available_for_registration(self):
        """
        :returns true if alias is available for registration:
        Based on expiration of alias
        """
        exists = self.in_storage()
        if exists:
            configuration = NeoAliasConfiguration()
            data = self.get_data()
            if data:
                owner = data[1]
                is_for_sale = data[8]
                if is_for_sale or CheckWitness(owner):
                    alias_reservation = 0
                else:
                    alias_reservation = configuration.get_reservation_duration()
                expiration = data[2]
                end = expiration + alias_reservation
                timestamp = get_header_timestamp()
                if end > timestamp:
                    return False
        return True

    def is_name_valid(self):
        """
        :returns true if name is valid for this alias type:
        """
        target = self._target
        # Asset alias name format: "NEO, NAS, etc." (up to 4 characters)
        if self.atype == 3 and len(self.name) > 4:
            return False
        # Account alias format string "NEO000000000001" (requires NEO Prefix)
        if self.atype == 4:
            acc = target
            acc_prefix = list_slice(acc,0,3)
            l = len(acc)
            if acc_prefix != "NEO":
                return False
            number = list_slice(acc,3,l)
            for c in number:
                if c != "0" and c != "1" and c != "2" and c != "3" and c != "4" and \
                        c != "5" and c != "6" and c != "7" and c != "8" and c != "9":
                    return False
        return True

    def is_target_valid(self):
        """
        :return True if target is valid for given alias type:
        """
        alias_type = self.atype
        target = self._target
        #if alias_type == 1 and len(self.target) != 20:  # Adress - 20 bytes
        #    return False
        if alias_type == 2 and len(target) != 20:  # ScriptHash - 20 bytes
            return False
        if alias_type == 3 and len(target) != 32:  # Aset symbol pointing to Asset Id - 32 bytes
            return False
        if alias_type == 4 and len(target) != 20:   # Account pointing to contract adress - 20 bytes
            return False
        return True

    def get_prefix(self):
        """
        :returns alias type prefix for storing in storage:
        """
        prefix = get_alias_prefix(self.atype)
        return prefix

    def exists(self):  # just for better readability
        """
        :returns True if alias exists:
        it is based on ability to load alias
        """
        result = self.in_storage()
        return result

    def in_storage(self):
        prefix = self.get_prefix()
        key = concat(prefix, self.name)
        storage = Storage()
        serialized = storage.load(key)
        if serialized:
            return True
        return False

    def get_assigned_data(self):
        """
        : returns alias info as array:
        """
        data = [self._target, self._owner, self._expiration, self._owner_since, self._buy_offer_owner, self._buy_offer_price, self._buy_offer_expiration, self._buy_offer_target, self._is_for_sale, self._sell_offer_price]
        return data

    def save(self):
        """
        Saves alias
        """
        prefix = self.get_prefix()
        storage = Storage()
        key = concat(prefix, self.name)
        data = self.get_assigned_data()
        serialized = storage.serialize_array(data)
        storage.save(key, serialized)
        return key

    def delete(self):
        """
        Removes alias
        """
        prefix = self.get_prefix()
        key = concat(prefix, self.name)
        storage = Storage()
        storage.delete(key)

