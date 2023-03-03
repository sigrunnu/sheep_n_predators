
from utils.Utm33ToLatLong import converter
import pandas as pd
import sys
sys.path.append('../')

'''
Clean rovviltobservasjoner
'''

df = pd.read_csv(
    '../data/rovbase/original/rovviltobservasjoner_meraker_2015-2022.csv')

# Convert to lat and long
df1 = converter(df)

# Drop columns not needed
df1 = df1.loc[:, ['RovbaseID', 'Art', 'Totalt antall',
                  'Aktivitetsdato, fra', 'Aktivitetsdato, til', 'latitude', 'longitude']]

# Format dates and update column names
df1['Aktivitetsdato, fra'] = pd.to_datetime(
    df1['Aktivitetsdato, fra'],  dayfirst=True)
df1['Aktivitetsdato, til'] = pd.to_datetime(
    df1['Aktivitetsdato, til'],  dayfirst=True)
df1.rename(columns={'Aktivitetsdato, fra': 'Aktivitetsdato_fra',
           'Aktivitetsdato, til': 'Aktivitetsdato_til', 'Totalt antall': 'Totalt_antall'}, inplace=True)

#print(df['Usikker skadedato'].value_counts())

df1.to_csv('../data/rovbase/rovviltobservasjoner.csv', index=False)
