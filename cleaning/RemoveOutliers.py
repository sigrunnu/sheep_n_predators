import pandas as pd
from haversine import haversine, Unit


def loop_individual(data):
    individuals = data.individual.unique()
    for i in individuals:
        individual = data[data['individual'] == i]
        find_movement_window(individual)


def find_movement_window(individual):
    for x in individual.index:
        if (x <= 3):
            group = individual.iloc[0: 5]
        elif (x >= len(individual) - 2):
            group = individual.iloc[len(individual) - 5: len(individual)]

        else:
            group = individual.iloc[x-2: x+3]

        lat = group['st_y']
        long = group['st_x']

        distance_median = distance_to_x(
            individual.loc[x, 'st_y'], individual.loc[x, 'st_x'], lat.median(), long.median())

        """
        if (distance_median > 100000):
            print(distance_median)
            print(data.loc[x])


        """
        distance_mean = distance_to_x(
            individual.loc[x, 'st_y'], individual.loc[x, 'st_x'], lat.mean(), long.mean())
        if (distance_mean > 50000):
            print(distance_mean)
            print(x)
            new_coordiantes = generate_new_coordinates(x)
            print(generate_new_coordinates(x))
            data.loc[x, "st_y"] = new_coordiantes[0]
            data.loc[x, "st_x"] = new_coordiantes[1]
            print(data.loc[x])


def generate_new_coordinates(x):
    lat = (data.loc[x-1, 'st_y'] + data.loc[x-1, 'st_y'])/2
    long = (data.loc[x-1, 'st_x'] + data.loc[x-1, 'st_x'])/2
    return [lat, long]


def distance_to_x(x_lat, x_long, lat_median, long_median):
    t1 = (x_lat, x_long)
    t2 = (lat_median, long_median)
    return haversine(t1, t2, unit=Unit.METERS)


data = pd.read_csv('data/kaasa/kaasa_2021.csv')
print(loop_individual(data))
data.to_csv('data/kaasa/test.csv', index=False)
