"""
Holds Alias structures

- it shows, how it ends coding if you try OOP, but compiler support is very small
"""


from nas.wrappers.storage import Storage
from boa.code.builtins import concat, list
from boa.blockchain.vm.Neo.Runtime import Notify, CheckWitness
from nas.configuration.Service import ServiceConfiguration
from nas.common.util import get_header_timestamp

class Alias():
    """
    Alias class stores all information of an alias and handles alias storage management.
    """
    atype = 0
    name = "alias"  # to translate by alias service
    _properties_count = 10
    target = b''
    owner = b''
    expiration = 0
    owner_since = 0
    buy_offer_owner = b''
    buy_offer_price = 0
    buy_offer_expiration = 0
    buy_offer_target = b''
    for_sale = False
    sell_offer_price = 0

    def get_data(self):
        data = [self.target, self.owner, self.expiration, self.owner_since, self.buy_offer_owner, self.buy_offer_price, self.buy_offer_expiration, self.buy_offer_target, self.for_sale, self.sell_offer_price]
        return data

    def is_valid(self):
        """
        :returns True if alias is valid:
        """
        name = self.name_valid()
        target = self.target_valid()
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
        configuration = ServiceConfiguration()
        if configuration.are_NEO_acc_free_of_charge() and self.atype == 4:
            return False
        expiration = self.expiration
        return expiration < get_header_timestamp()

    def available_for_registration(self):
        """
        :returns true if alias is available for registration:
        Based on expiration of alias
        """
        configuration = ServiceConfiguration()
        owner = self.owner
        for_sale = self.for_sale
        if for_sale or CheckWitness(owner):
            alias_reservation = 0
        else:
            alias_reservation = configuration.get_reservation_duration()
        expiration = self.expiration
        end = expiration + alias_reservation
        timestamp = get_header_timestamp()
        
        if configuration.are_NEO_acc_free_of_charge() and self.atype == 4:
            return False

        if end > timestamp:
            return False
        return True

    def name_valid(self):
        """
        :returns true if name is valid for this alias type:
        """
        # Asset alias name format: "NEO, NAS, etc." (up to 4 characters)
        if self.atype == 3 and len(self.name) > 4:
            return False
        # Account alias format string "NEO000000000001" (requires NEO Prefix)
        if self.atype == 4:
            acc = self.name
            acc_prefix = acc[0:3] 
            l = len(acc)
            if acc_prefix != "NEO":
                return False
            acc_number = acc[3:l] 
            l = len(acc_number)
            i = 1
            j = 0
            # this is only way I made it do, what I want :/
            # dont know why, but it didnt worked when I starte check from begining :/
            digit = acc_number[l-i:l-j]
            while digit and l-i >= 0:
                digit = acc_number[l-i:l-j]
                if digit < "0" or digit > "9":
                    return False
                i+=1
                j= i - 1
        return True

    def target_valid(self):
        """
        :return True if target is valid for given alias type:
        """
        alias_type = self.atype
        target = self.target
        #if alias_type == 1 and len(self.target) != 20:  # Adress - 20 bytes
        #    return False
        if alias_type == 2 and len(target) != 20:  # ScriptHash - 20 bytes
            return False
        if alias_type == 3 and len(target) != 32:  # Aset symbol pointing to Asset Id - 32 bytes
            return False
        if alias_type == 4 and len(target) != 20:  # Account pointing to contract adress - 20 bytes
            return False
        return True

    def get_prefix(self):
        """
        :returns alias type prefix for storing in storage:
        """
        #if alias_type == 1:  # Adress - 20 bytes # will be implemented later
        #    prefix = "adr_"
        if self.atype == 2:  # ScriptHash - 20 bytes
            prefix = "sc_"
        elif self.atype == 3:  # Asset Id - 32 bytes
            prefix = "ast_"
        elif self.atype == 4:  # Account string NEO000000000001
            prefix = "acc_"
        else:  # all others is general
            prefix = "gen_"
        return prefix

    def save(self):
        """
        Saves alias to storage
        """
        prefix = self.get_prefix()
        storage = Storage()
        data = self.get_data()
        to_save = storage.serialize_array(data)
        key = concat(prefix, self.name)
        storage.save(key, to_save)
        return True

    def exists(self):  # just for better readability
        """
        :returns True if alias exists:
        it is based on ability to load alias
        """
        result = self.in_storage()
        return result
    
    def in_storage(self):
        """
        :returns True if alias inStorage:
        it is based on ability to load alias
        """
        prefix = self.get_prefix()
        key = concat(prefix, self.name)
        storage = Storage()
        serialized = storage.load(key)
        if serialized:
            return True
        return False

    def delete(self):
        """
        Removes alias
        """
        prefix = self.get_prefix()
        key = concat(prefix, self.name)
        storage = Storage()
        storage.delete(key)

# At this point I was failing with load(self) method inside Alias class
# Seems like class methods cannot assign class properties
# Next method solved this, but since alias is not passed as reference we need to 
# return Alias class, what results to: alias = load_alias(alias) 
def load_alias(alias:Alias) -> Alias:
    """
    :param alias::: Alias:
    \n:returns alias::: Alias:
    \nLoads alias from storage, based on alias.name and alias.atype.load_alias
    """
    prefix = alias.get_prefix()
    key = concat(prefix, alias.name)
    storage = Storage()
    serialized = storage.load(key)
    if serialized:
        deserialized = storage.deserialize_bytearray(serialized)
        alias.target = deserialized[0]
        alias.owner = deserialized[1]
        alias.expiration = deserialized[2]
        alias.owner_since = deserialized[3]
        alias.buy_offer_owner = deserialized[4]
        alias.buy_offer_price = deserialized[5]
        alias.buy_offer_expiration = deserialized[6]
        alias.buy_offer_target = deserialized[7]
        alias.for_sale = deserialized[8]
        alias.sell_offer_price = deserialized[9]
    return alias