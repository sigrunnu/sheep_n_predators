import pandas as pd
from Distance import add_distance

def distance_traveled_day(data):
    dates = []
    total_dists = []
    
    for x in data.index:
        date = data.loc[x, 'Date']
        
        if date not in dates:
            dates.append(date)
    
    for date in dates:
        total_dist = data.loc[data['Date'] == date, 'distance'].sum()
        total_dists.append(total_dist)
    
    return pd.DataFrame(total_dists, index=dates, columns=["day_distance"])


#data = pd.read_csv('data/clean_tingvoll/2012_koksvik_00022_2201.csv') 
#data = add_distance(data)
#print(distance_traveled_day(data))