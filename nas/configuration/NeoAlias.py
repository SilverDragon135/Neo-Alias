"""
Module configuration - contains NA root configuration
"""
from boa.blockchain.vm.Neo.Runtime import Notify, CheckWitness
from boa.blockchain.vm.Neo.Action import RegisterAction
from nas.wrappers.storage import Storage
from nas.core.fee_pool import FeesPool
from nas.configuration.Administration import AdminConfiguration

ConfigurationUpdatedEvent = RegisterAction('configurationUpdated', 'option', 'value')


class NeoAliasConfiguration():
    """
    :Interface to access NEO Alias configuration:
    \n :Configuration will be determined based on voting mechanism, that will be implemented later:
    \n Final implementation will prevent centralized control and except init() method for initial
    setup, configuration is going to be controloble only trough voting
    """

    def init(self):
        """
        :Initializes dapp NASC:
        """
        configuration = AdminConfiguration()
        if not CheckWitness(configuration.root_admin):
            Notify("Only root_admin can initialize NASC.")
            return False
        storage = Storage()
        # initialize
        storage.save("NASC_initialized", True)
        Notify("NASC initialized.")

    def initialized(self):
        storage = Storage()
        return storage.load("NASC_initialized")


    def options(self):
        """
        : retruns available options to configure:
        """
        data = ["maximum_registration_duration", "free_maximum_registration_duration", "reservation_duration", "fee_per_period", "fee_period", "loyality_bonus_per_period", "loyality_bonus_period", "maximum_loyalty_bonus", "trade_commission", "non_expirable_free_of_charge_NEO_accounts"]
        return data

    # gas_id
    primary_asset_id = b'\xe7-(iy\xeel\xb1\xb7\xe6]\xfd\xdf\xb2\xe3\x84\x10\x0b\x8d\x14\x8ewX\xdeB\xe4\x16\x8bqy,`'

    # registration configuration

    def get_maximum_registration_duration(self, alias_type):
        """
        :param type:
        \n:returns maximum alias duration for given type:
        """
        keys = self.options()
        key = keys[0]
        key = concat(key, alias_type)
        hard_coded_minimum = 604800  # week
        storage = Storage()
        maximum_registration_duration = storage.load(key)
        if not maximum_registration_duration or maximum_registration_duration < hard_coded_minimum:
            return hard_coded_minimum
        else:
            return maximum_registration_duration

    def set_maximum_registration_duration(self, duration, alias_type):
        """
        :param duration:
        \n:param type:
        \nsets maximum alias registration duration for given type
        """
        keys = self.options()
        key = keys[0]
        key = concat(key, alias_type)
        storage = Storage()
        storage.delete(key)
        storage.save(key, duration)
        ConfigurationUpdatedEvent(key, duration)
        return True

    def get_reservation_duration(self):
        """
        :returns reservation duration:
        """
        hard_coded_minimum = 0  # prevent negative reservation
        storage = Storage()
        keys = self.options()
        key = keys[2]
        reservation_duration = storage.load(key)
        if not reservation_duration or reservation_duration < hard_coded_minimum:
            return hard_coded_minimum
        else:
            return reservation_duration

    def set_reservation_duration(self, duration):
        """
        :param duration:
        \nsets reservation duration
        """
        storage = Storage()
        keys = self.options()
        key = keys[2]
        storage.delete(key)
        storage.save(key, duration)
        ConfigurationUpdatedEvent(key, duration)
        return True
    # fee configuration

    def get_fee_per_period(self, alias_type):
        """
        :param type:
        \n:returns fee per period for given type:
        """
        storage = Storage()
        neo_accs_free_of_charge = self.are_NEO_acc_free_of_chage()
        if alias_type == 4 and neo_accs_free_of_charge:
            return 0
        keys = self.options()
        key = keys[3]
        key = concat(key, alias_type)
        hard_coded_minimum = 0  # prevent negative fee
        fee_per_period = storage.load(key)
        if not fee_per_period or fee_per_period < hard_coded_minimum:
            return hard_coded_minimum
        else:
            return fee_per_period

    def set_fee_per_period(self, fee, alias_type):
        """
        :param fee:
        \n:param type:
        \nsets fee per period for given type
        """
        storage = Storage()
        keys = self.options()
        key = keys[3]
        key = concat(key, alias_type)
        storage.delete(key)
        storage.save(key, fee)
        ConfigurationUpdatedEvent(key, fee)
        return True

    def get_fee_period(self):
        """
        :returns fee_period:
        """
        hard_coded_minimum = 86400  # minimum fee period can be 1 day
        storage = Storage()
        keys = self.options()
        key = keys[4]
        fee_period = storage.load(key)
        if not fee_period or fee_period < hard_coded_minimum:
            return hard_coded_minimum
        else:
            return fee_period

    def set_fee_period(self, period):
        """
        :param period:
        \nsets fee period
        """
        storage = Storage()
        keys = self.options()
        key = keys[4]
        storage.delete(key)
        storage.save(key, period)
        ConfigurationUpdatedEvent(key, period)
        return True

    # commissions
    def get_trade_commission(self):
        """
        :returns trade commission:
        """
        storage = Storage()
        hard_coded_minimum = 0  # prevent negative bonus
        hard_coded_maximum = 50
        keys = self.options()
        key = keys[8]
        trade_commission = storage.load(key)
        if not trade_commission or trade_commission < hard_coded_minimum:
            return hard_coded_minimum
        elif trade_commission > hard_coded_maximum:
            return hard_coded_maximum
        else:
            return trade_commission

    def set_trade_commission(self, trade_commission):
        """
        :param trade_commission:
        sets trade commission
        """
        storage = Storage()
        keys = self.options()
        key = keys[8]
        storage.delete(key)
        storage.save(key, trade_commission)
        ConfigurationUpdatedEvent(key, trade_commission)
        return True

    def are_NEO_acc_free_of_chage(self):
        """
        :returns True/False:
        \nmens NEO accs (NEO564522165) are free
        """
        storage = Storage()
        keys = self.options()
        key = keys[9]
        stored = storage.load(key)
        if not stored:
            return True
        return stored

    def set_are_NEO_acc_free_of_chage(self, free):
        """
        :param free:
        \nenalbles/disables free NEO accs (NEO564522165)
        """
        storage = Storage()
        keys = self.options()
        key = keys[9]
        storage.delete(key)
        storage.save(key,free)
        ConfigurationUpdatedEvent(key, free)
        return True