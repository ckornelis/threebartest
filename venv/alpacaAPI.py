import alpaca_trade_api as p
from iexfinance.stocks import Stock
from iexfinance.stocks import get_historical_intraday
from iexfinance.data_apis import get_data_points
import datetime as dt
import time


api = p.REST()
current_time = dt.datetime.now().time()


def get_available_funds():
    account = api.get_account()
    return float(account.equity)


def asset_price(q_asset):
    symbol = Stock(q_asset)
    a_sym = symbol.get_quote()
    return a_sym['latestPrice']
    # symbol = Stock(q_asset, output_format='pandas')
    # return symbol.get_quote()


# def show_tradable_equities():

# print(api.get_barset(symbols='QQQ', timeframe='minute'))
# print(api.get_asset('QQQ'))
# one_sec_data = []
# one_min_data = []
# x = 120
# # while current_time < dt.time(hour=15):
# current_min = dt.datetime.now().time().minute
# while x != 0:
#     tempdata = asset_price('BTCUSDT')
#     # print(x)
#     if dt.datetime.now().time().minute == current_min:
#         one_sec_data.append(tempdata)
#     else:
#         print('Open', one_sec_data[0])
#         print('Max', max(one_sec_data))
#         print('Min', min(one_sec_data))
#         print('Close', one_sec_data[-1])
#         one_min_entry_data = one_sec_data[0], max(one_sec_data), min(one_sec_data), one_sec_data[-1]
#         del one_sec_data[:]
#         one_min_data.append(one_min_entry_data)
#         current_min = dt.datetime.now().time().minute
#     x = x-1
#
#     if not x == 0:
#         time.sleep(1)
#
# print(one_min_data)

# buy at ask, sell at bid
