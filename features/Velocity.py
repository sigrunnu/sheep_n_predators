from Distance import calculate_distance

"""
Calculate the velocity of the sheep based on the Haversine formula in m/h.
"""

def calculate_velocity(lat1, long1, lat2, long2):
    dist = calculate_distance(lat1, long1, lat2, long2)
    return round(dist/0.5, 3)


def add_velocity(data):
    if not 'velocity' in data.columns: 
        data['velocity'] = 0
        
    for i in range(0, len(data)-1):
        long1 = data.loc[i, 'longitude']
        lat1 = data.loc[i, 'latitude']

        long2 = data.loc[i+1, 'longitude']
        lat2 = data.loc[i+1, 'latitude']

        velocity = calculate_velocity(lat1, long1, lat2, long2)

        data.loc[i+1, 'velocity'] = velocity

    return data
