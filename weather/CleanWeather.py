import pandas as pd
import numpy as np
import datetime

# Add temperature for every 30 minutes instead of 1 hours.
# Only used if sheep data has 30 minute intervals


data = pd.read_csv('weatherData/2012.csv', sep=';')

data['Tid(norsk normaltid)'] = pd.to_datetime(
    data['Tid(norsk normaltid)'], dayfirst=True)

data['Lufttemperatur'] = data['Lufttemperatur'].str.replace(",", ".")

# Add extra row every second row which contains the mean of the previous and next temperature
for i in range(0, len(data)*2-1, 2):

    # Copy row
    x = data.loc[[i]]

    # Add 45 minutes to the new row
    x['Tid(norsk normaltid)'] = x['Tid(norsk normaltid)'] + \
        datetime.timedelta(minutes=45)

    # Add fifteen minutes extra to the current row
    data.at[i, 'Tid(norsk normaltid)'] = data.at[i, 'Tid(norsk normaltid)'] + \
        datetime.timedelta(minutes=15)
    current_temp = float(data.loc[i, 'Lufttemperatur'])

    # Calculate new temperature
    if (i != len(data)-1):
        next_temp = float(data.loc[i + 1, 'Lufttemperatur'])
        x['Lufttemperatur'] = round((current_temp + next_temp)/2, 1)
    else:
        current_temp = float(data.loc[i, 'Lufttemperatur'])
        next_temp = float(data.loc[i - 1, 'Lufttemperatur'])
        x['Lufttemperatur'] = round((current_temp + next_temp)/2, 1)

    # Add the new row
    data = pd.concat([data.iloc[:i+1], x, data.iloc[i+1:]]
                     ).reset_index(drop=True)


data.to_csv('weatherData/2012_clean.csv', index=False)
print(data.head(50))
