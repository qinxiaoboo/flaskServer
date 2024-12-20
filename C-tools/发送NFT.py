import time
import random,requests,json
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.exceptions import ContractLogicError

# Arbitrum RPC URL
#arb_rpc_url = 'https://arb1.arbitrum.io/rpc'
arb_rpc_url = 'https://endpoints.omniatech.io/v1/arbitrum/one/public'

# 设置 NFT 合约地址（替换为你的合约地址）
nft_contract_address = Web3.to_checksum_address('0x830723f67Db87e2540Fc704F6878F8B14058154C')

# 设置多个发送者（转出方）钱包地址
sender_addresses = [
Web3.to_checksum_address("地址"),

]  # 添加更多发送地址

# 设置接收者（转入方）钱包地址
receiver_addresses = [


]

# 设置私钥（可以是多个发送方的私钥或分开管理）
private_keys = {

Web3.to_checksum_address("evm"): "私钥",


}  # 针对每个发送地址的私钥

# 创建 Web3 实例并连接到 Arbitrum 网络
w3 = Web3(Web3.HTTPProvider(arb_rpc_url))

# 适配 Web3 v6 的中间件注入方式
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# 获取 ERC-721 合约的 ABI
nft_abi = [
    {
        "constant": True,
        "inputs": [
            {
                "name": "owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "owner",
                "type": "address"
            },
            {
                "name": "index",
                "type": "uint256"
            }
        ],
        "name": "tokenOfOwnerByIndex",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "from",
                "type": "address"
            },
            {
                "name": "to",
                "type": "address"
            },
            {
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "safeTransferFrom",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# 创建 NFT 合约实例
nft_contract = w3.eth.contract(address=nft_contract_address, abi=nft_abi)


# 获取钱包地址拥有的 NFT 数量
def get_token_count(owner):
    return nft_contract.functions.balanceOf(owner).call()


# 获取钱包地址中持有的所有 token_id
def get_tokens_of_owner(owner):
    token_count = get_token_count(owner)
    tokens = []
    for index in range(token_count):
        token_id = nft_contract.functions.tokenOfOwnerByIndex(owner, index).call()
        tokens.append(token_id)
    return tokens


# 转账函数
def transfer_nft(from_address, to_address, token_id, private_key):
    # 构建交易
    nonce = w3.eth.get_transaction_count(from_address, 'pending')
    # 获取当前区块的baseFee
    latest_block = w3.eth.get_block('latest')
    block_gas_limit = latest_block['gasLimit']
    base_fee = latest_block['baseFeePerGas']

    print(f"Block Gas Limit: {block_gas_limit}, Base Fee: {base_fee}")

    # 设置maxPriorityFeePerGas（通常可以设置为较低值，例如1 gwei）
    max_priority_fee_per_gas = Web3.to_wei(0.02, 'gwei')  # 例如，设置为1 Gwei

    # 设置maxFeePerGas，确保其大于等于baseFee
    max_fee_per_gas = base_fee + max_priority_fee_per_gas + Web3.to_wei(0.02, 'gwei')

    gas_estimate = nft_contract.functions.safeTransferFrom(from_address, to_address, token_id).estimate_gas({
        'from': from_address,
        'nonce': nonce,
        'maxFeePerGas': max_fee_per_gas,
        'maxPriorityFeePerGas': max_priority_fee_per_gas,
    })
    print(f"Gas Estimate: {gas_estimate}")
    gas_limit = min(gas_estimate, block_gas_limit)

    transaction = nft_contract.functions.safeTransferFrom(from_address, to_address, token_id).build_transaction({
        'chainId': 42161,  # Arbitrum 主网链ID
        'gas': gas_limit,  # gas limit，根据实际情况调整
        'maxFeePerGas': max_fee_per_gas,
        'maxPriorityFeePerGas': max_priority_fee_per_gas,
        'nonce': nonce,
    })

    # 使用私钥签署交易
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

    # 发送交易并获取交易哈希
    try:
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"Transaction successful with hash: {txn_hash.hex()}")
        return txn_hash
    except ContractLogicError as e:
        print(f"Error during transaction: {str(e)}")
        return None


# 主函数
def main():
    a = 0
    for sender_address in sender_addresses:
        # 获取当前发送者钱包所有 NFT 的 token_id
        tokens = get_tokens_of_owner(sender_address)
        print(f"钱包 {sender_address} 持有的 token_id: {tokens}")

        if not tokens:
            print(f"钱包 {sender_address} 中没有NFT，无法进行转账。")
            continue

        # 选择一个 token_id 进行转账
        for i in tokens:
            token_id_to_transfer = i  # 这里选择第一个 token_id 进行转账
            print(f"选择的 token_id: {token_id_to_transfer}")

            # 获取当前发送者的私钥
            private_key = private_keys.get(sender_address)
            if not private_key:
                print(f"未找到私钥：{sender_address}，跳过转账。")
                continue

            # 调用转账函数
            txn_hash = transfer_nft(sender_address, receiver_addresses[a], token_id_to_transfer, private_key)


            if txn_hash:
                print(f"NFT 转账成功，交易哈希: {txn_hash.hex()}")
            else:
                print("转账失败。")
            if len(tokens) > 1:
                time.sleep(5)
        a += 1


if __name__ == '__main__':
    main()
