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

        remove_outliers_median(
            individual, x, lat.median(), long.median(), 100000)
        #remove_outliers_mean(individual, x, lat.mean(), long.mean(), 50000)


def remove_outliers_median(individual, x, lat_median, long_median, value):
    distance_median = distance_to_x(
        individual.loc[x, 'st_y'], individual.loc[x, 'st_x'], lat_median, long_median)
    if (distance_median > value):
        print(distance_median)
        print(x)
        print(data.loc[x])
        new_coordinates = generate_new_coordinates(x)
        print(new_coordinates)


def remove_outliers_mean(individual, x, lat_mean, long_mean, value):
    distance_mean = distance_to_x(
        individual.loc[x, 'st_y'], individual.loc[x, 'st_x'], lat_mean, long_mean)
    if (distance_mean > value):
        print(distance_mean)
        print(x)
        new_coordinates = generate_new_coordinates(x)
        print(generate_new_coordinates(x))
        data.loc[x, "st_y"] = new_coordinates[0]
        data.loc[x, "st_x"] = new_coordinates[1]
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
