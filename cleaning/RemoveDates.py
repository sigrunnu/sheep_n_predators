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



# Get date values for individual
def get_date_values(i_data):
    dates = pd.to_datetime(i_data['date_time']).dt.date # get only date and not time stamp
    dates_unique = dates.unique()
    first_date = dates.min()
    end_date = dates.max()
    return dates_unique, first_date, end_date


# Return list with missing dates
def missing_dates(dates_unique, first_date, end_date):
    return pd.date_range(start=first_date, end=end_date).difference(dates_unique)


"""
Check if each sheep have any missing date-values, and if they have over 10 missing values - delete the sheep.
"""
def delete_sheep_with_missing_dates(df):
    individuals = df.individual.unique() # list of individuals
    count_individual_w_missing_dates = 0
    occur_missing_dates = dict()
    
    for ind in individuals:
        i_data = df[df['individual'] == ind]
        dates_unique1, first_date1, end_date1 = get_date_values(i_data) # get date values to be used
        missing_dates1 = missing_dates(dates_unique1, first_date1, end_date1) # return list with missing dates
        
        if len(missing_dates1) > 0:
            print('For individ', ind, 'mangler følgende datoer: ', missing_dates1, '. Antall: ', len(missing_dates1))
            print('-------------------------------------------------------------------------------------------------')
            count_individual_w_missing_dates += 1
            occur_missing_dates[ind] = len(missing_dates1)

    print('Antall individer med missing dates: ', count_individual_w_missing_dates)

    for x in occur_missing_dates:
        print('Individ: ', x, 'mangler ', occur_missing_dates[x], 'datoer')
        # If sheep has more than ten missing days, delete the sheep
        if occur_missing_dates[x] >= 10:
            ind_index = df[df['individual'] == x].index
            df.drop(ind_index, inplace=True)
            print('Deleted individual: ', x, 'and ', len(ind_index), 'rows')
    
    return df


def delete_sheep_if_less_than_15_dates(df):
    individuals = df.individual.unique() # list of individuals

    for ind in individuals: 
        i_data = df[df['individual'] == ind]
        dates_unique1, first_date1, end_date1 = get_date_values(i_data) # get date values to be used

        # If sheep has less than 15 dates - delete the sheep 
        if len(dates_unique1) < 15:
            print('Delete individual', ind, 'with only', len(dates_unique1), 'dates')
            df.drop(i_data.index, inplace=True)
    
    return df

data = pd.read_csv('data/kaasa/kaasa_2020.csv')

new = delete_sheep_with_missing_dates(data)
new1 = delete_sheep_if_less_than_15_dates(data)
#new1.to_csv('data/kaasa/kaasa_2020.csv', index=False)
