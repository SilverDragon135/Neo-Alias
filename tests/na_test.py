import os
import time
from wrappers.test_invoke_contract import BuildAndRun, LoadAndRun, RunTestAndReturnResult
from configuration.private import path_to_root_script, path_to_avm
from wrappers.init import init_test
from tests_to_run import get_tests
from boa.compiler import Compiler

#settings
build = False
#settings

if build:
    #BuildAndRun(path_to_root_script,[])
    os.remove(path_to_avm)
    print("Bulding...")
    Compiler.load_and_save(path_to_root_script)

if not os.path.exists(path_to_avm):
    print("Cannot find AVM file")
    quit()

Wallet = init_test()

print("Executing tests...")
tests = get_tests()
test_count = len(tests)
success_count = 0
test_index = 1
for test in tests:
    arguments = test[1]
    result = RunTestAndReturnResult(arguments,Wallet)

    expected_results = test[0]
    success = False
    for expected_result in expected_results:
        if result == expected_result:
            msg = "Test n." + str(test_index) + " result (SUCCESS): " + str(result)
            print(msg)
            success_count += 1
            success = True
            break
    if not success: 
        msg="Test n." + str(test_index) + " result (FAILED): " + str(result)
        print(msg)
    test_index += 1


Wallet.Close()

print("=========================================================")
print("Testing results (success/total): " + str(success_count) + "/" + str(test_count))
print("=========================================================")
