import pandas as pd

# Return number of signals (plinger) for each date. Returns Dataframe with two column: date and num_occur
def nr_occurances_each_date(i_data):
    dates = pd.to_datetime(i_data['date_time']).dt.date # get only date and not time stamp
    occur = dates.value_counts().to_frame(name='occur')
    occur = occur.rename_axis('date').reset_index(level=0) # rename index-axis to date, before converting it to a column and adding new index with numbers
    return occur


# Retur number of occurances for each timestamp
def nr_occurances_each_timestamp(i_data):
    timestamps = pd.to_datetime(i_data['date_time']).dt.time # get only time and not date
    occur = timestamps.value_counts().to_frame(name='num_occur')
    return occur


# Standarize timestamps to nearest hour
def standarize_timestamp(df):
    for x in df.index:
        date = pd.to_datetime(df.at[x, 'date_time'])
        hour = date.hour
        minutes = date.minute
        if minutes > 30:
            if hour != 23:
                hour += 1
            else:
                hour = 0
        df.at[x, 'date_time'] = date.replace(hour=hour, minute=00, second=0, microsecond=0)

    return df