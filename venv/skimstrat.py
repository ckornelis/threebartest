import cashmanagement as cm
import alpacaAPI as aL
from config import email
from config import password
import datetime as dt
import robin_stocks as r

r.login(email, password)
current_time = dt.datetime.now().time()
current_min = dt.datetime.now().time().minute
in_position = False
position = 0
stop = 0
take = 0
buy = 0
sell = 0
profit = []
available = 189.52

while current_time < dt.time(hour=23):
    temp_data = float(r.crypto.get_crypto_quote('BTC', 'ask_price'))
    if in_position:
        # print('Own ' + str(position) + ' at ' + str(buy) + '. Current price: ' + str(temp_data))
        if temp_data < stop:
            profit_per_share = stop - buy
            print('Sell ' + str(position) + ' at ' + str(stop) + '. Profit per share = ' + str(profit_per_share))
            trade_profit = position * profit_per_share
            available = available + trade_profit
            profit.append(trade_profit)
            in_position = False
        if temp_data > take:
            stop = take
            take = temp_data
    elif not in_position:
        buy = float(r.crypto.get_crypto_quote('BTC', 'ask_price'))
        stop = buy - 0.10
        take = buy + 1
        position = available/float(temp_data)
        # position = cm.calc_position(temp_data)
        print('With ' + str(available) + ', buy ' + str(position) +
              ' at ' + str(temp_data) + '. Total profit ' + str(sum(profit)))
        in_position = True
