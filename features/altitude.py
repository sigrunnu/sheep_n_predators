import pandas as pd
import numpy as np
import plotly as pl
import requests
import math
import os

os.makedirs('cleanedData', exist_ok=True)
print('lol')

data = pd.read_csv('data/2012_koksvik_6051_2224.csv', sep='\t+', skiprows=[
                   1, 2], engine='python', index_col=False, usecols=range(1, 18))


counter = 1
old_range_count = 0
range_count = 50
data_len = len(data)
altitude = []

while counter <= math.ceil(data_len/50):
    coordinates = []
    for i in range(old_range_count, range_count):
        x = data['Long'][i]
        y = data['Lat'][i]
        d = [x, y]

        coordinates.append(d)

    req = requests.get(
        f'https://ws.geonorge.no/hoydedata/v1/punkt?koordsys=4326&geojson=false&punkter={coordinates}')

    for value in req.json()['punkter']:
        altitude.append(value['z'])

    old_range_count = range_count
    range_count += 50
    counter += 1

    if (range_count >= data_len-1):
        range_count -= 50
        range_count += (data_len - range_count)
    print(counter)


print(len(altitude))
data['altitude'] = altitude
print(data.head(20))
data['Date'] = pd.to_datetime(data['Date'], yearfirst=True)
data.to_csv('cleanedData/2012_koksvik_6051_2224_cleaned.csv')
