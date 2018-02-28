"""
Fee Pool module - handling stored fees
"""
from boa.blockchain.vm.Neo.Runtime import Notify, CheckWitness
from boa.blockchain.vm.Neo.Action import RegisterAction
from nas.configuration.Administration import AdminConfiguration
from nas.wrappers.storage import Storage

CollectedFeesChangedEvent = RegisterAction('collectedFeesChanged', 'total_collected')

class FeesPool:
    """
    Its fee pool implementation.
    \n: - takes care of collecting fees:
    \n: - takes care of redistributing fees to stakers:
    \n staking not yet implemented
    """      

    def get_collected_fees(self):
        """
        :returns total of collected fees (not redistributed):
        """
        storage = Storage()
        collected = storage.load("collected_fees_in_pool")
        return collected

    def add_fee_to_pool(self, to_add):
        """
        :parama to_add:
        \nadds fees to pool
        """
        # I guess compiler messes with datatypes badly,
        # because 0 is here > 0 ?!
        if to_add > 0:# and to_add != 0:
            collected_fees_in_pool = self.get_collected_fees()
            if not collected_fees_in_pool:
                collected_fees_in_pool = 0
            collected_fees_in_pool += to_add
            storage = Storage()
            storage.save("collected_fees_in_pool", collected_fees_in_pool)
            CollectedFeesChangedEvent(collected_fees_in_pool)
            msg = ["Fee added to pool",to_add]
            Notify(msg)
        return True
