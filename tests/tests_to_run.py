"""
tests_to_run - contains tests to run
\ntests are returned trough get_tests()
\ntests are specified in format [ [expected_result1, expected_result2, ...], [arguments]]
"""
import time
from configuration.private import path_to_avm

timestamp = round(time.time())
# We need this, because the register test would fail with static acc in the subsequent tests
test_neo_acc = 'NEO'+ str(timestamp)[-8:]

def get_tests() -> []:
    return [

    [ [b'NASC initialized.', b'Uknown operation'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'init','[]']],

#region NEP5 test

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

    [ [b'Transfer completed.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'transfer','["ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM", "AZRtyq1woyVP8va9uReGM3tsp7YtX33Nrw", 20]'],],

    [ [b'Spender can withdraw (from your address): \x14'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'approve','["ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM", "AZRtyq1woyVP8va9uReGM3tsp7YtX33Nrw", 20]'],],

    [ [b'Spender can withdraw: \x14'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'allowance','["ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM", "AZRtyq1woyVP8va9uReGM3tsp7YtX33Nrw"]'],],

    [ [b'Transfer completed.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'transferFrom','["AZRtyq1woyVP8va9uReGM3tsp7YtX33Nrw", "ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM", "AZRtyq1woyVP8va9uReGM3tsp7YtX33Nrw", 20]'],
    1 ],

    [ [40], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '02', 'True', 'False', 'balanceOf','["AZRtyq1woyVP8va9uReGM3tsp7YtX33Nrw"]']],

    # only to keep test consistency
    [ [b'Transfer completed.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'transfer','["AZRtyq1woyVP8va9uReGM3tsp7YtX33Nrw", "ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM", 40]'],
    1 ], # wallet id

#endregion

#region NA - register test

    [  [b'You can register alias only for yourself.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_register', '["'+test_neo_acc+'","AZ2YnqDxPffU2bRtkh1eod19QJ3uho5bTD",4,"ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",1519912704]']],

    [  [b'You can register alias only for yourself.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_register', '["hello_world2","AZ2YnqDxPffU2bRtkh1eod19QJ3uho5bTD",2,b"\x92v9\x9e\xb7\xc2As\xc4\x03\xda\xd1\xd1\x8b\x1c\xf6\x1b9\xab\xac",1519912704]']],


    [  [bytearray(b'This alias cannot be registered. Invalid name or target property for given alias_type.')], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_register', '["'+test_neo_acc+'a","ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",4,"ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",1519912704]']],


    [  [ b'You provided already expired alias_expiraton.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_register', '["'+test_neo_acc+'","ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",2,"ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",1300000000]']],


    [  [ b'Alias registered: '+ str.encode(test_neo_acc)], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_register', '["'+test_neo_acc+'","ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",4,"ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",1300000000]']],


    [  [b'Alias is already in use. You can submit buy offer if you are interested.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_register', '["'+test_neo_acc+'","ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",4,"ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",1519912704]']],

#endregion NA - register test

#region NA - querty test

    [  [bytearray(b'x\xc50\xe2V\xef\x8c\xd6\x0b\xf4+\x0f\xb9\x02\xe8\x9eFQ\xc7\xb7')], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_query', '["'+test_neo_acc+'",4]']],


    [  [b'Alias '+str.encode(test_neo_acc)+b'a not found or expired.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_query', '["'+test_neo_acc+'a",4]']],

#endregion NA - querty test

#region NA - alias data
    
    [  [[bytearray(b'x\xc50\xe2V\xef\x8c\xd6\x0b\xf4+\x0f\xb9\x02\xe8\x9eFQ\xc7\xb7'), bytearray(b'x\xc50\xe2V\xef\x8c\xd6\x0b\xf4+\x0f\xb9\x02\xe8\x9eFQ\xc7\xb7'), bytearray(b'\x00m|M'), bytearray(b'e\xfc\x88W'), bytearray(b''), bytearray(b''), bytearray(b''), bytearray(b''), bytearray(b''), bytearray(b'')]], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '10', 'True', 'False', 'na_alias_data', '["'+test_neo_acc+'",4]']],


    [  [b'Alias '+str.encode(test_neo_acc)+str.encode('a not found or expired.')], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_alias_data', '["'+test_neo_acc+'a",4]']],
#endregion NA - alias data

#region NA - transfer
    [  [b'Alias '+str.encode(test_neo_acc)+b' transfered to: \xc1\xab\x0e\xce\x99\xdbA\xfcCM\xbb\x18\x13\xf2\x04\xea{\xf5z`'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_transfer', '["'+test_neo_acc+'","AZRtyq1woyVP8va9uReGM3tsp7YtX33Nrw",4]']],

    [  [b'You do not own this alias, so you cannot invoke transfer'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_transfer', '["'+test_neo_acc+'","AZRtyq1woyVP8va9uReGM3tsp7YtX33Nrw",4]']],

    [  [b'Alias '+str.encode(test_neo_acc)+b' transfered to: x\xc50\xe2V\xef\x8c\xd6\x0b\xf4+\x0f\xb9\x02\xe8\x9eFQ\xc7\xb7'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_transfer', '["'+test_neo_acc+'","ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",4]'],
    1 ],
#endregion NA - transfer

#region NA - update target 
    [  [b'Alias target updated: \xc1\xab\x0e\xce\x99\xdbA\xfcCM\xbb\x18\x13\xf2\x04\xea{\xf5z`'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_update_target', '["'+test_neo_acc+'","AZRtyq1woyVP8va9uReGM3tsp7YtX33Nrw",4]']],

    [  [bytearray(b'\xc1\xab\x0e\xce\x99\xdbA\xfcCM\xbb\x18\x13\xf2\x04\xea{\xf5z`')], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_query', '["'+test_neo_acc+'",4]']],
#endregion NA - update target 

#region NA - renew
    [  [b'Alias already payed for requested or maximum duration.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_renew', '["'+test_neo_acc+'","1519952704",4]']],

    [  [ b'Alias registered: '+ str.encode(test_neo_acc)], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_register', '["'+test_neo_acc+'","ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",0,"ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",1468895301]']],
                                                                                                                                                                          
    [  [b'Alias renew success. New expiration: \xe56\x92W'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_renew', '["'+test_neo_acc+'",1469200101,0]']],

    [  [[bytearray(b'x\xc50\xe2V\xef\x8c\xd6\x0b\xf4+\x0f\xb9\x02\xe8\x9eFQ\xc7\xb7'), bytearray(b'x\xc50\xe2V\xef\x8c\xd6\x0b\xf4+\x0f\xb9\x02\xe8\x9eFQ\xc7\xb7'), bytearray(b'\xe56\x92W'), bytearray(b'e\xfc\x88W'), bytearray(b''), bytearray(b''), bytearray(b''), bytearray(b''), bytearray(b''), bytearray(b'')]], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '10', 'True', 'False', 'na_alias_data', '["'+test_neo_acc+'",0]']],

#endregion NA - renew

#region NA - delete
    [  [b'Alias '+str.encode(test_neo_acc)+b' type \x04 deleted.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_delete', '["'+test_neo_acc+'",4]']],

    [  [b'Alias '+str.encode(test_neo_acc)+b' not found or expired.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_query', '["'+test_neo_acc+'",4]']],
#endregion NA - delete

#region NA - trading

    [  [b'Alias registered: custom_alias'+str.encode(test_neo_acc)], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_register', '["custom_alias'+test_neo_acc+'","AZRtyq1woyVP8va9uReGM3tsp7YtX33Nrw",0,"random_target",1519912704]'],
    1 ],

    [  [b'Put on sale.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_offer_sell', '["custom_alias'+test_neo_acc+'", 1000]'], 
    1 ],

    [  [[bytearray(b'random_target'), bytearray(b'\xc1\xab\x0e\xce\x99\xdbA\xfcCM\xbb\x18\x13\xf2\x04\xea{\xf5z`'), bytearray(b'\xe56\x92W'), bytearray(b'e\xfc\x88W'), bytearray(b''), bytearray(b''), bytearray(b''), bytearray(b''), bytearray(b'\x01'), bytearray(b'\xe8\x03')]], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '10', 'True', 'False', 'na_alias_data', '["custom_alias'+test_neo_acc+'"]']],

    [  [b'Sold.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_offer_buy', '["custom_alias'+test_neo_acc+'", "ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM", "new_target", 1500, 1519912704 ]']],

    [  [[bytearray(b'new_target'), bytearray(b'x\xc50\xe2V\xef\x8c\xd6\x0b\xf4+\x0f\xb9\x02\xe8\x9eFQ\xc7\xb7'), bytearray(b'\xe56\x92W'), bytearray(b'e\xfc\x88W'), bytearray(b''), bytearray(b''), bytearray(b''), bytearray(b''), bytearray(b''), bytearray(b'')]], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '10', 'True', 'False', 'na_alias_data', '["custom_alias'+test_neo_acc+'"]']],

    [  [b'Alias custom_alias'+str.encode(test_neo_acc)+b' type  deleted.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_delete', '["custom_alias'+test_neo_acc+'"]'], 
    ],

    [ [b'Transfer completed.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'transfer','[ "AZRtyq1woyVP8va9uReGM3tsp7YtX33Nrw", "ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM", 1000]'],
    1 ],


#endregion NA - trading
    ]

