import config as c
import alpacaAPI as aL
import math


# available = aL.get_available_funds()
available = 189.52
at_risk_funds = available * c.risk_threshold


def stop_loss(buy_price, decimals):
    committed_cash = calc_position(float(buy_price)) * float(buy_price)
    return round((committed_cash - at_risk_funds)/calc_position(buy_price), decimals)


def calc_position(buy_price):
    # stock_volume = math.trunc(available/float(buy_price))
    stock_volume = available / float(buy_price)
    return stock_volume


def calc_crypto_position(buy_price):
    return at_risk_funds

# def trail_stop_loss():


# need something to calc trailing stop loss