import os
import time
from wrappers.test_invoke_contract import BuildAndRun, LoadAndRun, RunTestAndReturnResult
from configuration.private import path_to_root_script, path_to_avm, wallets
from wrappers.wallet import init_wallets
from wrappers.blockchain import init_blockchain
from tests_to_run import get_tests
from boa.compiler import Compiler

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
    result = RunTestAndReturnResult(arguments,test_wallets[wallet_id])

    expected_results = test[0]
    success = False
    for expected_result in expected_results:
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

print("=========================================================")
print("Testing results (success/total): " + str(success_count) + "/" + str(test_count))
print("=========================================================")
