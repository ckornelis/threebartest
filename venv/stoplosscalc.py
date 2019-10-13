import config as c

def stoploss(entry):
    stop_price = float(entry)-(float(entry) * c.stoptarget)
    return stop_price


def takeprofit(entry):
    take = float(entry) + (float(entry) * c.profitgoal)
    return take
