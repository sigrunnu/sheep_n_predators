import pandas as pd
import numpy as np
import plotly as pl
import requests
import math
import os
import datetime

from decimal import Decimal

data = pd.read_csv('weatherData/2012.csv', sep=';')


data['Tid(norsk normaltid)'] = pd.to_datetime(
    data['Tid(norsk normaltid)'], yearfirst=True)


data['Lufttemperatur'] = data['Lufttemperatur'].str.replace(",", ".")


df = data.iloc[:25]
for i in range(0, len(df)*2-1, 2):

    x = df.loc[[i]]

    x['Lufttemperatur'] = 10
    x['Tid(norsk normaltid)'] = x['Tid(norsk normaltid)'] + \
        datetime.timedelta(minutes=30)

    current_temp = float(df.loc[i, 'Lufttemperatur'])
    if (i != len(df)-1):
        next_temp = float(df.loc[i + 1, 'Lufttemperatur'])
        x['Lufttemperatur'] = round((current_temp + next_temp)/2, 1)
    else:
        current_temp = float(df.loc[i, 'Lufttemperatur'])
        next_temp = float(df.loc[i - 1, 'Lufttemperatur'])
        x['Lufttemperatur'] = round((current_temp + next_temp)/2, 1)

    df = pd.concat([df.iloc[:i+1], x, df.iloc[i+1:]]).reset_index(drop=True)


# data.to_csv('cleanedData/2012_koksvik_6051_2224_cleaned.csv')
print(df)
