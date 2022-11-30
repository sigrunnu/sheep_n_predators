import pandas as pd
from RemoveDuplicates import remove_duplicates
from CleanKaasa import clean_individual_nr_not_null, change_dtypes, match_source_id_to_individual


def iterate_over_all_files():
    files = ['kaasa_2021.csv', 'kaasa_2020.csv', 'kaasa_2019.csv',
             'kaasa_2018.csv', 'kaasa_2017.csv', 'kaasa_2016.csv', 'kaasa_2015.csv']

    for file in files:
        filepath = 'data/kaasa/' + str(file)
        data = pd.read_csv(filepath)

        if not data.empty:
            new = remove_duplicates(data) #DONE
            new2 = clean_individual_nr_not_null(new) #DONE
            new3 = change_dtypes(new2) #DONE 
            new4 = match_source_id_to_individual(new3) #DONE
            new5 = new4.sort_values(by=['individual', 'date_time']) #DONE

            if not new5.empty:
                new5.to_csv(filepath, index=False)
                print('Lagret til fil:', file)


iterate_over_all_files()
