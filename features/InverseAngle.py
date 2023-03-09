import numpy as np
import pandas as pd


# Add angle - but separate by individual positions
def add_angle(data):
    individuals = data.individual.unique()
    data['angle'] = 0
    for i in individuals:
        # get index of first row for every individual
        individual = data[data['individual'] == i]
        start_index = individual.first_valid_index()
        end_index = start_index + len(individual)
        add_angle_individual(data, start_index, end_index)

    return data


def add_angle_individual(df, start_index, end_index):
    for i in range(start_index + 1, end_index-1):
        vec1 = [df.at[i - 1, 'latitude'] - df.at[i, 'latitude'],
                df.at[i - 1, 'longitude'] - df.at[i, 'longitude']]
        vec2 = [df.at[i + 1, 'latitude'] - df.at[i, 'latitude'],
                df.at[i + 1, 'longitude'] - df.at[i, 'longitude']]

        len1 = np.sqrt(vec1[0]**2 + vec1[1]**2)
        len2 = np.sqrt(vec2[0] ** 2 + vec2[1] ** 2)
        dot = np.dot(vec1, vec2)

        # To make sure that we do not divide by zero - check that the values are not zero
        if len1*len2 == 0 and dot == 0:
            df.at[i, 'angle'] = 0
        else:
            df.at[i, 'angle'] = 180 - \
                (np.arccos(round(dot/(len1*len2), 7)) * 180 / np.pi)

            # 180 minus angle is the inverse trajectory angle
