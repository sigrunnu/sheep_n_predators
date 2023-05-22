import numpy as np
import pandas as pd


def add_angle(data):
    # Group the data by individual and apply the 'add_angle_individual' function to each individual group
    individuals = data.groupby('individual')
    data['angle'] = individuals.apply(add_angle_individual)
    return data


def add_angle_individual(individual):
    lat = individual['latitude'].values
    lon = individual['longitude'].values

    # Calculate vectors between consecutive positions
    vec1 = np.column_stack((lat[:-2] - lat[1:-1], lon[:-2] - lon[1:-1]))
    vec2 = np.column_stack((lat[2:] - lat[1:-1], lon[2:] - lon[1:-1]))

    # Calculate the dot product and vector lengths
    dot = (vec1 * vec2).sum(axis=1)
    len1 = np.linalg.norm(vec1, axis=1)
    len2 = np.linalg.norm(vec2, axis=1)

    # Calculate the angle between the vectors
    angle = np.degrees(np.arccos(dot / (len1 * len2)))

    # Calculate the inverse trajectory angle
    angle = 180 - angle

    # Set the first and last angle to 0
    angle = np.concatenate(([0], angle, [0]))

    return angle
