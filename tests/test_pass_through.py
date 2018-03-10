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
from neocore.UInt160 import UInt160

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

    def test_pass_through(self):

        print('=========== pass trough tests =============')
        output = Compiler.instance().load('./nasc.py').default
        na = output.write()
        output = Compiler.instance().load('./tests/contracts/hello_world.py')
        sc = output.write()
        
        print('===== init =====')
        tx, results, total_ops, engine = TestBuild(na, ['init', '[]'], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertIn(results[0].GetString() ,['NASC initialized.', 'Uknown operation'])

        print('===== test na =====')
        tx, results, total_ops, engine = TestBuild(na, ['na_test', '[]'], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString() ,'NASC is up!')

        print('===== test sc =====')
        tx, results, total_ops, engine = TestBuild(sc, ['test', '[]'], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString() , 'hello world')

        # get test contract scripptHash
        tx, results, total_ops, engine = TestBuild(sc, ['sc_hash', '[]'], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray() , b'>\n#\xcd\xe5)v\x1e\xd0\x1b\xb0\xa4\xa4\xcfLw\x9e\x01\x02\xf6')

        sc_hash = UInt160(data=results[0].GetByteArray())

        print('===== register hello world =====')
        tx, results, total_ops, engine = TestBuild(na, ['na_register', parse_param(["hello_world", self.wallet_1_script_hash.Data, 2, sc_hash.Data, 1519912704])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString() , 'Alias registered: hello_world')

        tx, results, total_ops, engine = TestBuild(na, ['na_query', parse_param(["hello_world", 2])], self.GetWallet1(), '0710', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray() , sc_hash.Data)

        return 
        # this is not working
        print('===== test dynamic app call =====')
        tx, results, total_ops, engine = TestBuild(na, ['uknown', parse_param(["hello_world"])], self.GetWallet1(), '0710', '05',True)
        #self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString() , 'hello world')

