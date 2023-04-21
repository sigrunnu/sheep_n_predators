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
    # df1 = converter(df)

    # Drop columns not needed
    df1 = df.loc[:, ['RovbaseID', 'Funnetdato', 'Rase', 'Skadedato, fra', 'Skadedato, til',
                    'Usikker skadedato', 'Skadeårsak', 'latitude', 'longitude']]

    # Format dates and update column names
    df1['Funnetdato'] = pd.to_datetime(df1["Funnetdato"],  dayfirst=True)
    df1['Skadedato, fra'] = pd.to_datetime(df1['Skadedato, fra'],  dayfirst=True)
    df1['Skadedato, til'] = pd.to_datetime(df1['Skadedato, til'],  dayfirst=True)
    df1 = translateToEnglish(df1)
    
    df2 = df1.sort_values(by=['date_from'])
    df3 = remove_specific_skadearsak(df2)

    return df3



# Removes rows with Skadeårsak = sykdom, ikke rovvilt, hund, ulykke.
def remove_specific_skadearsak(data):
    words = ["Disease", "Not predator", "Dog", "Accident"]
    for word in words:
        data.drop(data[(data['Predator'] == word)].index, inplace=True)
    return data


# Remove attacks that last more than 3 days.
def removeAttacks(df):
    df['date_from'] = pd.to_datetime(df['date_from'])
    df['date_to'] = pd.to_datetime(df['date_to'])

    for x in df.index:
        start_date = df.at[x, 'date_from']
        end_date = df.at[x, 'date_to']

        diff_days = (end_date - start_date) / np.timedelta64(1, 'D')

        if diff_days >= 3:
            df.drop(x, inplace=True)
            count += 1
    
    return df

def translateToEnglish(df):
    # Translate column names
    df.rename(columns={'Skadedato, til': 'date_to', 'Skadedato, fra': 'date_from', 'Skadeårsak': 'predator',
            'Funnetdato': 'date_found',  'Usikker skadedato': 'date_uncertain', 'Rase': 'sheep_breed'}, inplace=True)
    
    predators = {'Bjørn': 'Bear', 'Jerv': 'Wolverine', 'Ukjent':'Unknown', 'Ulv': 'Wolf', 'Rødrev': 'Red Fox', 'Sykdom': 'Disease', 'Ukjent fredet rovvilt': 'Unknown protected predator', 
                 'Ikke rovvilt': 'Not predator', 'Gaupe': 'Lynx', 'Kongeørn': 'Golden Eagle', 'Hund': 'Dog', 'Ulykke': 'Accident'}
    
    answers = {'Ja': 'Yes', 'Nei': 'No'}

    df1 = df.replace(predators)
    df2 = df1.replace(answers)
    
    return df2


#df = pd.read_csv('data/rovbase/original/rovviltskader_meraker_2015-2021.csv')
#df1 = claenSkader(df)
#df1 = removeAttacks(df)
#df1.to_csv('data/rovbase/rovviltskader.csv', index=False)

df = pd.read_csv('data/rovbase/original/rovviltskader_meraker_2015-2021.csv')
df1 = translateToEnglish(df)
df1.to_csv('data/rovbase/original/rovviltskader_meraker_2015-2021.csv', index=False)
