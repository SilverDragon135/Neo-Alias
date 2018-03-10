from nas.common.fee_pool import add_fee_to_pool
from nas.config.service import get_fee_per_period, get_fee_period


def try_pay_holding_fee(owner, alias_type, duration_to_pay):
    """
    :param owner:
    :param alias_type:
    :param duration_to_pay:
    \n:returns True if success or False if failed:
    \nchecks if owner provided enough assets to hold alias and if so 
    adds fee to fee pool
    """

    # get fee info
    fee = get_fee_per_period(alias_type)
    fee_period = get_fee_period()

    # calculate to pay * 100000000 to handle decimals
    periods_to_pay = (duration_to_pay * 100000000) / fee_period
    to_pay = (periods_to_pay * fee) / 100000000

    # check if enough assets
    available_assets = available_account_assets(owner)


    if available_assets >= to_pay:
        # update account assets
        dummy = sub_account_available_assets(owner, to_pay)
    else:
        return False

    dummy = add_fee_to_pool(to_pay)
    return True
