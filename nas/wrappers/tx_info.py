from boa.blockchain.vm.System.ExecutionEngine import GetScriptContainer, GetExecutingScriptHash
from boa.blockchain.vm.Neo.Transaction import Transaction, GetReferences, GetOutputs, GetUnspentCoins
from boa.blockchain.vm.Neo.Output import GetValue, GetAssetId, GetScriptHash
from nas.configuration.Service import ServiceConfiguration

def gas_attached():
    """
    :returns gas attached to Tx:
    """
    configuration = ServiceConfiguration()
    tx = GetScriptContainer()  # type:Transaction
    references = tx.References
    receiver_addr = GetExecutingScriptHash()

    if len(references) > 0:
        sent_amount_gas = 0

        for output in tx.Outputs:
            if output.ScriptHash == receiver_addr and output.AssetId == configuration.primary_asset_id:
                sent_amount_gas += output.Value

        return sent_amount_gas
    return 0

    

