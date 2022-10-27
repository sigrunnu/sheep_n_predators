from Distance import calculate_distance

"""
Calculate the velocit of the sheep based on the Haversine formula in m/h.
"""

def calculate_velocity(lat1, long1, lat2, long2):
    dist = calculate_distance(lat1, long1, lat2, long2)
    return round(dist/0.5, 3)

def add_velocity(data):
    data['velocity'] = 0
    for i in range(0, len(data)-1):
        long1 = data.loc[i, 'Long']
        lat1 = data.loc[i, 'Lat']

        long2 = data.loc[i+1, 'Long']
        lat2 = data.loc[i+1, 'Lat']

        velocity = calculate_velocity(lat1, long1, lat2, long2)
        
        data.loc[i+1, 'velocity'] = velocity
    
    return data