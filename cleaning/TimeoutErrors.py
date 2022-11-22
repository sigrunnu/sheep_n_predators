import pandas as pd

data = pd.read_csv('data/clean_tingvoll/2012_koksvik_00048_2212.csv')

def count_number_of_timeouts(data):
    str_pattern = 'Time Out'
    
    # row by row check for the string pattern in the row values
    filt = (data.apply(lambda r: r.astype('string').str.contains(str_pattern).any(), axis=1))
    return data[filt].size

def count_number_of_timeouts_all_datasets():
    main = pd.read_csv('../data/tingvoll/informasjon_datasett_tingvoll.csv', sep=";")

    for x in main.index:
        name = main.loc[x, 'datasett']
        filename = '../data/clean_tingvoll/' + str(name) + '.csv'
        data = pd.read_csv(filename, sep='\t+', skiprows=[1, 2], engine='python', index_col=False)

        count = count_number_of_timeouts(data)
        print('Datasett: ' + name + '. Antall timeout: ' + str(count))


# Fix time out errors when the two adjacent points are not time out errors
def fix_timeout_errors(data):
    time_out = 'Time Out'
    for x in data.index:
        if data.loc[x, 'TTF'] == time_out:
            point_before = data.loc[x-1, 'TTF']
            point_after = data.loc[x+1, 'TTF']
            
            if point_before != time_out and point_after != time_out:
                lat_before = data.loc[x-1, 'Lat']
                long_before = data.loc[x-1, 'Long']
                lat_after = data.loc[x+1, 'Lat']
                long_after = data.loc[x+1, 'Long']

                lat_new = (lat_before + lat_after)/2
                long_new = (long_before + long_after)/2

                data.at[x, 'Lat'] = lat_new
                data.at[x, 'Long'] = long_new
                data.at[x, 'TTF'] = 0 
    return data

# Fix multiple timeout errors in a row
def fix_multiple_timeout_errors(data):
    pass

print(data.dtypes)
print(fix_timeout_errors(data))

#print(count_number_of_timeouts(data))
#count_number_of_timeouts_all_datasets()