"""
addressounts module - addressounts management
"""
from boa.code.builtins import concat
from nas.wrappers.storage import Storage


class Account():
    """
    Account class holds information about account for given public key and handles asset management for this account.
    """
    address = None

    def is_valid(self):
        """
        :returns True if adress is in valid format:
        """
        if len(self.address) == 20:
            return True
        else:
            return False

    def available_assets(self):
        """
        :param address:
        \n:returns available assets:
        """
        if self.address:
            storage = Storage()          
            assets = storage.load(self.address)
            return assets
        return 0

    def approve_assets(self, t_to, assets_to_approve):
        """
        :param t_to:
        :param assets_to_approve:
        \n:returns True on success:
        \nApproves assets to withdraw for another address.
        Another adress has to be in valid format.
        """
        address = self.address
        approval_key = concat(address, t_to)
        storage = Storage()
        storage.delete(approval_key)
        if assets_to_approve > 0:
            storage.save(approval_key, assets_to_approve)
        return True

    def approved_assets(self, t_to):
        """
        :param t_to:
        \n:returns approved assets for given address:
        """
        storage = Storage()
        address = self.address
        approval_key = concat(address, t_to)
        return storage.load(approval_key)

    def add_approved_assets(self, t_to, assets_to_approve):
        """
        :param t_to:
        :param assets_to_approve:
        \n:returns True on success:
        \nAdds assets_to_approve to approved assets
        """
        storage = Storage()
        address = self.address
        approval_key = concat(address, t_to)
        approved = self.approved_assets(t_to)
        storage.delete(approval_key)
        approved += assets_to_approve 
        storage.save(approval_key, approved)
        return True

    def sub_approved_assets(self, t_to, assets_to_remove): 
        """
        :param t_to:
        :param assets_to_remove:
        \n:returns True on success:
        \nSubtracts assets_to_remove from approved assets
        """  
        storage = Storage()
        address = self.address
        approval_key = concat(address, t_to)
        approved = self.approved_assets(t_to)
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
        storage = Storage()
        storage.delete(self.address)
        if assets_to_store and assets_to_store > 0:
            storage.save(self.address, assets_to_store)
        return True

    def add_available_assets(self, assets_to_add):
        """
        :param assets_to_store:
        Adds assets_to_add to available assets
        """
        available = self.available_assets() 
        available = available + assets_to_add
        return self.update_available_assets(available)

    def sub_available_assets(self, assets_to_remove):
        """
        :param assets_to_store:
        Substracts assets_to_remove from available assets
        """
        available = self.available_assets()    
        available = available - assets_to_remove
        return self.update_available_assets(available)
