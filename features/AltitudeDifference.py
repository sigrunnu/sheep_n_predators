
import pandas as pd

#sheep_data = pd.read_csv( 'features/test.csv')


def add_altitude_difference(data):
    data['Altitude_diff'] = 0
    for i in range(len(data)-1):
        altitude = data.loc[i, 'Altitude']
        next_altitude = data.loc[i+1, 'Altitude']
        diff = next_altitude - altitude
        data.loc[i+1, 'Altitude_diff'] = diff

    return data
