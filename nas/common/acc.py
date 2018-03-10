"""
addressounts module - addressounts management
"""
from boa.builtins import concat

"""
Account class holds information about account for given public key and handles asset management for this account.
"""

def is_account_valid(address):
    """
    :returns True if adress is in valid format:
    """
    if len(address) == 20:
        return True
    else:
        return False

def available_account_assets(address):
    """
    :param address:
    \n:returns available assets:
    """
    if address:
        assets = storage_load(address)
        return assets
    return 0

def approve_account_assets(address, t_to, assets_to_approve):
    """
    :param t_to:
    :param assets_to_approve:
    \n:returns True on success:
    \nApproves assets to withdraw for another address.
    Another adress has to be in valid format.
    """
    approval_key = concat(address, t_to)
    dummy = storage_delete(approval_key)
    if assets_to_approve > 0:
        dummy = storage_save(approval_key, assets_to_approve)
    return True

def approved_account_assets(address, t_to):
    """
    :param t_to:
    \n:returns approved assets for given address:
    """
    approval_key = concat(address, t_to)
    return storage_load(approval_key)

def add_account_approved_assets(address, t_to, assets_to_approve):
    """
    :param t_to:
    :param assets_to_approve:
    \n:returns True on success:
    \nAdds assets_to_approve to approved assets
    """
    approval_key = concat(address, t_to)
    approved = approve_account_assets(address,t_to)
    dummy = storage_delete(approval_key)
    approved += assets_to_approve 
    dummy = storage_save(approval_key, approved)
    return True

def sub_account_approved_assets(address, t_to, assets_to_remove): 
    """
    :param t_to:
    :param assets_to_remove:
    \n:returns True on success:
    \nSubtracts assets_to_remove from approved assets
    """  
    approval_key = concat(address, t_to)
    approved = approved_account_assets(address, t_to)
    dummy = storage_delete(approval_key)
    assets_to_approve = approved - assets_to_remove
    if assets_to_approve > 0:
        dummy = storage_save(approval_key, assets_to_approve)
    return True

def update_account_available_assets(address, assets_to_store):
    """
    :param address:
    :param assets_to_store:
    Updates availabel assets for addressount
    """
    dummy = storage_delete(address)
    if assets_to_store and assets_to_store > 0:
        dummy = storage_save(address, assets_to_store)
    return True

def add_account_available_assets(address, assets_to_add):
    """
    :param assets_to_store:
    Adds assets_to_add to available assets
    """
    available = available_account_assets(address) 
    available = available + assets_to_add
    return update_account_available_assets(address,available)

def sub_account_available_assets(address, assets_to_remove):
    """
    :param assets_to_store:
    Substracts assets_to_remove from available assets
    """
    available = available_account_assets(address)  
    available = available - assets_to_remove
    return update_account_available_assets(address,available)
