"""
Removes rows with Skadeårsak = ukjent, rødrev, sykdom, ikke rovvilt, hund, ulykke. 
"""
def remove_specific_skadearsak(data):
    words = ["Ukjent", "Rødrev", "Sykdom", "Ikke rovvilt", "Hund", "Ulykke"]
    for word in words:
        data.drop(data[(data['Skadeårsak'] == word)].index)
    return data


#data2 = remove_specific_skadearsak(pd.read_csv('data/rovviltskader_meraker_2015-2022.csv'))
#data2.to_csv('data/rovviltskader_vasket.csv', encoding='utf-8', index=False)
