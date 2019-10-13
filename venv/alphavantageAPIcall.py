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