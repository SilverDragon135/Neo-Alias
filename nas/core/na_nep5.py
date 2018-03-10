from boa.interop.Neo.Runtime import Notify, CheckWitness
from boa.interop.Neo.Action import RegisterAction


TransferEvent = RegisterAction('transfer', 'from', 'to', 'amount')
ApproveEvent = RegisterAction('approval', 'owner', 'spender', 'value')


def balanceOf(address):
    if is_account_valid(address):
        return available_account_assets(address)
    
    msg = "Provided adresses are not in valid fromat (Expected length = 20)."
    Notify(msg)
    return return_value(0, msg)


def transfer(t_from, t_to, amount):
    """
    :param t_from:
    :param t_to:
    :param amount:
    \n:returns True on success and False if failed:
    \ntryes to transfer assets from one owner to another
    """
    if amount <= 0:
        msg = "Negative or zero amount."
        Notify(msg)
        return return_value(False, msg)

    if t_from == t_to:
        msg = "Sender and recipient are same!"
        Notify(msg)
        return return_value(False, msg)

    from_valid = is_account_valid(t_from)
    to_valid = is_account_valid(t_to)

    if not from_valid or not to_valid:
        msg = "Provided adresses are not in valid fromat (Expected length = 20)."
        Notify(msg)
        return return_value(False, msg)

    if not CheckWitness(t_from):
        msg = "Only owner can transfer!"
        Notify(msg)
        return return_value(False, msg)

    if available_account_assets(t_from) < amount:
        msg = "Insufficient funds"
        Notify(msg)
        return return_value(False, msg)

    dummy = sub_account_available_assets(t_from,amount)
    dummy = add_account_available_assets(t_to,amount)
    TransferEvent(t_from, t_to, amount)

    msg = "Transfer completed."
    Notify(msg)
    return return_value(True, msg)


def transfer_from(t_originator, t_from, t_to, amount):
    """
    :parma t_originator:
    :param t_from:
    :param t_to:
    :param amount:
    \n:returns True on success and False if failed:
    \ntryes to withdraw assets from one owner to another
    """
    if amount <= 0:
        msg = "Negative or zero amount."
        Notify(msg)
        return return_value(False, msg)

    from_valid = is_account_valid(t_from)
    to_valid = is_account_valid(t_to)
    originator_valid = is_account_valid(t_originator)

    if not from_valid or not to_valid or not originator_valid:
        msg = "Provided adresses are not in valid fromat (Expected length = 20)."
        Notify(msg)
        return return_value(False, msg)

    if t_from == t_to:
        msg = "Sender and recipient are same!"
        Notify(msg)
        return return_value(False, msg)

    if not CheckWitness(t_originator):
        msg = "Only originator can withdraw transferFrom!"
        Notify(msg)
        return return_value(False, msg)
    
    available_to_originator = approved_account_assets(t_from,t_originator)

    if available_to_originator < amount:
        msg = "Insufficient funds approved"
        Notify(msg)
        return return_value(False, msg)

    available_assets = available_account_assets(t_from)
    if available_assets < amount:
        msg = "Insufficient funds in from balance"
        Notify(msg)
        return return_value(False, msg)

    dummy = sub_account_available_assets(t_from, amount)
    dummy = sub_account_approved_assets(t_from, t_originator,amount)
    dummy = add_account_available_assets(t_to,amount)

    msg = "TransferFrom completed."
    Notify(msg)
    TransferEvent(t_from, t_to, amount)
    return return_value(True, msg)


def approve(t_owner, t_spender, amount):
    """
    :param t_owner:
    :param t_spender:
    :param amount:
    \n:returns True on success and False if failed:
    \ntryes to approve assets withdrawal for others
    """
    if amount <= 0:
        msg = "Negative amount."
        Notify(msg)
        return return_value(False, msg)

    if t_owner == t_spender:
        msg = "Owner and spender are same!"
        Notify(msg)
        return return_value(False, msg)

    if not CheckWitness(t_owner):
        msg = "Only owner can approve."
        Notify(msg)
        return return_value(False, msg)

    from_valid = is_account_valid(t_owner)
    to_valid = is_account_valid(t_spender)

    if not from_valid or not to_valid:
        msg = "Provided adresses are not in valid fromat (Expected length = 20)."
        Notify(msg)
        return return_value(False, msg)

    # cannot approve an amount that is
    # currently greater than the from balance
    available_assets = available_account_assets(t_owner)
    if available_assets >= amount:
        dummy = approve_account_assets(t_owner, t_spender,amount)
        ApproveEvent(t_owner, t_spender, amount)
        msg = concat("Spender can withdraw (from your address): ", amount)
        Notify(msg)
        return return_value(amount, msg)
    
    msg = "Not enough assets available."
    Notify(msg)
    return return_value(False, msg)


def allowance(t_owner, t_spender):
    """
    :param t_owner:
    :param t_spender:
    :param amount:
    \n:returns assets aproved to withdraw by t_spender from t_owner:
    """
    if t_owner == t_spender:
        msg = "Owner and spender are same!"
        Notify(msg)
        return return_value(False, msg)

    from_valid = is_account_valid(t_owner)
    to_valid = is_account_valid(t_spender)

    if not from_valid or not to_valid:
        msg = "Provided adresses are not in valid fromat (Expected length = 20)."
        Notify(msg)
        return return_value(False, msg)

    _allowance = approved_account_assets(t_owner, t_spender)
    msg = concat("Spender can withdraw: ", _allowance)
    Notify(msg)
    return return_value(_allowance, msg)
