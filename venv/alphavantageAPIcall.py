import config

baseapiurl = "https://www.alphavantage.co/"
qAPIkey = config.APIKey


def calldailyAPI(isym: str, ioutput: int, idatatype: int) -> str:
    qsymbol = isym
    qfunction = 'TIME_SERIES_DAILY'
    if ioutput == 0:
        qoutputsize = 'full'
    elif ioutput == 1:
        qoutputsize = 'compact'
    if idatatype == 0:
        qdatatype = 'json'
    elif idatatype == 1:
        qdatatype = 'csv'

    APItocall = baseapiurl + 'query?function=' + qfunction + '&symbol=' + qsymbol + '&apikey=' + qAPIkey + '&outputsize=' + qoutputsize + '&datatype=' + qdatatype
    return APItocall


def callintradayAPI (isym: str, iinterval: int, ioutput: int, idatatype: int) -> str:
    qsymbol = isym
    qfunction = 'TIME_SERIES_INTRADAY'
    if iinterval == 1:
        qinterval = '1min'
    elif iinterval == 5:
        qinterval = '5min'
    elif iinterval == 15:
        qinterval = '15min'
    elif iinterval == 30:
        qinterval = '30min'
    elif iinterval == 60:
        qinterval = '60min'
    if ioutput == 0:
        qoutputsize = 'full'
    elif ioutput == 1:
        qoutputsize = 'compact'
    if idatatype == 0:
        qdatatype = 'json'
    elif idatatype == 1:
        qdatatype = 'csv'

    APItocall = baseapiurl + 'query?function=' + qfunction + '&symbol=' + qsymbol + '&interval=' + qinterval + '&apikey=' + qAPIkey + '&outputsize=' + qoutputsize + '&datatype=' + qdatatype
    return APItocall


def call_realtime_crypto(ifrom: str, ito: str):
    qfunction = 'CURRENCY_EXCHANGE_RATE'
    qfrom = ifrom
    qto = ito
    APItocall = baseapiurl + 'query?function=' + qfunction + '&from_currency=' + qfrom + '&to_currency=' + qto + '&apikey=' + qAPIkey
    return APItocall


def call_MACD(isym: str, iint: str, idatatype: str, isertype='close', ifast=12, islow=26, isignal=9):
    qfunction = 'MACD'
    qsymbol = isym
    qinterval = iint  # 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly
    qseriestype = isertype  # close, open, high, low'
    qfastperiod = str(ifast)
    qslowperiod = str(islow)
    qsignalperiod = str(isignal)
    qdatatype = idatatype
    APItocall = baseapiurl + 'query?function=' + qfunction + '&symbol=' + qsymbol + '&interval=' + qinterval + '&series_type=' + qseriestype + '&apikey=' + qAPIkey + '&fastperiod=' + qfastperiod + '&slowperiod=' + qslowperiod + '&signalperiod=' + qsignalperiod + '&datatype=' + qdatatype
    return APItocall