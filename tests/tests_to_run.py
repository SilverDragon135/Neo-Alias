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

# NEP5 test

    [ [10000], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '02', 'True', 'False', 'balanceOf','["ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM"]']],


    [ [b'Neo Alias Coin'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'name','[]']],

    [ [b'NAC'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'symbol','[]']],

    [ [8], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '02', 'True', 'False', 'decimals','[]']],

    [ [100000000000000000], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '02', 'True', 'False', 'totalSupply','[]']],

# end NEP5 test

# NA - register test

    [  [b'You can register alias only for yourself.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_register', '["'+test_neo_acc+'","AZ2YnqDxPffU2bRtkh1eod19QJ3uho5bTD",4,"ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",1519912704]']],


    [  [bytearray(b'This alias cannot be registered. Invalid name or target property for given alias_type.')], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_register', '["'+test_neo_acc+'a","ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",4,"ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",1519912704]']],


    [  [ b'You provided already expired alias_expiraton.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_register', '["'+test_neo_acc+'","ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",2,"ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",1300000000]']],


    [  [ b'Alias registred: '+ str.encode(test_neo_acc)], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_register', '["'+test_neo_acc+'","ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",4,"ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",1300000000]']],


    [  [b'Alias is already in use. You can submit buy offer if you are interested.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_register', '["'+test_neo_acc+'","ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",4,"ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",1519912704]']],

#end NA - register test

# NA - querty test

    [  [bytearray(b'x\xc50\xe2V\xef\x8c\xd6\x0b\xf4+\x0f\xb9\x02\xe8\x9eFQ\xc7\xb7')], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_query', '["'+test_neo_acc+'",4]']],


    [  [b'Alias '+str.encode(test_neo_acc)+str.encode('a not found or expired.')], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_query', '["'+test_neo_acc+'a",4]']],

# end NA - querty test

    ]

