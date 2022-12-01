import pandas as pd
from haversine import haversine
from haversine import Unit

"""
Check if the sheep has been nearby an attack and add attack features to the dataset
"""


def calculate_distance(lat1, long1, lat2, long2):
    t1 = (lat1, long1)
    t2 = (lat2, long2)
    return haversine(t1, t2, unit=Unit.METERS)


def match_day(date, sheep_date):
    return date == sheep_date


def add_attack_features(sheep_data, si, attack_data, ai, distance):
    if (sheep_data.loc[si,
                       'close_to_attack'] == 'No'):
        sheep_data.loc[si,
                       'attack_lat'] = attack_data.loc[ai, 'latitude']
        sheep_data.loc[si,
                       'attack_long'] = attack_data.loc[ai, 'longitude']
        sheep_data.loc[si,
                       'attack_id'] = attack_data.loc[ai, 'RovbaseID']
        sheep_data.loc[si,
                       'attack_predator'] = attack_data.loc[ai, 'Skadeårsak']
        sheep_data.loc[si,
                       'attack_distance'] = distance
        sheep_data.loc[si,
                       'close_to_attack'] = 'Yes'
    else:
        sheep_data.loc[si,
                       'attack_id'] = sheep_data.loc[si,
                                                     'attack_id'] + " " + attack_data.loc[ai, 'RovbaseID']


def create_attack_data(attack_data, sheep_data):
    sheep_data['attack_distance'] = 0
    sheep_data['close_to_attack'] = "No"
    sheep_data['attack_predator'] = "No"
    sheep_data['attack_id'] = "No"
    sheep_data['attack_long'] = 0.0
    sheep_data['attack_lat'] = 0.0


    for x in sheep_data.index:
            sheep_date = sheep_data.loc[x, "date_time"].split(" ")[0] # Get only date with not time
            
            a_index = attack_data.loc[attack_data['Skadedato, fra'] == sheep_date].index
            for i in a_index:
                distance_to_attack = calculate_distance(
                    sheep_data.loc[x, 'st_y'], sheep_data.loc[x, 'st_x'], attack_data.loc[i, 'latitude'], attack_data.loc[i, 'longitude'])
                if (distance_to_attack <= 3000):
                    add_attack_features(
                        sheep_data, x, skadet, i, distance_to_attack)
                

    return sheep_data


skadet = pd.read_csv('data/rovbase/rovviltskader_sikker_en_dato_meraker_2015-2022.csv')
koksvik = pd.read_csv('data/kaasa/kaasa_2017.csv')

k = create_attack_data(skadet, koksvik)
print(k.head())
k.to_csv('test2.csv')
