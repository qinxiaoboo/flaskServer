from web3 import Web3
import os
# Arbitrum 网络的 RPC URL（主网或测试网）
arb_rpc_url = 'https://arb1.arbitrum.io/rpc'
# 连接到 Arbitrum 网络
web3 = Web3(Web3.HTTPProvider(arb_rpc_url))
# 检查连接是否成功
if not web3.is_connected():
    print("无法连接到Arbitrum网络！")
    exit()
# 发送地址与私钥的对应关系
senders_and_private_keys = {

}
# 每个发送地址对应的接收地址
senders_and_receivers = {


}
# 确保地址是 checksum 格式
def to_checksum_address(address):
    return Web3.to_checksum_address(address)


# 估算 gas 费用
def estimate_gas_fee(from_address, to_address,value):
    # 获取当前区块的baseFee
    latest_block = web3.eth.get_block('latest')
    base_fee = latest_block['baseFeePerGas']
    # 设置maxPriorityFeePerGas（通常可以设置为较低值，例如1 gwei）
    max_priority_fee_per_gas = Web3.to_wei(1, 'gwei')  # 例如，设置为1 Gwei
    # 设置maxFeePerGas，确保其大于等于baseFee
    max_fee_per_gas = base_fee + max_priority_fee_per_gas

    # 构建交易数据
    transaction = {
        'from': from_address,
        'to': to_address,
        'value': value,
        'gas': 0,  # 简单转账的gas数量
        'maxFeePerGas': max_fee_per_gas,
        'maxPriorityFeePerGas': max_priority_fee_per_gas,
    }
    try:
        # 估算gas费用
        gas_estimate = web3.eth.estimate_gas(transaction)
        return gas_estimate, max_fee_per_gas, max_priority_fee_per_gas
    except Exception as e:
        print(f"估算gas费用时出错: {str(e)}")
        return 0, 0, 0

# 转账函数
def send_transaction(from_address, private_key, to_address):
    # 获取发送地址余额
    balance_in_wei = web3.eth.get_balance(from_address)

    # 估算gas费用
    gas_estimate, max_fee_per_gas, max_priority_fee_per_gas = estimate_gas_fee(from_address, to_address, balance_in_wei)

    # 如果估算失败，直接跳过
    if gas_estimate == 0:
        print(f"估算gas费用失败，跳过地址 {from_address}。")
        return

    # 确保余额大于gas费用
    if balance_in_wei <= gas_estimate:
        print(f"地址 {from_address} 的余额不足以支付手续费，跳过该地址。")
        return

    # 计算可转账的金额（扣除gas费用）
    amount_to_send = balance_in_wei - gas_estimate
    print(
        f"地址 {from_address} 当前余额：{web3.from_wei(balance_in_wei, 'ether')} ETH，准备转账：{web3.from_wei(amount_to_send, 'ether')} ETH")
    # 获取nonce
    nonce = web3.eth.get_transaction_count(from_address)
    # 构造交易
    transaction = {
        'to': to_address,
        'value': amount_to_send,  # 发送金额
        'gas': gas_estimate,  # 使用估算的gas
        'maxFeePerGas': max_fee_per_gas,  # 使用估算的maxFeePerGas
        'maxPriorityFeePerGas': max_priority_fee_per_gas,  # 使用估算的maxPriorityFeePerGas
        'nonce': nonce,  # nonce确保交易顺序
        'chainId': 42161  # Arbitrum 主网的chainId
    }

    # 使用私钥签名交易
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

    try:
        # 发送交易
        transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        print(f"从 {from_address} 向 {to_address} 转账已发送，交易哈希：{transaction_hash.hex()}")
    except Exception as e:
        print(f"发送交易时发生错误: {str(e)}")

for sender, private_key in senders_and_private_keys.items():
    receiver = senders_and_receivers.get(sender)
    sender = to_checksum_address(sender)
    if receiver:
        receiver = to_checksum_address(receiver)
        send_transaction(sender, private_key, receiver)
    else:
        print(f"没有找到接收地址对应发送地址 {sender}，跳过该地址。")