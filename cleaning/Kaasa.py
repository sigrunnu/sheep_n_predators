import pandas as pd
from RemoveDuplicates import remove_duplicates

def iterate_over_all_files():
    files = ['kaasa_2021.csv', 'kaasa_2020.csv', 'kaasa_2019.csv', 'kaasa_2018.csv', 'kaasa_2017.csv', 'kaasa_2016.csv', 'kaasa_2015.csv']
     
    for file in files:
        filepath = 'data/kaasa/' + str(file)
        data = pd.read_csv(filepath)

        if not data.empty:
            new = remove_duplicates(data)

            if not new.empty:
                new.to_csv(filepath, index=False)
                print('Lagret til fil:', file)


iterate_over_all_files()
        