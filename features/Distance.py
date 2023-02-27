import pandas as pd
from haversine import haversine, Unit

"""
Calculate distance travelled from one point to another in meters by using Haversine formula.
"""


def calculate_distance(lat1, long1, lat2, long2):
    t1 = (lat1, long1)
    t2 = (lat2, long2)
    return haversine(t1, t2, unit=Unit.METERS)


def add_distance(data):
    if not 'velocity' in data.columns:
        data['distance'] = 0
    data['date_time'] = pd.to_datetime(data['date_time'])
    for i in range(0, len(data)-1):
        long1 = data.loc[i, 'longitude']
        lat1 = data.loc[i, 'latitude']

        # Find time_difference between the two data points
        time_difference = (
            data.loc[i+1, 'date_time'] - data.loc[i, 'date_time']).total_seconds()

        long2 = data.loc[i+1, 'longitude']
        lat2 = data.loc[i+1, 'latitude']

        # If the time difference is more than 24 hours then the distance is set to 0
        distance = 0 if time_difference > 86400 else calculate_distance(
            lat1, long1, lat2, long2)

        data.loc[i+1, 'distance'] = round(distance, 1)

    return data
