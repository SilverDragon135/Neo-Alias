"""
tests_to_run - contains tests to run
\ntests are returned trough get_tests()
\ntests are specified in format [ [expected_result1, expected_result2, ...], [arguments]]
"""
import time
from configuration.private import path_to_avm

timestamp = round(time.time())
# We need this, because the register test would fail with static acc in the subsequent tests
test_neo_acc1 = 'NEO' + str(round(time.time()))
test_neo_acc2 = 'NEO' + str(round(time.time())+10)

def get_smart_tests() -> []:
    return [
    [ [b'NASC initialized.', b'Uknown operation'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'init','[]']],

    [  [ b'Alias registered: '+ str.encode(test_neo_acc1)], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_register', '["'+test_neo_acc1+'","ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",4,"ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",1300000000]']],

    [ [10000], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '02', 'True', 'False', 'smart_balanceOf','["'+test_neo_acc1+'"]']],

    [  [ b'Alias registered: '+ str.encode(test_neo_acc2)], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_register', '["'+test_neo_acc2+'","AZRtyq1woyVP8va9uReGM3tsp7YtX33Nrw",4,"AZRtyq1woyVP8va9uReGM3tsp7YtX33Nrw",1300000000]'],
    1 ],

    [ [b'Transfer completed.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'smart_transfer','["'+test_neo_acc1+'", "'+test_neo_acc2+'", 500]']],

    [ [500], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '02', 'True', 'False', 'smart_balanceOf','["'+test_neo_acc2+'"]']],

    [ [b'Transfer completed.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'smart_transfer','["'+test_neo_acc2+'", "'+test_neo_acc1+'", 500]'],
    1 ],

    [ [b'Spender can withdraw (from your address): 2'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'smart_approve','["'+test_neo_acc1+'", "'+test_neo_acc2+'", 50]'],],

    [ [b'Spender can withdraw: 2'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'smart_allowance','["'+test_neo_acc1+'", "'+test_neo_acc2+'"]'],],

    [ [b'Transfer completed.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'smart_transferFrom','["'+test_neo_acc2+'", "'+test_neo_acc1+'", "'+test_neo_acc2+'", 50]'],
    1 ],

    [ [50], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '02', 'True', 'False', 'smart_balanceOf','["'+test_neo_acc2+'"]']],

    [ [b'Transfer completed.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'smart_transfer','["'+test_neo_acc2+'", "'+test_neo_acc1+'", 50]'],
    1],

    ]
