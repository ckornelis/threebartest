import pandas as pd
import alphavantageAPIcall as aAPI
from urllib.request import urlretrieve
import os

url = aAPI.callintradayAPI('qqq', 1, 0, 1)
urlretrieve(url, 'testfile.csv')

df = pd.read_csv("testfile.csv")  # read csv file

rows = df.values.tolist()  # convert dataframe into a list
rows.reverse()

for row in rows:
    print(row)

os.remove('testfile.csv')