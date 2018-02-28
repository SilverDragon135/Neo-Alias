"""
tests_to_run - contains tests to run
\ntests are returned trough get_tests()
\ntests are specified in format [ [expected_result1, expected_result2, ...], [arguments]]
"""
import time
from configuration.private import path_to_avm

timestamp = round(time.time())
# We need this, because the register test would fail with static acc in the subsequent tests
test_neo_acc = 'NEO' + str(round(time.time()))

def get_tests() -> []:
    return [

    [ [b'NASC initialized.', b'Uknown operation'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'init','[]']],

    [ [10000], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '02', 'True', 'False', 'balanceOf','["ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM"]']],

    [ [ b'Alias registred: '+ str.encode(test_neo_acc) ], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_register', '["'+test_neo_acc+'","ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",4,"ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",1519912704]']],

    [  [b'Alias is already in use. You can submit buy offer if you are interested.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_register', '["'+test_neo_acc+'","ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",4,"ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",1519912704]']],

    ]

