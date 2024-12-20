from web3 import Web3
from eth_account import Account

w3 = Web3(Web3.HTTPProvider("https://rpc.ankr.com/eth"))

def getPrivateBymnemonic(mnemonic):
    Account.enable_unaudited_hdwallet_features()
    account = Account.from_mnemonic(mnemonic)
    private_key = account.key.hex()
    address = account.address
    return f"{address},{private_key}"

if __name__ == '__main__':
    with open("zhujici" + '.csv', 'r') as f:
        res = [txt.strip() for txt in f.readlines()]
    for item in res:
        with open("private"+'.csv', 'a') as f:
            f.write(getPrivateBymnemonic(item)+"\n")


