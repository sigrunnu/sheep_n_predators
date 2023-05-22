
import numpy as np
import pandas as pd

"""
Adds sine and cosine values for time of day to a given DataFrame.

Parameters:
    df (pandas.DataFrame): The DataFrame to add the values to.

Returns:
    pandas.DataFrame: The updated DataFrame with sine and cosine values.
"""

def add_trig_time(df):
    # Convert date_time column to datetime type
    df['date_time'] = pd.to_datetime(df['date_time'])

    # Calculate minutes after midnight for each date time
    minutes_since_midnight = (
        df['date_time'] - df['date_time'].dt.normalize()).dt.total_seconds() / 60

    # Calculate sine and cosine values for time of day. 1440 is the number of minutes in 24 hours.
    df['sin_time'] = np.sin(
        2 * np.pi * minutes_since_midnight / 1440)
    df['cos_time'] = np.cos(
        2 * np.pi * minutes_since_midnight / 1440)

    return df

