import config as c

def stoploss(entry):
    stop_price = entry-(entry * c.stoptarget)
    return stop_price


def takeprofit(entry):
    take = entry + (entry * c.profitgoal)
    return take
