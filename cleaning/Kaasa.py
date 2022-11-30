import pandas as pd
from RemoveDuplicates import remove_duplicates
from CleanKaasa import match_source_id_to_individual, remove_sheep_with_less_than_10_points
from FormatKaasa import replace_individual_nr_with_null_values, change_dtypes

def iterate_over_all_files():
    files = ['kaasa_2021.csv', 'kaasa_2020.csv', 'kaasa_2019.csv',
             'kaasa_2018.csv', 'kaasa_2017.csv', 'kaasa_2016.csv', 'kaasa_2015.csv']

    for file in files:
        filepath = 'data/kaasa/' + str(file)
        data = pd.read_csv(filepath)

        if not data.empty:
            #new = remove_duplicates(data) #DONE
            #new2 = replace_individual_nr_with_null_values(new) #DONE
            #new3 = change_dtypes(new2) #DONE 
            #new4 = match_source_id_to_individual(new3) #DONE
            #new5 = remove_sheep_with_less_than_10_points(data) #DONE
            new6 = data.sort_values(by=['individual', 'date_time']) #DONE

            if not new6.empty:
                new6.to_csv(filepath, index=False)
                print('Lagret til fil:', file)


#iterate_over_all_files()
