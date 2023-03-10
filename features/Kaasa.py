
import pandas as pd

from Velocity import add_velocity
#from Altitude import add_altitude
from Distance import add_distance
from TrigonometricTime import add_trigonometric_time
from InverseAngle import add_angle
"""
The first row for every individual should have 0 in velocity and distance 
This because they dont have any previous point to calculate from
"""


def fix_0_points_first_row_each_individual(data):
    # get all unique individual numbers (list)
    individuals = data.individual.unique()

    for i in individuals:
        # get index of first row for every individual
        first_index = data.loc[data.individual == i, 'individual'].index[0]

        data.loc[first_index, 'velocity'] = 0.0
        data.loc[first_index, 'distance'] = 0.0

        #print('Fixed 0-points for individual:', str(i))

    return data


"""
Add velocity, altitude, temperature and distance for each data point
"""


def add_features():

    files = ['kaasa_2021.csv', 'kaasa_2020.csv', 'kaasa_2019.csv',
             'kaasa_2018.csv', 'kaasa_2017.csv', 'kaasa_2016.csv', 'kaasa_2015.csv']

    for file in files:
        filepath = 'data/kaasa/' + str(file)
        data = pd.read_csv(filepath)

        #weather_filepath = 'data/weather/' + str(file)
        #weather_data = pd.read_csv(weather_filepath, sep=';')

        if not data.empty:
            # new = add_velocity(data) # DONE
            # new1 = add_distance(data)  # DONE
            # new2 = fix_0_points_first_row_each_individual(new1)  # DONE
            # new = add_velocity(data)  # DONE

            #new3 = add_altitude(new2)
            # new4 = add_temperature(new3, weather_data) # DONE
            #new5 = add_trigonometric_time(data)
            #new['velocity'] = new['velocity'].astype('int64')
            #new2['distance'] = new2['distance'].astype('int64')
            new = add_angle(data)

            if not new.empty:
                new.to_csv(filepath, index=False)
                print('Lagret til fil:', file)


add_features()
