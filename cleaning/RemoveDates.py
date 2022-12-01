import pandas as pd

import warnings
warnings.filterwarnings("ignore")

"""
Remove dates where the sheep is not out on the pastures. 
Return data if dates are correct, if not, skip frame and inspect manually.
"""
def remove_dates_where_sheep_not_on_pastures(data, filename, start, end):
    start = pd.to_datetime(start, dayfirst=True)
    end = pd.to_datetime(end, dayfirst=True)

    try: 
        data['Date'] = pd.to_datetime(data['date_time'], yearfirst=True)

        for x in data.index:
            #date = data.loc[x, 'Date'] # if date and time is splitted
            #time = data.loc[x, 'Time'] # if date and time is splitted
            #full_date = f'{date} {time}' # if date and time is splitted
            date_time = data.loc[x, 'date_time']

            parsed_date = pd.to_datetime(date_time)
            if parsed_date < start or parsed_date > end:
                print("Droppet:",  parsed_date)
                data.drop(x, inplace=True)
        print('Ferdig med: ' + filename)
        return data

    except Exception as e:
        print('Skippet dataset: ' + filename)
        print(e)
        return pd.DataFrame() # return empty dataframe


#data = pd.read_csv('data/kaasa/kaasa_2021.csv')
#new = remove_dates_where_sheep_not_on_pastures(data, 'kaasa_2021.csv', '2021-05-28 15:43:37', '01.10.2021  23:59:59')
#print(new)
