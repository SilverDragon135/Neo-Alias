from neo.Implementations.Wallets.peewee.UserWallet import UserWallet
from neo.Wallets.utils import to_aes_key
import os

def init_wallets(wallets) -> []:
    result = []
    for wallet in wallets:
        path = wallet[0]
        password = wallet[1]
        if not os.path.exists(path):
            print("Wallet file not found")
            quit()
    
        #print("Opening wallet: " + path)
        password_key = to_aes_key(password)
        Wallet = UserWallet.Open(path, password_key)
        result.append(Wallet)

    return result