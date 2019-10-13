import pandas as pd
import stoplosscalc as sl
import cashmanagement as cm
import alpacaAPI as al
import datetime as dt
import time

one_sec_data = []
one_min_data = []
last_length = 0
in_position = False
profit_list = []
x = 240
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
take = 0
stop = 0
buy = 0
local_max = 0
position = 0


while current_time < dt.time(hour=23):  # Change to hour = 15 for normal market time
    # while x != 0:
    temp_data = al.asset_price('BTCUSDT')  # BTCUSDT
    if float(temp_data) > local_max:
        local_max = float(temp_data)
    if in_position:
        print('Own ' + str(position) + ' at ' + str(buy) + '. Current price: ' + str(temp_data))
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
    if not last_length == len(one_min_data):
        # print(dt.datetime.now().time(), in_position, len(one_min_data))
        # print(one_min_data)
        if not in_position:
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
                    if bar2low > bar1low:
                        print(str(bar1time) + ' Bar(C-1) low is lower then Bar(C-2) low')
                        if bar1high < one_min_data[-1][3] and bar2high < one_min_data[-1][3]:
                            buy = one_min_data[-1][3]
                            stop = cm.stop_loss(buy, 4)
                            take = local_max
                            # stop = round(sl.stoploss(one_min_data[-1][3]), 4)
                            # take = round(sl.takeprofit(one_min_data[-1][3]), 4)
                            position = cm.calc_position(buy)
                            print('Buy ' + str(position) + ' at ' + str(buy) + ', stop at ' +
                                  str(stop) + ', take profit at ' + str(take))
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
            if float(one_min_data[-1][1]) > take:
                profit_share = float(one_min_data[-1][1]) - float(buy)
                print('Sell ' + str(position) + ' at ' + str(one_min_data[-1][1]) + '. Profit per share is '
                      + str(profit_share))
                profit_list.append(profit_share)
                in_position = False
            elif float(one_min_data[-1][2]) < stop:
                # profit_share = row['low']-buy
                profit_share = float(stop) - float(buy)
                print('Sell ' + str(position) + ' at ' + str(stop) + '. Profit per share is ' + str(profit_share))
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

print(sum(profit_list))
