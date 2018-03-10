from boa.interop.System.ExecutionEngine import GetExecutingScriptHash

def Main(operation, args):
    if operation =='sc_hash':
        return GetExecutingScriptHash()
    return 'hello world'