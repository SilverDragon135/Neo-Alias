
from boa.blockchain.vm.Neo.Blockchain import GetHeader, GetHeight
from boa.blockchain.vm.Neo.Header import GetTimestamp, GetNextConsensus, GetHash

def get_header_timestamp():
    """
    :returns current block timestamp:
    """
    height=GetHeight()
    header=GetHeader(height)
    return GetTimestamp(header)

def list_slice(array, start, stop):
    if array:
        nitems = len(array)
        if nitems < stop:
            stop = nitems
        if start < 0:
            start = 0 
        l = stop - start
        result = list(length = l)
        i = 0
        j = 0
        for item in array:
            if i >= start and i < stop:
                result[j]=item
                j+=1
            i+=1
        return result
    else:
        return None

def get_alias_prefix(alias_type):
    """
    :returns alias type prefix for storing in storage:
    """
    #if alias_type == 1:  # Adress - 20 bytes # will be implemented later
    #    temp_alias_type = "adr_"
    if alias_type == 2:  # ScriptHash - 20 bytes
        temp_alias_type = "sc_"
    elif alias_type == 3:  # Asset Id - 32 bytes
        temp_alias_type = "ast_"
    elif alias_type == 4:  # Account string NEO000000000001
        temp_alias_type = "acc_"
    else:  # all others is general
        temp_alias_type = "gen_"
    return temp_alias_type