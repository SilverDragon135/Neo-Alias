from boa_test.tests.boa_test import BoaFixtureTest
from boa.compiler import Compiler
from neo.Core.TX.Transaction import Transaction
from neo.Prompt.Commands.BuildNRun import TestBuild
from neo.EventHub import events
from neo.SmartContract.SmartContractEvent import SmartContractEvent, NotifyEvent
from neo.Settings import settings
from neo.Prompt.Utils import parse_param
from neo.Core.FunctionCode import FunctionCode
from neocore.Fixed8 import Fixed8
from boa_test.example.demo.nex.token import *

import shutil
import os
import time

settings.USE_DEBUG_STORAGE = True
settings.DEBUG_STORAGE_PATH = './fixtures/debugstorage'

class TestContract(BoaFixtureTest):

    dispatched_events = []
    dispatched_logs = []

    @classmethod
    def tearDownClass(cls):
        super(BoaFixtureTest, cls).tearDownClass()

        try:
            if os.path.exists(settings.DEBUG_STORAGE_PATH):
                shutil.rmtree(settings.DEBUG_STORAGE_PATH)
        except Exception as e:
            print("couldn't remove debug storage %s " % e)

    @classmethod
    def setUpClass(cls):
        super(TestContract, cls).setUpClass()

        cls.dirname = '/'.join(os.path.abspath(__file__).split('/')[:-2])

        def on_notif(evt):
            print(evt)
            cls.dispatched_events.append(evt)
            print("dispatched events %s " % cls.dispatched_events)

        def on_log(evt):
            print(evt)
            cls.dispatched_logs.append(evt)
        events.on(SmartContractEvent.RUNTIME_NOTIFY, on_notif)
        events.on(SmartContractEvent.RUNTIME_LOG, on_log)

    def test_0_NEP5(self):

        print('=========== NEP5 =============')
        output = Compiler.instance().load('./nasc.py').default
        out = output.write()

        print('===== init =====')
        tx, results, total_ops, engine = TestBuild(out, ['init', '[]'], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertIn(results[0].GetString() ,['NASC initialized.', 'Uknown operation'])

        print('===== test =====')
        tx, results, total_ops, engine = TestBuild(out, ['na_test', '[]'], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString() ,'NASC is up!')

        print('===== balanceOf =====')
        tx, results, total_ops, engine = TestBuild(out, ['balanceOf', parse_param([self.wallet_1_script_hash.Data])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger() , 10000)

        print('===== name =====')
        tx, results, total_ops, engine = TestBuild(out, ['name', '[]'], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString() , 'Neo Alias Coin')

        print('===== decimals =====')
        tx, results, total_ops, engine = TestBuild(out, ['decimals', '[]'], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger() , 8)

        print('===== symbol =====')
        tx, results, total_ops, engine = TestBuild(out, ['symbol', '[]'], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString() , 'NAT')

        print('===== totalSupply =====')
        tx, results, total_ops, engine = TestBuild(out, ['totalSupply', '[]'], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger() , 1000000000 * 100000000 )
       
        print('===== transfer =====')
        tx, results, total_ops, engine = TestBuild(out, ['transfer', parse_param([self.wallet_1_script_hash.Data, self.wallet_3_script_hash.Data, 20])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString(), 'Transfer completed.')

        print('===== aprove =====')
        tx, results, total_ops, engine = TestBuild(out, ['approve', parse_param([self.wallet_1_script_hash.Data, self.wallet_3_script_hash.Data, 20])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'Spender can withdraw (from your address): \x14')

        print('===== allowance =====')
        tx, results, total_ops, engine = TestBuild(out, ['allowance', parse_param([self.wallet_1_script_hash.Data, self.wallet_3_script_hash.Data])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'Spender can withdraw: \x14')

        print('===== transfeFrom =====')
        tx, results, total_ops, engine = TestBuild(out, ['transferFrom', parse_param([self.wallet_3_script_hash.Data, self.wallet_1_script_hash.Data, self.wallet_3_script_hash.Data, 20])], self.GetWallet3(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString(), 'TransferFrom completed.')

        print('===== balanceOf =====')
        tx, results, total_ops, engine = TestBuild(out, ['balanceOf', parse_param([self.wallet_3_script_hash.Data])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger() , 40)

        tx, results, total_ops, engine = TestBuild(out, ['transfer', parse_param([self.wallet_3_script_hash.Data, self.wallet_1_script_hash.Data, 40])], self.GetWallet3(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString(), 'Transfer completed.')


    def test_1_NA(self):
        timestamp = round(time.time())
        test_neo_acc = 'NEO'+ str(timestamp)[-8:]
        test_neo_acc2 = 'NEO'+ str(timestamp-10000)[-8:]

        print('=========== NA =============')
        output = Compiler.instance().load('./nasc.py').default
        out = output.write()

        print('===== init =====')
        tx, results, total_ops, engine = TestBuild(out, ['init', '[]'], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertIn(results[0].GetString() ,['NASC initialized.', 'Uknown operation'])
        
        print('===== test =====')
        tx, results, total_ops, engine = TestBuild(out, ['na_test', '[]'], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString() ,'NASC is up!')

        #region na_register
        print('===== na_register =====')
        tx, results, total_ops, engine = TestBuild(out, ['na_register', parse_param([test_neo_acc, self.wallet_2_script_hash.Data, 4, self.wallet_1_script_hash.Data, 1519912704])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString() , 'You can register alias only for yourself.')

        tx, results, total_ops, engine = TestBuild(out, ['na_register', parse_param(["hello_world", self.wallet_2_script_hash.Data, 2, self.wallet_1_script_hash.Data, 1519912704])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString() , 'You can register alias only for yourself.')

        tx, results, total_ops, engine = TestBuild(out, ['na_register', parse_param([test_neo_acc+'a', self.wallet_1_script_hash.Data, 4, self.wallet_1_script_hash.Data, 1519912704])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString() , 'This alias cannot be registered. Invalid name or target property for given alias_type.')
  
        tx, results, total_ops, engine = TestBuild(out, ['na_register', parse_param([test_neo_acc, self.wallet_1_script_hash.Data, 0, self.wallet_1_script_hash.Data, 1300000000])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString() , 'You provided already expired alias_expiraton.')

        tx, results, total_ops, engine = TestBuild(out, ['na_register', parse_param([test_neo_acc, self.wallet_1_script_hash.Data, 4, self.wallet_1_script_hash.Data, 1519912704])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString() , 'Alias registered: '+ test_neo_acc)

        tx, results, total_ops, engine = TestBuild(out, ['na_register', parse_param([test_neo_acc, self.wallet_1_addr, 4, self.wallet_1_script_hash.Data, 1519912704])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString() , 'Alias is already in use. You can submit buy offer if you are interested.')
        print('===== end na_register =====')
        #endregion na_register
        
        print('===== na_query =====')
        tx, results, total_ops, engine = TestBuild(out, ['na_query', parse_param([test_neo_acc, 4])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray() , self.wallet_1_script_hash.Data)
        
        tx, results, total_ops, engine = TestBuild(out, ['na_query', parse_param([test_neo_acc+'a', 4])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString() , 'Alias '+test_neo_acc+'a not found or expired.')
        print('===== end na_query =====')

        print('===== na_alias_data =====')
        tx, results, total_ops, engine = TestBuild(out, ['na_alias_data', parse_param([test_neo_acc, 4])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        new_result = []
        for item in results[0].GetArray():
            new_result.append(item.GetByteArray())
        self.assertSequenceEqual(new_result , [b'S\xefB\xc8\xdf!^\xbeZ|z\xe8\x01\xcb\xc3\xac/\xacI)', b'S\xefB\xc8\xdf!^\xbeZ|z\xe8\x01\xcb\xc3\xac/\xacI)', b'\x80\x88{S', b'\x00NrS', b'', b'', b'', b'', b'', b''])

        tx, results, total_ops, engine = TestBuild(out, ['na_alias_data', parse_param([test_neo_acc+'a', 4])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString() , 'Alias '+test_neo_acc+'a not found or expired.')
        print('===== end na_alias_data =====')

        print('===== na_transfer =====')
        tx, results, total_ops, engine = TestBuild(out, ['na_transfer', parse_param([test_neo_acc, self.wallet_3_script_hash.Data, 4])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray() , b'Alias ' + str.encode(test_neo_acc)+b' transfered to: \xa6\xc5\x9d\xeb\xf0\xd7(\xbd\x14\x89\xcd\xb9\xd9{\xd1\x90\xcb\x0b\xdch')
        
        tx, results, total_ops, engine = TestBuild(out, ['na_transfer', parse_param([test_neo_acc, self.wallet_3_script_hash.Data, 4])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString() , 'You do not own this alias, so you cannot invoke transfer')
        
        tx, results, total_ops, engine = TestBuild(out, ['na_transfer', parse_param([test_neo_acc, self.wallet_1_script_hash.Data, 4])], self.GetWallet3(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray() , b'Alias ' + str.encode(test_neo_acc)+b' transfered to: S\xefB\xc8\xdf!^\xbeZ|z\xe8\x01\xcb\xc3\xac/\xacI)')
        print('===== end na_transfer =====')

        print('===== na_update_target =====')
        tx, results, total_ops, engine = TestBuild(out, ['na_update_target', parse_param([test_neo_acc, self.wallet_3_script_hash.Data, 4])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray() , b'Alias target updated: \xa6\xc5\x9d\xeb\xf0\xd7(\xbd\x14\x89\xcd\xb9\xd9{\xd1\x90\xcb\x0b\xdch')
        
        tx, results, total_ops, engine = TestBuild(out, ['na_query', parse_param([test_neo_acc, 4])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray() , b'\xa6\xc5\x9d\xeb\xf0\xd7(\xbd\x14\x89\xcd\xb9\xd9{\xd1\x90\xcb\x0b\xdch')
        print('===== end na_update_target =====')

        print('===== na_renew =====')
        tx, results, total_ops, engine = TestBuild(out, ['na_renew', parse_param([test_neo_acc, 1519952704, 4])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString() , 'Alias already payed for requested or maximum duration.')

        tx, results, total_ops, engine = TestBuild(out, ['na_register', parse_param([test_neo_acc2, self.wallet_1_script_hash.Data, 0, self.wallet_1_script_hash.Data, 1400010000])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString() , 'Alias registered: '+ test_neo_acc2)

        tx, results, total_ops, engine = TestBuild(out, ['na_renew', parse_param([test_neo_acc2, 1400020000, 0])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray() ,b'Alias renew success. New expiration:  \x9crS')

        tx, results, total_ops, engine = TestBuild(out, ['na_alias_data', parse_param([test_neo_acc, 4])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        new_result = []
        for item in results[0].GetArray():
            new_result.append(item.GetByteArray())
        print(new_result)
        self.assertSequenceEqual(new_result , [bytearray(b'\xa6\xc5\x9d\xeb\xf0\xd7(\xbd\x14\x89\xcd\xb9\xd9{\xd1\x90\xcb\x0b\xdch'), bytearray(b'S\xefB\xc8\xdf!^\xbeZ|z\xe8\x01\xcb\xc3\xac/\xacI)'), bytearray(b'\x80\x88{S'), bytearray(b'\x00NrS'), bytearray(b''), bytearray(b''), bytearray(b''), bytearray(b''), bytearray(b''), bytearray(b'')])
        print('===== end na_renew =====')

        print('===== na_delete =====')
        tx, results, total_ops, engine = TestBuild(out, ['na_delete', parse_param([test_neo_acc, 4])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray() , b'Alias '+str.encode(test_neo_acc)+b' type \x04 deleted.')
        
        tx, results, total_ops, engine = TestBuild(out, ['na_query', parse_param([test_neo_acc, 4])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray() , b'Alias '+str.encode(test_neo_acc)+b' not found or expired.')
        print('===== end na_delete =====')

    def test_2_SmartNEP5(self):

        timestamp = round(time.time())
        test_neo_acc = 'NEO'+ str(timestamp)[-8:]
        test_neo_acc2 = 'NEO'+ str(timestamp-10000)[-8:]

        print('=========== NA =============')
        output = Compiler.instance().load('./nasc.py').default
        out = output.write()

        print('===== init =====')
        tx, results, total_ops, engine = TestBuild(out, ['init', '[]'], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertIn(results[0].GetString() ,['NASC initialized.', 'Uknown operation'])
        
        print('===== test =====')
        tx, results, total_ops, engine = TestBuild(out, ['na_test', '[]'], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString() ,'NASC is up!')

        tx, results, total_ops, engine = TestBuild(out, ['na_register', parse_param([test_neo_acc, self.wallet_1_script_hash.Data, 4, self.wallet_1_script_hash.Data, 1519912704])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString() , 'Alias registered: '+ test_neo_acc)

        tx, results, total_ops, engine = TestBuild(out, ['smart_balanceOf', parse_param([test_neo_acc])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger() , 10000)

        tx, results, total_ops, engine = TestBuild(out, ['na_register', parse_param([test_neo_acc2, self.wallet_3_script_hash.Data, 4, self.wallet_3_script_hash.Data, 1519912704])], self.GetWallet3(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString() , 'Alias registered: '+ test_neo_acc2)

        print('===== transfer =====')
        tx, results, total_ops, engine = TestBuild(out, ['smart_transfer', parse_param([test_neo_acc, test_neo_acc2, 500])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString(), 'Transfer completed.')

        tx, results, total_ops, engine = TestBuild(out, ['smart_balanceOf', parse_param([test_neo_acc2])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger() , 500)

        print('===== aprove =====')
        tx, results, total_ops, engine = TestBuild(out, ['smart_approve', parse_param([test_neo_acc, test_neo_acc2, 50])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'Spender can withdraw (from your address): 2')

        print('===== allowance =====')
        tx, results, total_ops, engine = TestBuild(out, ['smart_allowance', parse_param([test_neo_acc, test_neo_acc2])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'Spender can withdraw: 2')

        print('===== transfeFrom =====')
        tx, results, total_ops, engine = TestBuild(out, ['smart_transferFrom', parse_param([test_neo_acc2, test_neo_acc, test_neo_acc2, 50])], self.GetWallet3(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString(), 'TransferFrom completed.')

        print('===== balanceOf =====')
        tx, results, total_ops, engine = TestBuild(out, ['smart_balanceOf', parse_param([test_neo_acc2])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger() , 550)
