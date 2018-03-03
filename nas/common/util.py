
from boa.blockchain.vm.Neo.Blockchain import GetHeader, GetHeight
from boa.blockchain.vm.Neo.Header import GetTimestamp, GetNextConsensus, GetHash
from nas.configuration.Service import ServiceConfiguration

def get_header_timestamp():
    """
    :returns current block timestamp:
    """
    height=GetHeight()
    header=GetHeader(height)
    return GetTimestamp(header)

def list_slice(array, start, stop):
    """
    :param array:
    :param start:
    :param stop:
    \n:retuns sliced array:
    Since python compiler does not support slicing lists, this is really simple implementation. 
    """
    if array:
        nitems = len(array)
        if nitems < stop:
            stop = nitems
        if start < 0:
            start = 0 
        l = stop - start
        result = list(length = l)
        j = 0 
        for i in range(start,stop):
            item=array[i]
            result[j] = item
            j+=1
        return result
    else:
        return None

def return_value(non_debug, debug):
    """
    :param non_debug:
    :param debug:
    \n:returns one of parameters:
    \nBased on configuration.debug returns non_debug or debug parameter. 
    \nThanks to this we can see text messages as result in test environment and 
    non debug messages in mainnet
    """
    configuration = ServiceConfiguration()
    if configuration.debug:
        return debug
    else: 
        return non_debug
