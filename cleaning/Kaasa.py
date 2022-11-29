import pandas as pd
from RemoveDuplicates import remove_duplicates
from kaasa_convert import convert, change_dtypes


def iterate_over_all_files():
    files = ['kaasa_2021.csv', 'kaasa_2020.csv', 'kaasa_2019.csv',
             'kaasa_2018.csv', 'kaasa_2017.csv', 'kaasa_2016.csv', 'kaasa_2015.csv']

    for file in files:
        filepath = 'data/kaasa/' + str(file)
        data = pd.read_csv(filepath)

        if not data.empty:
            new = remove_duplicates(data)
            new2 = convert(new)
            new3 = change_dtypes(new2)
            new4 = new3.sort_values(by=['individual', 'date_time'])

            if not new4.empty:
                new4.to_csv(filepath, index=False)
                print('Lagret til fil:', file)


iterate_over_all_files()
