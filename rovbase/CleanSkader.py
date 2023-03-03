from utils.Utm33ToLatLong import converter
import pandas as pd
import sys
sys.path.append('../')

'''
Clean rovviltskader
'''

df = pd.read_csv(
    '../data/rovbase/original/rovviltskader_meraker_2015-2022.csv')

# Join 'rase' and 'rase, annet'
df.loc[df['Rase, annet'].notna(), 'Rase'] = df['Rase, annet']

# Convert to lat and long
df1 = converter(df)

# Drop columns not needed
df1 = df1.loc[:, ['RovbaseID', 'Funnetdato', 'Rase', 'Skadedato, fra', 'Skadedato, til',
                  'Usikker skadedato', 'Alder', 'Tilstand', 'Skadeårsak', 'latitude', 'longitude']]

# Format dates and update column names
df1['Funnetdato'] = pd.to_datetime(df1["Funnetdato"],  dayfirst=True)
df1['Skadedato, fra'] = pd.to_datetime(df1['Skadedato, fra'],  dayfirst=True)
df1['Skadedato, til'] = pd.to_datetime(df1['Skadedato, til'],  dayfirst=True)
df1.rename(columns={'Skadedato, til': 'Skadedato_til', 'Skadedato, fra': 'Skadedato_fra', 'Skadeårsak': 'Skadearsak',
           'Funnetdato': 'Funnet_dato',  'Usikker skadedato': 'Usikker_skadedato'}, inplace=True)

# Removes rows with Skadeårsak = rødrev, sykdom, ikke rovvilt, hund, ulykke.


def remove_specific_skadearsak(data):
    words = ["Sykdom", "Ikke rovvilt", "Hund", "Ulykke"]
    for word in words:
        data.drop(data[(data['Skadearsak'] == word)].index, inplace=True)
    return data


#print(df1['Usikker skadedato'].value_counts())
# print(df1['Skadearsak'].value_counts())

df2 = remove_specific_skadearsak(df1)
df2.to_csv('../data/rovbase/rovviltskader.csv', index=False)
