import pandas as pd

import warnings
warnings.filterwarnings("ignore")

data = pd.read_csv('data/rovviltskader_vasket.csv')

# Remove where skadedato is usikker
def remove_skadedato_uncertain(data):
    return data.loc[data["Usikker skadedato"] == "Nei"]

# Remove skadedato where skadedato, til and skadedato, fra is not the same 
def remove_skadedato_not_one_date(data):
    for x in data.index:
        skadedato_from = data.loc[x, "Skadedato, fra"]
        skadedato_to = data.loc[x, "Skadedato, til"]
        
        if skadedato_from != skadedato_to:
            data.drop(x, inplace=True)
    
    return data

def remove_skadedato_uncertain_and_not_one_date(data):
    data1 = remove_skadedato_uncertain(data)
    data2 = remove_skadedato_not_one_date(data1)
    return data2

data = remove_skadedato_uncertain_and_not_one_date(data)
data.to_csv('rovviltskader_sikker_en_dato_meraker_2015-2022.csv', index=False)

