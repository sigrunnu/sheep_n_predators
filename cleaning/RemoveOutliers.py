import pandas as pd
from haversine import haversine, Unit


# Step 1. Group by individuals ad then find movement window. Grouping by individuals is done so other individuals wont affect the one sheeps movements.
def remove_outliers(data):
    individuals = data.individual.unique()
    for i in individuals:
        individual = data[data['individual'] == i]
        start_index = individual.first_valid_index()
        end_index = start_index + len(individual)
        find_movement_window(start_index, end_index, data)
    return data


def find_movement_window(start_index, end_index,  data):
    # Pick out the current row plus the 4 adjacent and find a movement window of five rows
    for x in range(start_index, end_index):
        if (x < start_index + 3):
            group = data.iloc[start_index: start_index + 5]
        elif (x >= end_index - 2):
            group = data.iloc[end_index - 5: end_index]
        else:
            group = data.iloc[x-2: x+3]

        lat = group['latitude']
        long = group['longitude']

        # Find out the mean of the time between each row
        date_time = pd.to_datetime(group['date_time']).reset_index(drop=True)
        time_diff = []
        for i in range(len(date_time)-1):
            diff = date_time[i]-date_time[i+1]
            time_diff.append(abs(diff.total_seconds()/3600))
        
        # mean_hours are used to find what the distance limit from x to the mean should be
        mean_hours = sum(time_diff)/5

        remove_outliers_median(x, lat.median(), long.median(), 100000, data)
        remove_outliers_mean(x, lat.mean(), long.mean(), data, mean_hours)


# Find and replace the outliers with a spesific distance to the median of the movement window
def remove_outliers_median(x, lat_median, long_median, distance_limit, data):
    distance_median = distance_to_x(
        data.loc[x, 'latitude'], data.loc[x, 'longitude'], lat_median, long_median)
    if (distance_median > distance_limit):
        print("The distance from x to the median is", distance_median)
        print("Date of current row", data.loc[x, 'date_time'])
        print("Individual of current row", data.loc[x, 'individual'])
        print('-------------------')
        generate_new_coordinates(x, data)


# Find and replace the outliers with a spesific distance to the mean of the movement window
def remove_outliers_mean(x, lat_mean, long_mean, data,  mean_hours):

    # find distance from x to the mean distance
    distance_mean = distance_to_x(
        data.loc[x, 'latitude'], data.loc[x, 'longitude'], lat_mean, long_mean)

    # Set the lowest limit to 15km/h * 1
    mean_hours = mean_hours if mean_hours > 1 else 1
    # Set the highest limit to 15km/h * 6
    mean_hours = 6 if mean_hours > 5 else mean_hours

    # The distance is found by multiplying 15 km/h with the number of hours between each point because a sheep can not run 15km/hour
    distance_limit = 15000 * mean_hours

    # If the distance is more than the limit set, then new coordinates are made for the data row
    if (distance_mean > distance_limit):
        print("The distance from x to the mean is", distance_mean)
        print("Date of current row", data.loc[x, 'date_time'])
        print("Individual of current row", data.loc[x, 'individual'])
        print('-------------------')
        generate_new_coordinates(x, data)


def generate_new_coordinates(x, data):
    # Generates new coordinates based on the mean of the two adjacent rows
    lat = (data.loc[x-1, 'latitude'] +
           data.loc[x+1, 'latitude'])/2
    long = (data.loc[x-1, 'longitude'] +
            data.loc[x + 1, 'longitude'])/2
    data.loc[x, "latitude"] = lat
    data.loc[x, "longitude"] = long


def distance_to_x(x_lat, x_long, lat_median, long_median):
    t1 = (x_lat, x_long)
    t2 = (lat_median, long_median)
    return haversine(t1, t2, unit=Unit.METERS)
