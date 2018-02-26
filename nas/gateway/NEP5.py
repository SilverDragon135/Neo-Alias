from boa.blockchain.vm.Neo.App import DynamicAppCall
from boa.blockchain.vm.Neo.Runtime import Notify, CheckWitness
from boa.blockchain.vm.Neo.Action import RegisterAction
from nas.core.base import query
from nas.configuration.tokenInfo import Token
from nas.common.Account import Account
from nas.common.util import list_slice

TransferEvent = RegisterAction('transfer', 'from', 'to', 'amount')
ApproveEvent = RegisterAction('approval', 'owner', 'spender', 'value')


class NEP5Gateway():

    def get_methods(self):
        """
        \nreturns NEP5 methods as array
        """
        methods = ['name', 'symbol', 'decimals', 'totalSupply', 'balanceOf', 'transfer', 'transferFrom', 'approve', 'allowance']
        return methods

    def dynamic_call_nep5(self, operation, args):
        """
        :param operation:
        :param args [ [alias_name, sub_nas],... ]:
        \n tryes to resolve alias_name in specified sub_nas and 
        passes invoke call to resolved alias_target
        """
        nargs = len(args)
        alias = args[0]
        sub_nas = None
        if alias and len(alias) > 1:
            sub_nas = alias[1]
        elif len(alias) == 0:
            Notify("Alias name not provided.")
            return False
        alias_name = alias[0]
        if not alias_name:
            Notify("Alias name not provided.")
            return False
        args = list_slice(args,1,nargs)
        to_invoke = query(alias_name, sub_nas, 2)  # script hash or asset id ?
        if to_invoke:
            return DynamicAppCall(to_invoke, operation, args)
        else:
            Notify("NEP5 DynamicAppCall failed.")
            return False

    def handle_NEP5_call(self, operation, args):
        """
        :param operation:
        :param args [...]:
        \nhandles 2 scenarios based on parameters call:
        \n - returns values for NAC token, if standard parameter count
        \n - passes NEP5 call to other asset based on added parameter(args[0]) [alias_name, sub_nas] 
        """
        nargs = len(args)
        NAC = Token()
        if operation == 'name':
            if nargs == 1:
                return self.dynamic_call_nep5(operation, args)
            else:
                # NAC token
                return NAC.name
        elif operation == 'decimals':
            if nargs == 1:
                return self.dynamic_call_nep5(operation, args)
            else:
                # NAC token 100 000 000 or 1 000 000 000, and 2 decimals ?
                return NAC.decimals

        elif operation == 'symbol':
            if nargs == 1:
                return self.dynamic_call_nep5(operation, args)
            else:
                # NAC (possibly NAT or NAG)
                return NAC.symbol

        arg_error = "Not enough arguments provided."

        if operation == 'totalSupply':
            if nargs == 1:
                return self.dynamic_call_nep5(operation, args)
            else:
                return NAC.total_supply

        elif operation == 'balanceOf':
            if nargs == 1:
                account = Account()
                account.address = args[0]
                if account.is_valid():
                    return account.available_assets()
            elif nargs == 2:
                return self.dynamic_call_nep5(operation, args)
            return arg_error

        elif operation == 'transfer':
            if nargs == 3:
                t_from = args[0]
                t_to = args[1]
                t_amount = args[2]
                return self.transfer(t_from, t_to, t_amount)
            elif nargs == 4:
                return self.dynamic_call_nep5(operation, args)
            return arg_error

        elif operation == 'transferFrom':
            if nargs == 3:
                t_from = args[0]
                t_to = args[1]
                t_amount = args[2]
                return self.transfer_from(t_from, t_to, t_amount)
            elif nargs == 4:
                return self.dynamic_call_nep5(operation, args)
            return arg_error

        elif operation == 'approve':
            if nargs == 3:
                t_owner = args[0]
                t_spender = args[1]
                t_amount = args[2]
                return self.approve(t_owner, t_spender, t_amount)
            elif nargs == 4:
                return self.dynamic_call_nep5(operation, args)
            return arg_error

        elif operation == 'allowance':
            if nargs == 2:
                t_owner = args[0]
                t_spender = args[1]
                return self.allowance(t_owner, t_spender)
            elif nargs == 3:
                return self.dynamic_call_nep5(operation, args)
            return arg_error

        return False

    def transfer(self, t_from, t_to, amount):
        """
        :param t_from:
        :param t_to:
        :param amount:
        \n:returns True on success and False if failed:
        \ntryes to transfer assets from one owner to another
        """
        if amount <= 0:
            return False
        from_acc = Account()
        from_acc.address = t_from
        to_acc = Account()
        to_acc.address = t_to
        if not from_acc.is_valid() or not to_acc.is_valid():
            Notify("One or both of accounts not valid")
            return False

        if CheckWitness(from_acc.address):
            if t_from == t_to:
                print("Transfer to self!")
                return True

            if from_acc.available_assets() < amount:
                print("Insufficient funds")
                return False

            from_acc.sub_available_assets(amount)
            to_acc.add_available_assets(amount)
            TransferEvent(t_from, t_to, amount)
            return True
        else:
            print("You can send only from your adress")
        return False

    def transfer_from(self, t_from, t_to, amount):
        """
        :param t_from:
        :param t_to:
        :param amount:
        \n:returns True on success and False if failed:
        \ntryes to withdraw assets from one owner to another
        """
        if amount <= 0:
            return False

        from_acc = Account()
        from_acc.address = t_from
        to_acc = Account()
        to_acc.address = t_to
        if not from_acc.is_valid() or not to_acc.is_valid():
            Notify("One or both of accounts not valid")
            return False

        available_to_to_addr = from_acc.approved_assets(to_acc)

        if available_to_to_addr < amount:
            print("Insufficient funds approved")
            return False

        if from_acc.available_assets() < amount:
            print("Insufficient tokens in from balance")
            return False

        from_acc.sub_available_assets(amount)
        to_acc.add_available_assets(amount)

        Notify("Transfer complete")

        from_acc.sub_approved_assets(to_acc, amount)
        TransferEvent(t_from, t_to, amount)
        return True

    def approve(self, t_owner, t_spender, amount):
        """
        :param t_owner:
        :param t_spender:
        :param amount:
        \n:returns True on success and False if failed:
        \ntryes to approve assets withdrawal for others
        """
        if not CheckWitness(t_owner):
            print("Incorrect permission")
            return False

        if amount < 0:
            print("Negative amount")
            return False

        from_acc = Account()
        from_acc.address = t_owner
        to_acc = Account()
        to_acc.address = t_spender
        if not from_acc.is_valid() or not to_acc.is_valid():
            Notify("One or both of accounts not valid")
            return False

        # cannot approve an amount that is
        # currently greater than the from balance
        if from_acc.available_assets() >= amount:
            from_acc.approve_assets(to_acc, amount)
            ApproveEvent(t_owner, t_spender, amount)
            return True
        return False

    def allowance(self, t_owner, t_spender):
        """
        :param t_owner:
        :param t_spender:
        :param amount:
        \n:returns assets aproved to withdraw by t_spender from t_owner:
        """
        from_acc = Account()
        from_acc.address = t_owner
        to_acc = Account()
        to_acc.address = t_spender
        if not from_acc.is_valid() or not to_acc.is_valid():
            Notify("One or both of accounts not valid")
            return False
        return from_acc.approved_assets(to_acc)
