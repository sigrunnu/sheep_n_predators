
import numpy as np
import pandas as pd
import plotly.express as px


def add_trig_time(df):
    """
    Adds sine and cosine values for time of day to a given DataFrame.

    Parameters:
        df (pandas.DataFrame): The DataFrame to add the values to.

    Returns:
        pandas.DataFrame: The updated DataFrame with sine and cosine values.
    """
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


# Read data from file
data_file = 'data/kaasa/kaasa_2021.csv'
df = pd.read_csv(data_file)

# Add sine and cosine values to data
df = add_trig_time(df)

fig = px.scatter(df.sample(100), x='sin_time', y='cos_time')

# Set the axis labels and title
fig.update_layout(
    xaxis_title='Sine time',
    yaxis_title='Cosine time',
    width=400,
    height=400
)

# Show the plot
fig.show()
