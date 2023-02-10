
import pandas as pd

from Velocity import add_velocity
from Altitude import add_altitude
from Distance import add_distance
from TemperatureEveryHour import add_temperature


"""
The first row for every individual should have 0 in velocity and distance 
This because they dont have any previous point to calculate from
"""
def fix_0_points_first_row_each_individual(data):
    individuals = data.individual.unique() # get all unique individual numbers (list)

    for i in individuals:
        first_index = data.loc[data.individual == i, 'individual'].index[0] # get index of first row for every individual

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

            weather_filepath = 'data/weather/' + str(file)
            weather_data = pd.read_csv(weather_filepath, sep=';')

            if not data.empty:
                #new = add_velocity(data) # DONE
                #new1 = add_distance(new) # DONE
                #new2 = fix_0_points_first_row_each_individual(new1) # DONE
                #new3 = add_altitude(new2) 
                #new4 = add_temperature(new3, weather_data) # DONE

                if not new4.empty:
                            new4.to_csv(filepath, index=False)
                            print('Lagret til fil:', file)

add_features()
