import pandas as pd

data = pd.read_csv('../data/clean_tingvoll/2012_koksvik_7030_2225.csv', sep='\t+', skiprows=[1, 2], engine='python', index_col=False)

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


def fix_timeout_errors(data):
    pass

#print(count_number_of_timeouts(data))
#count_number_of_timeouts_all_datasets()