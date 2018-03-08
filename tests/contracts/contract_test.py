path_to_avm = './tests/contracts/hello_world.avm'
path_to_avm2 = './NASC.avm'


def get_contract_tests() -> []:
    return [

    [ [b'hello world'], #expected result
    #arguments
    [ path_to_avm, 'test', '0710', '05', 'True', 'False', 'init','[]'] ],

    [ [b'hello world'], #expected result
    #arguments
    [ path_to_avm2, 'test', '0710', '05', 'True', 'True', 'init','[de044c0198aff952fadf58b7a434559b0988a682]'] ],

    ]