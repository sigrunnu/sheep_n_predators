import numpy as np

"""
Removes rows with Skadeårsak = ukjent, rødrev, sykdom, ikke rovvilt, hund, ulykke. 
"""
def remove_specific_skadearsak(data):
    words = ["Ukjent", "Rødrev", "Sykdom", "Ikke rovvilt", "Hund", "Ulykke"]
    for word in words:
        data.drop(data[(data['Skadeårsak'] == word)].index, inplace=True)
    return data


"""
Might use later. Remove rows with empty or invalid position.
"""
def remove_rows_with_empty_position(data):
    for x in data.index: 
        if np.isnan(data.loc[x, "Lengdegrad"]) or np.isnan(data.loc[x, "Breddegrad"]):
            data.drop(x, inplace=True)