"""
Removes rows with Skadeårsak = ukjent, rødrev, sykdom, ikke rovvilt, hund, ulykke. 
"""
def remove_specific_skadearsak(data):
    words = ["Ukjent", "Rødrev", "Sykdom", "Ikke rovvilt", "Hund", "Ulykke"]
    for word in words:
        data.drop(data[(data['Skadeårsak'] == word)].index, inplace=True)
    return data
