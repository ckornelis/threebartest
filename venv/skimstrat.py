# import cashmanagement as cm
# import alpacaAPI as aL
from config import email, password
import datetime as dt
import time
import robin_stocks as r

r.login(email, password)
current_time = dt.datetime.now().time()
current_min = dt.datetime.now().time().minute
trigger = False
profit = []
BTC_code_id = 0
filename = str(dt.datetime.now().date()) + '_log.txt'
f = open(filename, 'a+')
available = r.load_account_profile('crypto_buying_power')
f.write(str(dt.datetime.now().time()) + ', Opening available cash ' + available + '\r\n')
x = 0
crypto = r.get_crypto_positions('currency')
for item in crypto:
    if item["code"] == 'BTC':
        BTC_code_id = x
    x += 1

buy = 0
crypto = r.get_crypto_positions('cost_bases')  # gets all the crypto positions in a big list/dict
print(crypto[4][0]['direct_quantity'])
if crypto[4][0]['direct_quantity'] == '0.000000000000000000':
    in_position = False
    position = 0
    stop = 0
    take = 0
else:
    in_position = True
    position = crypto[4][0]['direct_quantity']
    stop = float(crypto[4][0]['direct_cost_basis']) - .20
    take = float(crypto[4][0]['direct_cost_basis']) + .10
print('In position? ' + str(in_position))

while not trigger:
    try:
        while current_time < dt.time(hour=23, minute=00):
            ask_price = float(r.crypto.get_crypto_quote('BTC', 'ask_price'))
            bid_price = float(r.crypto.get_crypto_quote('BTC', 'bid_price'))
            if in_position:
                print('Ask: ' + str(ask_price), 'Bid: ' + str(bid_price))
                # print('Own ' + str(position) + ' at ' + str(buy) + '. Current price: ' + str(temp_data))
                if bid_price < stop:
                    profit_per_share = stop - buy  # calculates the profit per share
                    crypto = r.get_crypto_positions('cost_bases')  # gets all the crypto positions in a big list/dict
                    position = crypto[BTC_code_id][0]['direct_quantity']  # isolates the BTC entry and
                    # determines position
                    f.write(str(r.order_sell_crypto_by_quantity('BTC', position, 'bid_price')))  # Sells whole position
                    # at bid
                    print('Sell ' + str(position) + ' at ' + str(stop) + '. Profit per share = ' +
                          str(profit_per_share))
                    trade_profit = float(position) * profit_per_share  # calculates the profit of the trade
                    # available = float(available) + trade_profit
                    available = r.load_account_profile('crypto_buying_power')  # gets the $ amount of
                    # crypto tradable funds then subtracts 10 to ensure there is enough to cover price creep
                    profit.append(trade_profit)  # adds the trade profit to the trade profit list
                    while not crypto[4][0]['direct_cost_basis'] == '0.000000000000000000':
                        print('Waiting for order to process...')
                        time.sleep(.25)
                    in_position = False
                    print('In position? ' + str(in_position))
                if bid_price > take:  # sets the stop to current take and sets take to current ask;
                    # intended to be a trailing stop loss
                    stop = take
                    take = bid_price
            elif not in_position:
                buy = ask_price  # sets buy price to current ask price
                stop = bid_price - 0.10  # sets the stop price to .10$ below the bid price
                take = buy + .10  # sets take price to .10$ above current ask price
                position = float('%.8f' % ((float(available)-10)/float(buy)))  # calculates the number of shares
                # that can be bought at current price
                # print(position)
                # position = cm.calc_position(temp_data)
                order_details = r.order_buy_crypto_by_quantity('BTC', position, 'ask_price')
                f.write(str(order_details))  # buys the crypto
                print('With ' + str(available) + ', buy ' + str(position) +
                      ' at ' + str(ask_price) + '. Total profit ' + str(sum(profit)), order_details)
                crypto = r.get_crypto_positions('cost_bases')  # gets all the crypto positions in a big list/dict
                while crypto[4][0]['direct_cost_basis'] == '0.000000000000000000':
                    print('Waiting for order to process...')
                    time.sleep(.25)
                in_position = True
    except KeyboardInterrupt:
        trigger = True  # when ran from terminal, crtl + c stops the program

#  closes position and finishes final calculations
profit_per_share = stop - buy
f.write(str(r.order_sell_crypto_by_quantity('BTC', position, 'bid_price')))  # Sells whole position at bid
print('Sell ' + str(position) + ' at ' + str(stop) + '. Profit per share = ' + str(profit_per_share))
trade_profit = float(position) * float(profit_per_share)
profit.append(trade_profit)
f.write('Total profit ' + str(sum(profit)))
print('Total profit ' + str(sum(profit)))
print('ended')
