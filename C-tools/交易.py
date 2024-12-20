import ccxt
import pandas as pd
import time
import logging

# 配置你的 OKX API 密钥
api_key = '你的API_KEY'
api_secret = '你的API_SECRET'
password = '你的API_PASSWORD'

# 初始化 OKX API 客户端
exchange = ccxt.okx({
    'apiKey': api_key,
    'secret': api_secret,
    'password': password,
    'enableRateLimit': True,
})

# 设置交易对
symbol = 'JUP-USDT-SWAP'  # 你可以修改为你想要交易的币种对
timeframe = '1h'  # 选择小时线（1小时K线）
limit = 200  # 获取历史数据的最大数量，200根K线
amount = 0.001  # 每次交易的数量，可以根据你的资金调整

# 配置日志
logging.basicConfig(filename='trading_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')


# 获取历史数据
def fetch_ohlcv(symbol, timeframe, limit):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    ohlcv_df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    ohlcv_df['timestamp'] = pd.to_datetime(ohlcv_df['timestamp'], unit='ms')
    return ohlcv_df


# 计算均线
def calculate_ma(data, window):
    return data['close'].rolling(window=window).mean()


# 判断 MA10 上穿 MA40 或下穿 MA40
def check_ma_cross(ma10, ma40):
    if ma10.iloc[-2] < ma40.iloc[-2] and ma10.iloc[-1] > ma40.iloc[-1]:
        return 'buy'  # MA10上穿MA40，买入
    elif ma10.iloc[-2] > ma40.iloc[-2] and ma10.iloc[-1] < ma40.iloc[-1]:
        return 'sell'  # MA10下穿MA40，卖出
    return None  # 没有交叉


# 执行开多操作（买入合约）
def open_long(symbol, amount):
    try:
        print(f"执行开多操作: {amount} {symbol}")
        order = exchange.create_market_buy_order(symbol, amount)
        logging.info(f"开多成功: {amount} {symbol} - {order}")
        return order
    except Exception as e:
        logging.error(f"开多失败: {amount} {symbol} - 错误: {e}")
        print(f"开多失败: {e}")


# 执行开空操作（卖出合约）
def open_short(symbol, amount):
    try:
        print(f"执行开空操作: {amount} {symbol}")
        order = exchange.create_market_sell_order(symbol, amount)
        logging.info(f"开空成功: {amount} {symbol} - {order}")
        return order
    except Exception as e:
        logging.error(f"开空失败: {amount} {symbol} - 错误: {e}")
        print(f"开空失败: {e}")


# 平仓操作（卖出多单）
def close_long(symbol, amount):
    try:
        print(f"平多操作: {amount} {symbol}")
        order = exchange.create_market_sell_order(symbol, amount)
        logging.info(f"平多成功: {amount} {symbol} - {order}")
        return order
    except Exception as e:
        logging.error(f"平多失败: {amount} {symbol} - 错误: {e}")
        print(f"平多失败: {e}")


# 平仓操作（买入空单）
def close_short(symbol, amount):
    try:
        print(f"平空操作: {amount} {symbol}")
        order = exchange.create_market_buy_order(symbol, amount)
        logging.info(f"平空成功: {amount} {symbol} - {order}")
        return order
    except Exception as e:
        logging.error(f"平空失败: {amount} {symbol} - 错误: {e}")
        print(f"平空失败: {e}")


# 创建止损单（多单和空单）
def create_stop_loss(symbol, amount, entry_price, stop_loss_percentage, position_type):
    stop_loss_price = entry_price * (1 - stop_loss_percentage) if position_type == 'long' else entry_price * (
                1 + stop_loss_percentage)

    # 判断止损单类型：多单还是空单
    side = 'sell' if position_type == 'long' else 'buy'

    # 创建止损单
    try:
        stop_loss_order = exchange.create_order(symbol, 'stop', side, amount, stop_loss_price, {
            'stop': 'loss',
            'price': stop_loss_price
        })
        logging.info(f"创建止损单成功: {side} {amount} {symbol} - 止损价: {stop_loss_price}")
        print(f"创建止损单成功: {side} {amount} {symbol} - 止损价: {stop_loss_price}")
        return stop_loss_order
    except Exception as e:
        logging.error(f"创建止损单失败: {side} {amount} {symbol} - 错误: {e}")
        print(f"创建止损单失败: {side} {amount} {symbol} - 错误: {e}")


# 记录每次的收益
def log_profit_or_loss(entry_price, exit_price, amount, position_type):
    profit_or_loss = (exit_price - entry_price) * amount if position_type == 'long' else (
                                                                                                     entry_price - exit_price) * amount
    logging.info(
        f"平仓收益: {profit_or_loss:.2f} USDT ({position_type}单) - 入场价: {entry_price}, 出场价: {exit_price}")
    print(f"平仓收益: {profit_or_loss:.2f} USDT ({position_type}单) - 入场价: {entry_price}, 出场价: {exit_price}")


# 获取当前账户余额
def get_balance():
    balance = exchange.fetch_balance()
    return balance['total']['USDT']  # 获取 USDT 余额，你可以根据实际情况修改


# 主函数
def main():
    entry_price_long = None  # 用于记录多单的入场价
    entry_price_short = None  # 用于记录空单的入场价
    position_type = None  # 记录当前持仓类型

    stop_loss_percentage = 0.03  # 止损比例，3% 可以调整

    while True:
        try:
            # 获取历史K线数据
            ohlcv_df = fetch_ohlcv(symbol, timeframe, limit)

            # 计算 MA10 和 MA40
            ma10 = calculate_ma(ohlcv_df, 10)
            ma40 = calculate_ma(ohlcv_df, 40)

            # 检查 MA10 和 MA40 的交叉
            signal = check_ma_cross(ma10, ma40)

            # 执行操作
            if signal == 'buy':
                print("检测到 MA10 上穿 MA40, 开多并平空单")
                # 如果当前有空单，则先平空单
                if position_type == 'short':
                    close_short(symbol, amount)
                    log_profit_or_loss(entry_price_short, ohlcv_df['close'].iloc[-1], amount, 'short')
                    position_type = None  # 清空空单状态
                # 开多
                open_long(symbol, amount)
                entry_price_long = ohlcv_df['close'].iloc[-1]
                position_type = 'long'
                # 创建止损单
                create_stop_loss(symbol, amount, entry_price_long, stop_loss_percentage, 'long')

            elif signal == 'sell':
                print("检测到 MA10 下穿 MA40, 卖出多单并建仓空单")
                # 如果当前有多单，则先平多单
                if position_type == 'long':
                    close_long(symbol, amount)
                    log_profit_or_loss(entry_price_long, ohlcv_df['close'].iloc[-1], amount, 'long')
                    position_type = None  # 清空多单状态
                # 开空
                open_short(symbol, amount)
                entry_price_short = ohlcv_df['close'].iloc[-1]
                position_type = 'short'
                # 创建止损单
                create_stop_loss(symbol, amount, entry_price_short, stop_loss_percentage, 'short')

            # 等待下一次周期（1小时）
            time.sleep(60 * 60)  # 等待1小时

        except Exception as e:
            logging.error(f"发生错误: {e}")
            print(f"发生错误: {e}")
            time.sleep(60)  # 出错时等待1分钟重试

if __name__ == '__main__':
    main()