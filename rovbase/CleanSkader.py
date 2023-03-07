import pandas as pd
import numpy as np
"""
from utils.Utm33ToLatLong import converter
import sys
sys.path.append('../')
"""



def cleanSkader(df):
    # Join 'rase' and 'rase, annet'
    df.loc[df['Rase, annet'].notna(), 'Rase'] = df['Rase, annet']

    # Convert to lat and long
    #df1 = converter(df)

    # Drop columns not needed
    df1 = df1.loc[:, ['RovbaseID', 'Funnetdato', 'Rase', 'Skadedato, fra', 'Skadedato, til',
                    'Usikker skadedato', 'Alder', 'Tilstand', 'Skadeårsak', 'latitude', 'longitude']]

    # Format dates and update column names
    df1['Funnetdato'] = pd.to_datetime(df1["Funnetdato"],  dayfirst=True)
    df1['Skadedato, fra'] = pd.to_datetime(df1['Skadedato, fra'],  dayfirst=True)
    df1['Skadedato, til'] = pd.to_datetime(df1['Skadedato, til'],  dayfirst=True)
    df1.rename(columns={'Skadedato, til': 'Skadedato_til', 'Skadedato, fra': 'Skadedato_fra', 'Skadeårsak': 'Skadearsak',
            'Funnetdato': 'Funnet_dato',  'Usikker skadedato': 'Usikker_skadedato'}, inplace=True)
    
    df2 = df1.sort_values(by=['Skadedato_fra'])
    df3 = remove_specific_skadearsak(df2)

    return df3



# Removes rows with Skadeårsak = sykdom, ikke rovvilt, hund, ulykke.
def remove_specific_skadearsak(data):
    words = ["Sykdom", "Ikke rovvilt", "Hund", "Ulykke"]
    for word in words:
        data.drop(data[(data['Skadearsak'] == word)].index, inplace=True)
    return data


# Remove attacks that last more than 3 days.
def removeAttacks(df):
    df['Skadedato_fra'] = pd.to_datetime(df['Skadedato_fra'])
    df['Skadedato_til'] = pd.to_datetime(df['Skadedato_til'])

    for x in df.index:
        start_date = df.at[x, 'Skadedato_fra']
        end_date = df.at[x, 'Skadedato_til']

        diff_days = (end_date - start_date) / np.timedelta64(1, 'D')

        if diff_days >= 3:
            df.drop(x, inplace=True)
            count += 1
    
    return df

df = pd.read_csv('data/rovbase/rovviltskader.csv')
df1 = removeAttacks(df)
df1.to_csv('data/rovbase/rovviltskader.csv', index=False)

