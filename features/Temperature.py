import pandas as pd
import numpy as np
import plotly as pl
import requests
import math
import os

#sheep_data = pd.read_csv('cleanedData/2012_koksvik_6051_2224_cleaned.csv')
#weather_data = pd.read_csv('weatherData/2012_clean.csv')


def add_temperature(sheep_data, weather_data):

    first_date = sheep_data.loc[1, 'Date']
    first_time = sheep_data.loc[1, 'Time']

    index = weather_data.index[weather_data['Tid(norsk normaltid)']
                               == first_date + ' ' + first_time]
    temperature = []
    for i in range(len(sheep_data)):

        date = sheep_data.loc[i, 'Date']
        time = sheep_data.loc[i, 'Time']

        index = weather_data.index[weather_data['Tid(norsk normaltid)']
                                   == date + ' ' + time]
        if (index.size != 0):
            temp = weather_data.loc[index, 'Lufttemperatur']
        else:
            temp = weather_data.loc[index + 1, 'Lufttemperatur']

        temperature.append(temp)

    sheep_data["Temperature"] = temperature

    return sheep_data
