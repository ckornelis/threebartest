import pandas as pd
import datetime as dt
import time
import robin_stocks as r
from config import email, password

r.login(email, password)
one_sec_data = []
one_min_data = []
last_length = 0
profit_list = []
current_time = dt.datetime.now().time()
current_min = dt.datetime.now().time().minute
bar1close = 0,
bar1low = 0,
bar1high = 0,
bar1open = 0,
bar1time = 0,
bar2close = 0,
bar2low = 0,
bar2high = 0,
bar2open = 0,
bar2time = 0,
local_max = 0
trigger = False

BTC_code_id = 0
filename = str(dt.datetime.now().date()) + '_log_three_bar.txt'
f = open(filename, 'a+')
available = r.load_account_profile('crypto_buying_power')
f.write(str(dt.datetime.now().time()) + ', Opening available cash ' + available + '\r\n')
x = 0
crypto = r.get_crypto_positions('currency')
for item in crypto:
    if item["code"] == 'BTC':
        BTC_code_id = x
    x += 1

crypto = r.get_crypto_positions('cost_bases')  # gets all the crypto positions in a big list/dict
print(crypto[4][0]['direct_quantity'])
if crypto[4][0]['direct_quantity'] == '0.000000000000000000':
    in_position = False
    position = 0
    stop = 0
    take = 0
    buy = 0
else:
    in_position = True
    position = crypto[4][0]['direct_quantity']
    stop = float(crypto[4][0]['direct_cost_basis']) - 1.00
    take = float(crypto[4][0]['direct_cost_basis']) + .10
    buy = float(crypto[4][0]['direct_cost_basis'])
print('In position? ' + str(in_position))

# x = 240
while not trigger:
    try:
        while current_time < dt.time(hour=23):  # Change to hour = 15 for normal market time
            ask_price = float(r.crypto.get_crypto_quote('BTC', 'ask_price'))
            bid_price = float(r.crypto.get_crypto_quote('BTC', 'bid_price'))
            # while x != 0:
            temp_data = bid_price
            if float(temp_data) > local_max:
                local_max = float(temp_data)
            if in_position:
                print('Own ' + str(position) + ' at ' + str(buy) + '. Current bid price: ' + str(temp_data))
                f.write('Own ' + str(position) + ' at ' + str(buy) + '. Current bid price: ' + str(temp_data) + '\r\n')
            # print(dt.datetime.now().time())
            if dt.datetime.now().time().minute == current_min:
                one_sec_data.append(temp_data)
            else:
                # print('Open', one_sec_data[0])
                # print('Max', max(one_sec_data))
                # print('Min', min(one_sec_data))
                # print('Close', one_sec_data[-1])
                one_min_entry_data = one_sec_data[0], max(one_sec_data), min(one_sec_data), one_sec_data[-1]
                del one_sec_data[:]
                # print(one_min_entry_data)
                one_min_data.append(one_min_entry_data)
                current_min = dt.datetime.now().time().minute

            x = x-1
            if not in_position:
                if not last_length == len(one_min_data):
                    if len(one_min_data) == 1:
                        last_length += 1
                        bar1close = one_min_data[-1][3]  # row['close']
                        bar1low = one_min_data[-1][2]  # row['low']
                        bar1high = one_min_data[-1][1]  # row['high']
                        bar1open = one_min_data[-1][0]  # row['open']
                        bar1time = dt.datetime.now()  # row['timestamp']
                    elif len(one_min_data) == 2:
                        last_length += 1
                        bar2high = bar1high
                        bar2low = bar1low
                        bar2close = bar1close
                        bar2open = bar1open
                        bar2time = bar1time
                        bar1close = one_min_data[-1][3]  # row['close']
                        bar1low = one_min_data[-1][2]  # row['low']
                        bar1high = one_min_data[-1][1]  # row['high']
                        bar1open = one_min_data[-1][0]  # row['open']
                        bar1time = dt.datetime.now()  # row['timestamp']
                    elif len(one_min_data) > 2:
                        # print(bar2close, bar2open)
                        if bar2close < bar2open:
                            print(str(bar2time) + ' Bar(C-2) closed down')
                            # f.write(str(bar2time) + ' Bar(C-2) closed down' + '\r\n')
                            if bar2low > bar1low:
                                print(str(bar1time) + ' Bar(C-1) low is lower then Bar(C-2) low')
                                # f.write(str(bar1time) + ' Bar(C-1) low is lower then Bar(C-2) low' + '\r\n')
                                if bar1high < one_min_data[-1][3] and bar2high < one_min_data[-1][3]:
                                    buy = one_min_data[-1][3]
                                    stop = buy-1.00
                                    take = buy+.10
                                    position = float(available)/float(buy)
                                    print('Buy ' + str(position) + ' at ' + str(buy) + ', stop at ' +
                                          str(stop) + ', take profit at ' + str(take))
                                    f.write('Buy ' + str(position) + ' at ' + str(buy) + ', stop at ' + str(stop) +
                                            ', take profit at ' + str(take) + '\r\n')
                                    in_position = True
                        bar2high = bar1high
                        bar2low = bar1low
                        bar2close = bar1close
                        bar2open = bar1open
                        bar2time = bar1time
                        bar1close = one_min_data[-1][3]  # row['close']
                        bar1low = one_min_data[-1][2]  # row['low']
                        bar1high = one_min_data[-1][1]  # row['high']
                        bar1open = one_min_data[-1][0]  # row['open']
                        bar1time = dt.datetime.now()  # row['timestamp']
                        last_length += 1
            elif in_position:
                print(bid_price, one_min_data[-1][1])
                if float(bid_price) > stop:
                    stop = float(bid_price)-.20
                    # profit_share = float(one_min_data[-1][1]) - float(buy)
                    # print('Sell ' + str(position) + ' at ' + str(one_min_data[-1][1]) + '. Profit per share is '
                    #       + str(profit_share))
                    # profit_list.append(profit_share)
                    # in_position = False
                elif float(bid_price) < stop:
                    # profit_share = row['low']-buy
                    profit_share = float(bid_price) - float(buy)
                    print('Sell ' + str(position) + ' at ' + str(bid_price) + '. Profit per share is ' +
                          str(profit_share))
                    f.write('Sell ' + str(position) + ' at ' + str(bid_price) + '. Profit per share is ' +
                            str(profit_share) + '\r\n')
                    profit_list.append(profit_share)
                    in_position = False
                bar2high = bar1high
                bar2low = bar1low
                bar2close = bar1close
                bar2open = bar1open
                bar2time = bar1time
                bar1close = one_min_data[-1][3]  # row['close']
                bar1low = one_min_data[-1][2]  # row['low']
                bar1high = one_min_data[-1][1]  # row['high']
                bar1open = one_min_data[-1][0]  # row['open']
                bar1time = dt.datetime.now()  # row['timestamp']
                last_length += 1

            if not x == 0:
                time.sleep(1)

    except KeyboardInterrupt:
        trigger = True  # when ran from terminal, crtl + c stops the program
print(sum(profit_list))
