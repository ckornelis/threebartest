import pandas as pd
import os
import alphavantageAPIcall as aAPI
from urllib.request import urlretrieve
import stoplosscalc as sl


url = aAPI.callintradayAPI('nke', 1, 0, 1)
urlretrieve(url, 'testfile.csv')

data = pd.read_csv("testfile.csv")
data = data[::-1]
# print(data['close'])

line_count = 0
in_position = False
profit_list = []
for index, row in data.iterrows():
    if not in_position:
        if line_count == 0:
            line_count += 1
            bar1close = row['close']
            bar1low = row['low']
            bar1high = row['high']
            bar1open = row['open']
            bar1time = row['timestamp']
        elif line_count == 1:
            line_count += 1
            bar2high = bar1high
            bar2low = bar1low
            bar2close = bar1close
            bar2open = bar1open
            bar2time = bar1time
            bar1close = row['close']
            bar1low = row['low']
            bar1high = row['high']
            bar1open = row['open']
            bar1time = row['timestamp']
        elif line_count > 1:
            if bar2close < bar2open:
                # print(bar2time + ' Bar(C-2) closed down')
                if bar2low > bar1low:
                    # print(bar1time+ ' Bar(C-1) low is lower then Bar(C-2) low')
                    if bar1high < row['close'] and bar2high < row['close']:
                        buy = row['close']
                        stop = round(sl.stoploss(row['close']), 4)
                        take = round(sl.takeprofit(row['close']), 4)
                        print('Buy at '+ str(row['close']) + ', stop at ' + str(stop) + ', take profit at ' + str(take))
                        # print(row['timestamp']+ ' Bar(C) close is higher then the Bar(C-2) close and Bar(C-1) close')
                        in_position = True
            bar2high = bar1high
            bar2low = bar1low
            bar2close = bar1close
            bar2open = bar1open
            bar2time = bar1time
            bar1time = row['timestamp']
            bar1high = row['high']
            bar1low = row['low']
            bar1close = row['close']
            bar1open = row['open']
            line_count += 1
    elif in_position:
        if row['high']>take:
            profit_share = row['high']-buy
            print('Sell at '+ str(row['high']) + '. Profit per share is ' + str(profit_share))
            profit_list.append(profit_share)
            in_position = False
        elif row['low']< stop:
            profit_share = row['low']-buy
            print('Sell at '+ str(row['low'])+ '. Profit per share is ' + str(profit_share))
            profit_list.append(profit_share)
            in_position = False
        bar2high = bar1high
        bar2low = bar1low
        bar2close = bar1close
        bar2open = bar1open
        bar2time = bar1time
        bar1time = row['timestamp']
        bar1high = row['high']
        bar1low = row['low']
        bar1close = row['close']
        bar1open = row['open']
        line_count += 1
    # print(line_count)
# os.remove('testfile.csv')
print(sum(profit_list))
