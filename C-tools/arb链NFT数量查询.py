import time
import random,requests,json
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.exceptions import ContractLogicError

# Arbitrum RPC URL
#arb_rpc_url = 'https://arb1.arbitrum.io/rpc'
arb_rpc_url = 'https://arbitrum-one.publicnode.com'

# 设置 NFT 合约地址（替换为你的合约地址）
nft_contract_address = Web3.to_checksum_address('0x830723f67Db87e2540Fc704F6878F8B14058154C')

# 设置多个发送者（转出方）钱包地址
sender_addresses = [
Web3.to_checksum_address("0x59dF52D51789Ff5d8Db032B35872C6d34AC61551"),
Web3.to_checksum_address("0x6d2Eac77905A52D22DB8E18Ab83a19f6a0720A51"),
Web3.to_checksum_address("0xd1b72f6C19F694A5Ff8AB39FeEC35F3CBDee1c6B"),
Web3.to_checksum_address("0xEC41C68259E0d58B50C76e1b68ccdcc403399EdE"),
Web3.to_checksum_address("0x63505468b04becb3e7DD2960aB96a09ca78EEdBd"),
Web3.to_checksum_address("0xa5423daE3B03124fF1166C979F6A2408B3F7975a"),
Web3.to_checksum_address("0xbe58562051Ff28eC52dDc1C1771Da305AABE2904"),
Web3.to_checksum_address("0xb61b4EC7033f83EC57b75442fb238F1Eede1d40e"),
Web3.to_checksum_address("0x60cAb3f021C45DE0230da82E960632F152F8d2FF"),
Web3.to_checksum_address("0x077b22a9BDDE082C227069F7Af923A005eDc96e5"),
Web3.to_checksum_address("0xb047e6a505e36676505b8012EF5d437A5CE0D7d7"),
Web3.to_checksum_address("0x561dd29F6d85291d84c8aEF18F407156F180ECD0"),
Web3.to_checksum_address("0xc765099d2908e36bDcF67331E098dC64eE57e1d5"),
Web3.to_checksum_address("0xe186d48E3c39b3d5b0Bd4ac019972AaF4055345f"),
Web3.to_checksum_address("0x6593083AD6c836AAFcEf2B3fD4Ebb60AC26F62F2"),
Web3.to_checksum_address("0xa9F1Cc3Ab28A92A81D00b288a2c9c97d53B11915"),
Web3.to_checksum_address("0x74af955ec774D621F50673AdEf6dae5063FF69B1"),
Web3.to_checksum_address("0xe612176647eFf6C6516169061dfD49cA529D0636"),
Web3.to_checksum_address("0x340551c3b435a85262A3F993603922B407309935"),
Web3.to_checksum_address("0x4E139130bfaC6d1D2f51Ee92a0d1349fca54008E"),
Web3.to_checksum_address("0xdd6fA23380Ad78EBAab89773FC216F37f11beab5"),
Web3.to_checksum_address("0x5EA7F4aB512Dcf5388D771df517fBd9719b9a017"),
Web3.to_checksum_address("0xAd95458B9c508DEe8C723747b670e37A6bd87b88"),
Web3.to_checksum_address("0x7314A97B14c5D34e0Cd09E2b79d3235333494A8f"),
Web3.to_checksum_address("0x2d50cdE33bdE413A8514348235f07635de496EBC"),
Web3.to_checksum_address("0x56cc6D372Da617C1E9Ef5E6360323CeE825B01b4"),
Web3.to_checksum_address("0x62936dB755a5627d08eA69cadcF4761bE7fC6f5A"),
Web3.to_checksum_address("0xd1D51e56e3fCFF7DD6b885F454e5B4363E770A01"),
Web3.to_checksum_address("0x482a62dF952F121240571f827816331668d08f86"),
Web3.to_checksum_address("0xAC88D1E675F3485b1cB2E206D5Ca208F9debBa36"),
Web3.to_checksum_address("0x815bbDbEfaD0Df4C82e3e4FB7ECC529193C71F23"),
Web3.to_checksum_address("0x24F41EC736c557d46780A0daDd5c712180C363A8"),
Web3.to_checksum_address("0x6DD1B5a62E5bd7ffF3BAcfD7FEaaF79363bc0d9F"),
Web3.to_checksum_address("0xF08C15E421167729E7719CE3dB5a64AD6fe19943"),
Web3.to_checksum_address("0x74B3de73555013067f91E0d5Dbb76DDD0adf2186"),
Web3.to_checksum_address("0x3E01d4e76F8b250900F0987C7f4c55f1B68c0a27"),
Web3.to_checksum_address("0x34C30C1be155911E5D2F11C54AD55dDE2194F4f7"),
Web3.to_checksum_address("0x7f6756bBA6a0264616584decd163376DD03B8A4b"),
Web3.to_checksum_address("0x2818Ca4a9Cd34eF3BB75Cb57a1095c5D1721B141"),
Web3.to_checksum_address("0x1563A1f1B95FBbe5B2d14317651871c412F18b81"),
Web3.to_checksum_address("0x803CCCe28FAa395E861c7ceE1807D9e2e1EcB3eC"),
Web3.to_checksum_address("0x864BA4Cc60Cc500888787D916e21fEF410C5F248"),
Web3.to_checksum_address("0xB90Fc20EEB9c773E96B4b270b512971dD2406794"),
Web3.to_checksum_address("0xCd98EB68722fEa9f4f4C05DFb1ef4c47Ce6c9747"),
Web3.to_checksum_address("0x9cd4628F1F7490b4421bA4F30002f24D52f4195D"),
Web3.to_checksum_address("0x79689Df9AA255EcAed59b4e315e322134fEbF76d"),
Web3.to_checksum_address("0x90c1b8d42D73091AC27eE40b128a3a5008F4A05a"),
Web3.to_checksum_address("0x4ef7798C2B5cAEE41D015206CCC909A2900A382a"),
Web3.to_checksum_address("0x6fC5b99C4Fe62139A60AAeF52cc415FB3F2f8875"),
Web3.to_checksum_address("0x5368F7D9DDFEF60C4bE6561e92fD69B588A4f9Ac"),
Web3.to_checksum_address("0xd7eE098D75F5Bbe1B17906781CACDA7D6A41204c"),
Web3.to_checksum_address("0x9FFC970b16a4360F7E3F10346CCF0EA31f2c4291"),
Web3.to_checksum_address("0xBdDF3C8493eb09d5Ccd6c65CBC3b57365e54E67a"),
Web3.to_checksum_address("0x7Df4aEbc14a7ba89e4DD8eF6B1B4014ADFB56E31"),
Web3.to_checksum_address("0xEa1F3f0bFb68939B08eE65dD7BC093b18CA17cEd"),
Web3.to_checksum_address("0x2607ece9c3eCB73F0c7650FAf0eE66acB2d31A36"),
Web3.to_checksum_address("0x828E7Ac5E2AED209Fedd4b23C33e97710B2eadA8"),
Web3.to_checksum_address("0x8a921190aDAA6c168a035D530108011Cd1Cf3D3f"),
Web3.to_checksum_address("0x4C5F6914371c2C765b68D3923722e6dBf459c17d"),
Web3.to_checksum_address("0x576322f2d34F67FCa3F51A0c2732fc1647A6936A"),
Web3.to_checksum_address("0x3d417CF320D2F7b40762F72598Fe6E7E738bF9A6"),
Web3.to_checksum_address("0x17fb3752D0AecFaD1Ba72e7c892C87ED80786bE6"),
Web3.to_checksum_address("0x1f08D3d32b961E26a807d7D082fB378E2d116526"),
Web3.to_checksum_address("0xa87aC6d2C63Bf1b14556f02d37D80F5149eDBE5b"),
Web3.to_checksum_address("0xFdD53E9f232Dc8C7E59EC238C18F75987B08854d"),
Web3.to_checksum_address("0x3b9291980D245d0051767eB6fF43d7E1fC28084B"),
Web3.to_checksum_address("0xD11121Dea9BE911410283Ec1c6586ad93ea0B4E2"),
Web3.to_checksum_address("0xD02795E9575fE5C06afB2F35e3687B717D577Ee0"),
Web3.to_checksum_address("0x8a29015fae02E906e369Ce8D38761Bb5035b73D1"),
Web3.to_checksum_address("0xdcB6d22fD6b3e8f218C44bd9F8Ee76C1A942D0E5"),
Web3.to_checksum_address("0x56Ac19fEb4EeF46c2985552a72e42052c6A09AdC"),
Web3.to_checksum_address("0x4467f0095A1d5c6509eEB109BF4A8D10fdB896Fc"),
Web3.to_checksum_address("0xF0894C1B1Aa324dd84D5C9453637B4fb0850BEAc"),
Web3.to_checksum_address("0xda1A4aD00C7916CbB2Bd5B5eD5FB3563DAFe25ef"),
Web3.to_checksum_address("0x06D3e4AF78F2a7a6892635430cA34cA24d3f67cA"),
Web3.to_checksum_address("0x874cb2b6414E02F907bF51995C14CCb410479a98"),
Web3.to_checksum_address("0xfC6eE9BAcba0369D64e75582Ef2606E39a3FEC5b"),
Web3.to_checksum_address("0xFDf59f2107309DB872CeCc69546C46d2c7A7c1d7"),
Web3.to_checksum_address("0x3ad238fB057Fa792f9b1aF48Ab1FD73e756A0069"),
Web3.to_checksum_address("0x1feeD0A63c27F0BdC4A97F9dD4CC9D61e43F7836"),
Web3.to_checksum_address("0xCa2E4127187b8192f0B9620794A0366F8523937f"),
Web3.to_checksum_address("0x1E454a94cfD842659C7BE9A6739DA8D5bB4d4B8F"),
Web3.to_checksum_address("0xf35A89f9C78143fb16B5E1BD8EeA416DE54594e3"),
Web3.to_checksum_address("0xCaCd102bAB3B567F9895158C4E12a5aBDF946F45"),
]  # 添加更多发送地址


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

# 主函数
def main():
    a = 0
    for sender_address in sender_addresses:
        # 获取当前发送者钱包所有 NFT 的 token_id
        tokens = get_tokens_of_owner(sender_address)
        print(f"钱包 {sender_address} 持有的 token_id: {tokens}")


if __name__ == '__main__':
    main()
