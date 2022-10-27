import pandas as pd
from haversine import haversine

"""
Calculate distance travelled from one point to another in meters by using Haversine formula.
"""

def calculate_distance(lat1, long1, lat2, long2):
    t1 = (lat1, long1)
    t2 = (lat2, long2)
    return haversine(t1, t2) * float(10^3) # meters

def add_distance(data):
    data['distance'] = 0
    for i in range(0, len(data)-1):
        long1 = data.loc[i, 'Long']
        lat1 = data.loc[i, 'Lat']

        long2 = data.loc[i+1, 'Long']
        lat2 = data.loc[i+1, 'Lat']

        distance = calculate_distance(lat1, long1, lat2, long2)
        
        data.loc[i+1, 'distance'] = round(distance, 3)
    
    return data

data = pd.read_csv('data/clean_tingvoll/2012_koksvik_00022_2201.csv')
print(add_distance(data))


