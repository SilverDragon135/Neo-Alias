import os
import time
from wrappers.test_invoke_contract import BuildAndRun, LoadAndRun, RunTestAndReturnResult, RunTestAndReturnResultWithRetryOnFailure
from configuration.private import path_to_root_script, path_to_avm, wallets
from wrappers.wallet import init_wallets
from wrappers.blockchain import init_blockchain
from tests_to_run import get_tests
from boa.compiler import Compiler
from neo.VM.InteropService import Array

#settings
build = False
#settings

def try_print_msg(msg):
    while True: # there is bug in OSError: raw write() returned invalid length
        try:
            print(msg)
            break
        except:
            continue

if build:
    #BuildAndRun(path_to_root_script,[])
    os.remove(path_to_avm)
    print("Bulding...")
    Compiler.load_and_save(path_to_root_script)

if not os.path.exists(path_to_avm):
    print("Cannot find AVM file")
    quit()

init_blockchain()
test_wallets = init_wallets(wallets)

print("Executing tests...")
tests = get_tests()
test_count = len(tests)
success_count = 0
test_index = 1
for test in tests:
    arguments = test[1]
    
    wallet_id = 0
    if len(test) > 2:
        wallet_id = test[2]    
    # sometimes it wont return result properly, so it is better to retry few times
    result = RunTestAndReturnResultWithRetryOnFailure(arguments,test_wallets[wallet_id],5)

    expected_results = test[0]
    success = False
    for expected_result in expected_results:
        if len(arguments) > 3 and arguments[3] == '10':
            # the result is in this case neo.VM.InteropService.Array
            # so we have to rebuild it to printable result :)
            result_list = []
            for item in result[0].GetArray():
                result_list.append(item.GetByteArray())
            result = result_list

        if result == expected_result:
            success_count += 1
            success = True
            break

    if success:
        msg = "Test n." + str(test_index) + " result (SUCCESS): " + str(result)
        try_print_msg(msg)
    else:
        msg="Test n." + str(test_index) + " result (FAILED): " + str(result)
        try_print_msg(msg)
    test_index += 1


for wallet in test_wallets:
    wallet.Close()

try_print_msg("=========================================================")
try_print_msg("Testing results (success/total): " + str(success_count) + "/" + str(test_count))
try_print_msg("=========================================================")
