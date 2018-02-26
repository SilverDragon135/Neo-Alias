"""
addressounts module - addressounts management
"""
from boa.code.builtins import concat
from nas.wrappers.storage import Storage
from nas.configuration.NeoAlias import NeoAliasConfiguration


class Account():
    """
    Account class holds information about account for given public key and handles asset management for this account.
    """
    address = None

    def is_valid(self):
        if len(self.address) == 20:
            return True
        else:
            return False

    def available_assets(self):
        """
        :param address:
        :returns asset count:
        """
        # if NEP5:
        #    return self.storage.load(address)
        alias_available_assets_key = self.asset_key()
        if alias_available_assets_key:
            storage = Storage()          
            assets = storage.load(alias_available_assets_key)
            return assets
        return 0

    def approve_assets(self, address, assets_to_approve):
        approval_key = concat(self.address, address)
        storage = Storage()
        storage.delete(approval_key)
        if assets_to_approve > 0:
            storage.save(approval_key, assets_to_approve)
        return True

    def approved_assets(self, address):
        storage = Storage()
        approval_key = concat(self.address, address)
        return storage.load(approval_key)

    def add_approved_assets(self, address, assets_to_approve):
        storage = Storage()
        approval_key = concat(self.address, address)
        approved = self.approved_assets(address)
        storage.delete(approval_key)
        approved += assets_to_approve 
        storage.save(approval_key, approved)
        return True

    def sub_approved_assets(self, address, assets_to_remove):   
        storage = Storage()
        approval_key = concat(self.address, address)
        approved = self.approved_assets(address)
        storage.delete(approval_key)
        assets_to_approve = approved - assets_to_remove
        if assets_to_approve > 0:
            storage.save(approval_key, assets_to_approve)
        return True

    def update_available_assets(self, assets_to_store):
        """
        :param address:
        :param assets_to_store:
        Updates availabel assets for addressount
        """
        # if NEP5:
        #    self.storage.delete(address)
        #    self.storage.save(address, assets_to_store)
        #    return True  
        storage = Storage()
        alias_available_assets_key = self.asset_key()
        storage.delete(alias_available_assets_key)
        if assets_to_store and assets_to_store > 0:
            storage.save(alias_available_assets_key, assets_to_store)
        return True

    def add_available_assets(self, assets):

        # if NEP5:
        #    available = self.available_assets() 
        #    return self.update_available_assets(available + assets) 
        available = self.available_assets()    
        available = available + assets
        return self.update_available_assets(available)

    def sub_available_assets(self, assets):
        # if NEP5:
        #    available = self.available_assets() 
        #    return self.update_available_assets(available - assets) 
        available = self.available_assets()    
        available = available - assets
        return self.update_available_assets(available)

    def asset_key(self):
        """
        :param adress:
        \n:param type_of_key:
        \n:returns generated storage key:
        """
        # will be removed in NEP5 implementation
        configuration = NeoAliasConfiguration()
        addr = self.address
        return concat(configuration.primary_asset_id, addr)
