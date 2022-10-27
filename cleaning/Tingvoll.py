import pandas as pd
from RemoveDates import remove_dates_where_sheep_not_on_pastures

"""
Iterate over every dataset and do cleaning.
"""
def iterate_over_all_files():
    main = pd.read_csv('../data/tingvoll/informasjon_datasett_tingvoll.csv', sep=";")
    
    for x in main.index:
       start_date =  main.loc[x, 'Start']
       end_date = main.loc[x, 'Slutt']
       name = main.loc[x, 'datasett']
       
       filename = '../data/tingvoll/' + str(name) + '.csv'

       data = pd.read_csv(filename, sep='\t+', skiprows=[1, 2], engine='python', index_col=False)

       if not data.empty:
        # Add more here afterwards when cleaning-functions are ready
        new = remove_dates_where_sheep_not_on_pastures(data, name, start_date, end_date)
        if not new.empty:
            path_to_save = '../data/clean_tingvoll/' + str(name) + '.csv'
            new.to_csv(path_to_save, index=False)
        
#iterate_over_all_files()