from neo.Implementations.Wallets.peewee.UserWallet import UserWallet
from neo.Wallets.utils import to_aes_key
from wrappers.blockchain import init_blockchain
from configuration.private import wallet_password, wallet_path
import os

def init_test() -> UserWallet:
    if not os.path.exists(wallet_path):
        print("Wallet file not found")
        quit()

    print("Opening wallet...")
    password_key = to_aes_key(wallet_password)
    Wallet = UserWallet.Open(wallet_path, password_key)

    print("Initializing blockchain...")
    init_blockchain()
    return Wallet