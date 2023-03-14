import pandas as pd
from haversine import haversine
from haversine import Unit

# Calculate distance from one point to another point
def calculate_distance(lat1, long1, lat2, long2):
    t1 = (lat1, long1)
    t2 = (lat2, long2)
    return haversine(t1, t2, unit=Unit.METERS)

# Add attack feature if attack is on same day as sheep and sheep is closer than 1500 meters
def add_attack(sheep_data, attack_data, radius):
    for a in attack_data.index:
        attack_start_date = attack_data.at[a, 'Skadedato_fra'].date()
        attack_end_date = attack_data.at[a, 'Skadedato_til'].date()

        sheep_date = pd.to_datetime(sheep_data['date_time']).dt.date

        # Get a list of indexes from sheep data where the sheep matches the attack date
        sheep_indexes = sheep_data.loc[(attack_start_date <= sheep_date) & (sheep_date <= attack_end_date)].index
        
        for sheep in sheep_indexes:
            sheep_lat = sheep_data.at[sheep, 'latitude']
            sheep_long = sheep_data.at[sheep, 'longitude']
            attack_lat = attack_data.at[a, 'latitude']
            attack_long = attack_data.at[a, 'longitude']

            distance_to_attack = calculate_distance(sheep_lat, sheep_long, attack_lat, attack_long)
            if distance_to_attack <= radius: 
                sheep_data.at[sheep, 'attack'] = 1
                #sheep_data.at[sheep, 'attack_distance'] = round(distance_to_attack, 0)
                #sheep_data.at[sheep, 'predator'] = attack_data.at[a, 'Skadearsak']
                #sheep_data.at[sheep, 'attack_id'] = attack_data.at[a, 'RovbaseID']
    
    attack_count = sheep_data['attack'].value_counts()
    print('Radius: ', radius, 'meter \n', attack_count)

    # attack_count[0] = antall rader som ikke er med i attack, attack_count[1] = antall rader som er med i attack
    perc = 0.0 if attack_count[0] == len(sheep_data) else ((attack_count[1]/len(sheep_data)) * 100)
    perc = round(perc, 2)
    print('Prosent av hvor mye av dataen som er med i ett attack: ', perc, '%')

    return sheep_data

"""
attack_data = pd.read_csv('data/rovbase/rovviltskader.csv')

files = ['kaasa_2021.csv', 'kaasa_2020.csv', 'kaasa_2019.csv',
             'kaasa_2018.csv', 'kaasa_2017.csv', 'kaasa_2016.csv', 'kaasa_2015.csv']

for file in files:
    filepath = 'data/kaasa/' + str(file)
    sheep_data = pd.read_csv(filepath)

    sheep_data['date_time'] = pd.to_datetime(sheep_data['date_time'])
    attack_data['Skadedato_fra'] = pd.to_datetime(attack_data['Skadedato_fra'])
    attack_data['Skadedato_til'] = pd.to_datetime(attack_data['Skadedato_til'])

    sheep_data1 = sheep_data.drop(columns=['attack'])
    sheep_data1['attack'] = 0
    #sheep_data['attack_distance'] = 0.0
    #sheep_data['predator'] = None
    #sheep_data['attack_id'] = None

    print('For datasett: ', file)
    
    new = add_attack(sheep_data=sheep_data1, attack_data=attack_data, radius=1500)
    new.to_csv(filepath, index=False)
"""