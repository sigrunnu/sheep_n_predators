import datetime
import pandas as pd
from haversine import haversine, Unit
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

# Counts how many rows that are being removed
total_deleted = 0

# If the sheep do not leave the farm before this date - print a message
limit_first_date = pd.to_datetime('2019-07-11')

# If the sheep is back at the farm before this date - print a message
limit_last_date = pd.to_datetime('2019-08-01')

never_left = True


'''
Loops trough the whole dataframe and extracts each individual sheep
creates a new dataframe which do not contain the rows where the sheep are on the farm 
'''
def main(data):
    individuals = data.individual.unique()
    total_data = pd.DataFrame()

    for i in individuals:
        i_data = data[data['individual'] == i]
        i_not_on_farm_data = sheep_on_farm(i_data)
        total_data = pd.concat([total_data, i_not_on_farm_data])
    print("Total deleted rows:", total_deleted)
    return total_data


'''
Loops trough each individual to find out when the sheep leave for pasture and when it comes back
'''
def sheep_on_farm(i_data):
    global never_left
    never_left = True
    i_data['date_time'] = pd.to_datetime(i_data['date_time'])

    first_date_1, index = find_first_date(i_data, i_data.first_valid_index())
    last_date_1, last_date_i = find_last_date(i_data, index)

    first_date_1 = pd.to_datetime(first_date_1)
    last_date_1 = pd.to_datetime(last_date_1)

    # Check if the first date is after the set limit
    if (first_date_1 >= limit_first_date):
        print("This individual exceeded limit for first date:",
              i_data.loc[i_data.first_valid_index(), 'individual'])
        print('First date it left the farm:', first_date_1)

    # Check if the last date is before the limit AND that the last date is not the last row in that individual
    if ((last_date_1 <= limit_last_date) & (last_date_i + 1 < i_data.index[-1])):
        second_first_date, index_2 = find_first_date(i_data, last_date_i)

        # Run find_first_date again with the index of last date to see if the sheep ever return from the farm
        if (pd.to_datetime(second_first_date).date() != pd.to_datetime(last_date_1).date()):

            # If the sheep does return from the farm, print these messages to inspect them manually
            print("This individual exceeded limit for last date:",
                  i_data.loc[i_data.first_valid_index(), 'individual'])
            print('First date:', first_date_1)
            print('Last date:', last_date_1)
            print('Second first date:', second_first_date)

    # Drop all rows that are before the first date that the sheep leave the farm
    drop_group_1 = i_data[i_data['date_time'] <=
                          first_date_1].index

    # Drop all rows that are after the last date that the sheep are on pasture
    drop_group_2 = i_data[i_data['date_time'] >=
                          last_date_1].index
    global total_deleted

    # If the sheep never left the farm then the whole individual is deleted
    if (never_left):
        print("Never left",
              i_data.loc[i_data.first_valid_index(), 'individual'])
        total_deleted += len(i_data)
        return pd.DataFrame()

    total_deleted += len(drop_group_2) + len(drop_group_1)
    i_data.drop(drop_group_1, inplace=True)
    i_data.drop(drop_group_2, inplace=True)

    return i_data


def find_first_date(i_data, index):
    first_i = i_data.first_valid_index()
    first_date = i_data.loc[index, 'date_time']

    for i in range(index, first_i + len(i_data)-1):
        lat = i_data.loc[i, 'latitude']
        long = i_data.loc[i, 'longitude']
        dis = distance_to_x(center_farm_lat, center_farm_long, lat, long)
        if (dis > 1500):
            first_date = i_data.loc[i, 'date_time']
            global never_left
            never_left = False
            break

    return first_date, i


def find_last_date(i_data, index):
    first_i = i_data.first_valid_index()
    last_date = i_data.loc[first_i + len(i_data)-1, 'date_time']

    for i in range(index, first_i + len(i_data)-1):
        lat = i_data.loc[i, 'latitude']
        long = i_data.loc[i, 'longitude']
        dis = distance_to_x(center_farm_lat, center_farm_long, lat, long)

        if (dis < 1500):
            last_date = i_data.loc[i, 'date_time']
            break

    return last_date, i


def distance_to_x(x_lat, x_long, lat_median, long_median):
    t1 = (x_lat, x_long)
    t2 = (lat_median, long_median)
    return haversine(t1, t2, unit=Unit.METERS)


# Calculated center of the farm based on a density map
center_farm_lat = 63.4026
center_farm_long = 11.7167
