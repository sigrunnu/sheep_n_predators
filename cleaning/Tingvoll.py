import pandas as pd
from RemoveDates import remove_dates_where_sheep_not_on_pastures

"""
Iterate over every dataset and do cleaning.
"""
def iterate_over_all_files():
    main = pd.read_csv('data/tingvoll/informasjon_datasett_tingvoll.csv', sep=";")
    
    for x in main.index:
       start_date =  main.loc[x, 'Start']
       end_date = main.loc[x, 'Slutt']
       name = main.loc[x, 'datasett']
       
       # Kan bruke clean_data-mappen i stedet da den er riktig format
       filename = 'data/clean_tingvoll/' + str(name) + '.csv'

       #data = pd.read_csv(filename, sep='\t+', skiprows=[1, 2], engine='python', index_col=False)
       data = pd.read_csv(filename)

       if not data.empty:
        # Add more here afterwards when cleaning-functions are ready
        new1 = remove_dates_where_sheep_not_on_pastures(data, name, start_date, end_date)
        new2 = remove_unnecessary_columns(new1, filename)

        if not new2.empty:
            path_to_save = 'data/clean_tingvoll/' + str(name) + '.csv'
            new2.to_csv(path_to_save, index=False)
        
def remove_unnecessary_columns(data, filename):
    try: 
        return data.drop(['Alt', '2D3D', 'FOM', 'DOP', 'Bat', 'SVs','Status', 'SCap', 'GPS', 'GSM'], axis=1)
    except Exception as e:
        print("Skippet datasett:", filename)
        print(e)
        return pd.DataFrame()

#data = pd.read_csv('data/clean_tingvoll/2012_koksvik_00022_2201.csv')
iterate_over_all_files()