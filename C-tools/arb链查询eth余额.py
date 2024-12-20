from web3 import Web3

# 配置Arbitrum链的Web3提供者（这里使用Infura节点）
infura_url = "https://arb1.arbitrum.io/rpc"  # Arbitrum主网的RPC URL
w3 = Web3(Web3.HTTPProvider(infura_url))

# 检查连接是否成功
if not w3.is_connected():
    print("无法连接到Arbitrum网络")
    exit()


addresses = [
'0x3dF3dEf911E87Ab4Db50885F66B815ea50d31725',

]


# 查询余额的函数
def get_balance(address):

    address = w3.to_checksum_address(address)
    if not w3.is_address(address):
        print(f"{address} 不是一个有效的地址")
        return None

    # 获取该地址的ETH余额（单位是wei，需要转换为ether）
    balance_wei = w3.eth.get_balance(address)
    balance_ether = w3.from_wei(balance_wei, 'ether')
    return balance_ether


# 查询每个地址的余额
for address in addresses:
    balance = get_balance(address)
    if balance is not None:
        print(f"地址 {address} 的余额为: {balance}")

    with open(f'arb.txt', 'a') as file:

        file.write("\n"f'{address} {balance} ')
