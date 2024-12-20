import okx.Funding as Funding

# API 初始化
apikey = ""
secretkey = ""
passphrase = ""

flag = "0"  # 实盘: 0, 模拟盘: 1

fundingAPI = Funding.FundingAPI(apikey, secretkey, passphrase, False, flag)


addr = [
'evm地址',


]

# 提币
for a in addr:
    result = fundingAPI.withdrawal(
        ccy="ETH",
        toAddr=a,
        amt="0.0011",
        dest="4",
        chain="ETH-Arbitrum One",
        fee="0.00004"
    )
    print(result)