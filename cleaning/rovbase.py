import numpy as np
import pandas as pd

data = pd.read_csv('data/rovviltskader_meraker_2015-2022.csv')

# Removes rows with Skadeårsak = ukjent, rødrev, sykdom, ikke rovvilt, hund, ulykke. 
def remove_specific_skadearsak(data):
    words = ["Ukjent", "Rødrev", "Sykdom", "Ikke rovvilt", "Hund", "Ulykke"]
    for word in words:
        data.drop(data[(data['Skadeårsak'] == word)].index, inplace=True)
    return data

# Format date fields
def format_date(data):
    data['Funnetdato'] = pd.to_datetime(data["Funnetdato"])
    data['Skadedato, fra'] = pd.to_datetime(data["Skadedato, fra"])
    data['Skadedato, til'] = pd.to_datetime(data["Skadedato, til"])

    return data


# Might use later. Remove rows with empty or invalid position.
def remove_rows_with_empty_position(data):
    for x in data.index: 
        if np.isnan(data.loc[x, "Lengdegrad"]) or np.isnan(data.loc[x, "Breddegrad"]):
            data.drop(x, inplace=True)

data = remove_specific_skadearsak(data)
data = format_date(data)
data.to_csv("rovviltskader_vasket.csv", index = False)