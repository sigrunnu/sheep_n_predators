import pandas as pd
"""
Calculate the velocity of the sheep based on the calculated distance and time interval between data points
"""


def add_velocity(data):
    if not 'velocity' in data.columns:
        data['velocity'] = 0.0
    data['date_time'] = pd.to_datetime(data['date_time'])
    for i in range(0, len(data)-1):
        distance = data.loc[i+1, 'distance']

        # time difference in hours
        time_difference = (
            data.loc[i+1, 'date_time'] - data.loc[i, 'date_time']).total_seconds()/3600

        # If time-difference is less than 15 minutes then time-difference is set to 0.5 as the number gets really high when dividing it by a small number.
        if (time_difference < 0.25):
            velocity = round(
                distance / 0.5, 0)
        elif (distance == 0.0):
            velocity = 0
        else:
            velocity = round(
                distance / time_difference, 0)

        # meters walked divided by time used is m/h. If distance is 0 then velocity is also 0.
        data.loc[i+1, 'velocity'] = velocity

    return data
