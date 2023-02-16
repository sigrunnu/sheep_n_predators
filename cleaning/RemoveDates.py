import pandas as pd

import warnings
warnings.filterwarnings("ignore")

"""
Remove dates where the sheep is not out on the pastures. Args is dates. 
Return data if dates are correct, if not, skip frame and inspect manually.
"""
def remove_dates_where_sheep_not_on_pastures(data, filename, start, end):
    start = pd.to_datetime(start, dayfirst=True)
    end = pd.to_datetime(end, dayfirst=True)

    num_removed = 0

    try: 
        data['date_time'] = pd.to_datetime(data['date_time'], yearfirst=True)

        for x in data.index:
            #date = data.loc[x, 'Date'] # if date and time is splitted
            #time = data.loc[x, 'Time'] # if date and time is splitted
            #full_date = f'{date} {time}' # if date and time is splitted
            date_time = data.at[x, 'date_time']

            if date_time < start or date_time > end:
                print("Droppet:",  date_time)
                data.drop(x, inplace=True)
                num_removed += 1
        print('Ferdig med: ' + filename)
        print('Antall rader fjernet: ', num_removed)
        return data

    except Exception as e:
        print('Skippet dataset: ' + filename)
        print(e)
        return pd.DataFrame() # return empty dataframe


"""
Remove all data from oct - june.
"""
def remove_rows_from_oct_to_jun(data):
    data['date_time'] = pd.to_datetime(data['date_time'], yearfirst=True)

    filter = data[(data['date_time'].dt.month == 6) | # juni
                  (data['date_time'].dt.month == 7) | # juli
                  (data['date_time'].dt.month == 8) | # august
                  (data['date_time'].dt.month == 9)] # september
    
    print('Antall rader slettet: ', len(data) - len(filter))
    return filter


