from boa.blockchain.vm.Neo.Runtime import Notify, CheckWitness
from boa.blockchain.vm.Neo.Action import RegisterAction
from boa.code.builtins import concat
from nas.common.Account import Account
from nas.common.util import return_value

TransferEvent = RegisterAction('transfer', 'from', 'to', 'amount')
ApproveEvent = RegisterAction('approval', 'owner', 'spender', 'value')


def balanceOf(address):
    account = Account()
    account.address = address
    if account.is_valid():
        return account.available_assets()
    
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

    from_acc = Account()
    from_acc.address = t_from
    to_acc = Account()
    to_acc.address = t_to
    if not from_acc.is_valid() or not to_acc.is_valid():
        msg = "Provided adresses are not in valid fromat (Expected length = 20)."
        Notify(msg)
        return return_value(False, msg)

    if not CheckWitness(from_acc.address):
        msg = "Only owner can transfer!"
        Notify(msg)
        return return_value(False, msg)

    if from_acc.available_assets() < amount:
        msg = "Insufficient funds"
        Notify(msg)
        return return_value(False, msg)

    from_acc.sub_available_assets(amount)
    to_acc.add_available_assets(amount)
    TransferEvent(t_from, t_to, amount)
    
    msg = "Transfer completed."
    Notify(msg)
    return return_value(True, msg)


def transfer_from(t_from, t_to, amount):
    """
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

    from_acc = Account()
    from_acc.address = t_from
    to_acc = Account()
    to_acc.address = t_to
    if not from_acc.is_valid() or not to_acc.is_valid():
        msg = "Provided adresses are not in valid fromat (Expected length = 20)."
        Notify(msg)
        return return_value(False, msg)

    if t_from == t_to:
        msg = "Sender and recipient are same!"
        Notify(msg)
        return return_value(False, msg)

    if not CheckWitness(to_acc.address):
        msg = "Only owner of destination address can transferFrom!"
        Notify(msg)
        return return_value(False, msg)

    available_to_to_addr = from_acc.approved_assets(to_acc)

    if available_to_to_addr < amount:
        msg = "Insufficient funds approved"
        Notify(msg)
        return return_value(False, msg)

    if from_acc.available_assets() < amount:
        msg = "Insufficient funds in from balance"
        Notify(msg)
        return return_value(False, msg)

    from_acc.sub_available_assets(amount)
    from_acc.sub_approved_assets(to_acc, amount)
    to_acc.add_available_assets(amount)

    msg = "Transfer completed."
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

    from_acc = Account()
    from_acc.address = t_owner
    to_acc = Account()
    to_acc.address = t_spender
    if not from_acc.is_valid() or not to_acc.is_valid():
        msg = "Provided adresses are not in valid fromat (Expected length = 20)."
        Notify(msg)
        return return_value(False, msg)

    # cannot approve an amount that is
    # currently greater than the from balance
    if from_acc.available_assets() >= amount:
        from_acc.approve_assets(to_acc, amount)
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

    from_acc = Account()
    from_acc.address = t_owner
    to_acc = Account()
    to_acc.address = t_spender

    if not from_acc.is_valid() or not to_acc.is_valid():
        msg = "Provided adresses are not in valid fromat (Expected length = 20)."
        Notify(msg)
        return return_value(False, msg)

    _allowance = from_acc.approved_assets(to_acc)
    msg = concat("Spender can withdraw: ", _allowance)
    Notify(msg)
    return return_value(_allowance, msg)
