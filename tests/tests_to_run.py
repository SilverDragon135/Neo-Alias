"""
tests_to_run - contains tests to run
\ntests are returned trough get_tests()
\ntests are specified in format [ [expected_result1, expected_result2, ...], [arguments]]
"""

from configuration.private import path_to_avm

def get_tests():
    return [
    
    [ [b'Alias registred: NEO546579'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_register', '["NEO546579","ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",4,"ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",1519912704]']],

    [  [b'Alias is already in use. You can submit buy offer if you are interested.'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'na_register', '["NEO546579","ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",4,"ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",1519912704]']],

    ]

