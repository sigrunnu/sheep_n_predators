import pandas as pd
import numpy as np
import plotly as pl


# Loops trough the sheep data and compares date and hour with the weather data from the same year. Get the right temperature and adds it to the data.
def add_temperature(sheep_data, weather_data):
    weather_data['Tid(norsk normaltid)'] = pd.to_datetime(
        weather_data['Tid(norsk normaltid)'], dayfirst=True)

    weather_data['Lufttemperatur'] = weather_data['Lufttemperatur'].str.replace(
        ",", ".")

    sheep_data['temperature'] = ''
    for i in range(len(sheep_data)):

        date = pd.to_datetime(sheep_data.loc[i, 'date_time'])
        new_hour = date.hour + 1 if date.minute > 30 and date.hour != 23 else date.hour
        date = date.replace(hour=new_hour, minute=0, second=0)

        row = weather_data.loc[weather_data['Tid(norsk normaltid)']
                               == date].index

        if (row.size != 0):
            temp = weather_data.loc[row[0], 'Lufttemperatur']
            sheep_data.at[i, 'temperature'] = temp
        else:
            date = sheep_data.at[i, 'date_time']
            print("Date does not exist", date)
            # If the date do not exist in the weather data
            sheep_data.at[i, 'temperature'] = None
    return sheep_data


def add_features():

    files = ['kaasa_2021.csv', 'kaasa_2020.csv', 'kaasa_2019.csv',
             'kaasa_2018.csv', 'kaasa_2017.csv', 'kaasa_2016.csv', 'kaasa_2015.csv']

    for file in files:
        filepath = 'data/kaasa/' + str(file)
        data = pd.read_csv(filepath)

        weather_filepath = 'data/weather/' + str(file)
        weather_data = pd.read_csv(weather_filepath, sep=';')

        if not data.empty:
            new4 = add_temperature(data, weather_data)  # DONE

            if not new4.empty:
                new4.to_csv(filepath, index=False)
                print('Lagret til fil:', file)


add_features()
