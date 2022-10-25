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
        data['Date'] = pd.to_datetime(data['Date'], yearfirst=True)

        for x in data.index:
            date = data.loc[x, 'Date']
            time = data.loc[x, 'Time']
            full_date = f'{date} {time}'

            parsed_date = pd.to_datetime(full_date)
            if parsed_date < start or parsed_date > end:
                data.drop(x, inplace=True)
        print('Ferdig med: ' + filename)
        return data

    except Exception as e:
        print('Skippet dataset: ' + filename)
        print(e)
        return pd.DataFrame() # return empty dataframe


#data = pd.read_csv('../data/tingvoll/2013_torjul_90075_2203.csv', sep='\t+', skiprows=[1, 2], engine='python', index_col=False)
#new = remove_dates_where_sheep_not_on_pastures(data, '2013_torjul_90075_2203.csv', '16.06.2013  00:15:00', '25.08.2013  23:45:00')

