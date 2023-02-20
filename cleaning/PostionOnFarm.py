import datetime
import pandas as pd
from haversine import haversine, Unit
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")


total_deleted = 0
limit_first_date = pd.to_datetime('2015-07-11')
limit_last_date = pd.to_datetime('2015-08-01')


def main(data):
    individuals = data.individual.unique()
    total_data = pd.DataFrame()

    for i in individuals:
        i_data = data[data['individual'] == i]
        i_not_on_farm_data = sheep_on_farm(i_data)
        total_data = pd.concat([total_data, i_not_on_farm_data])
    print("Total deleted rows:", total_deleted)
    return total_data


def sheep_on_farm(i_data):
    i_data['date_time'] = pd.to_datetime(i_data['date_time'])
    first_date_1, index = find_first_date(i_data, i_data.first_valid_index())
    last_date_1, last_date_i = find_last_date(i_data, index)

    first_date_1 = pd.to_datetime(first_date_1)
    last_date_1 = pd.to_datetime(last_date_1)

    # Check if the first date is after 01.07 - then sheep most likeley never left the farm
    if (first_date_1 >= limit_first_date):
        print("Exceeded limit for first date:",
              i_data.loc[i_data.first_valid_index(), 'individual'])
        print('first adte', first_date_1)

    # If the last date is before 01.08 then check if that data point is not the last of that sheep
    if ((last_date_1 <= limit_last_date) & (last_date_i + 1 < i_data.index[-1])):
        second_last_date, index_2 = find_first_date(i_data, last_date_i)
        # Run find_first_date again to see if the sheep ever return from the farm
        if (pd.to_datetime(second_last_date).date() != pd.to_datetime(last_date_1).date()):
            print("Exceeded limit for last date:",
                  i_data.loc[i_data.first_valid_index(), 'individual'])
            print('last adte', last_date_1)
            print('first adte', first_date_1)
            print('second first date', second_last_date)

    drop_group_1 = i_data[i_data['date_time'] <=
                          first_date_1].index

    drop_group_2 = i_data[i_data['date_time'] >=
                          last_date_1].index

    global total_deleted
    total_deleted += drop_group_2.size + drop_group_1.size

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


center_farm_lat = 63.4026
center_farm_long = 11.7167

df = pd.read_csv('data/kaasa/kaasa_2015.csv')
new_data = main(df)
new_data.to_csv('test.csv', index=False)
