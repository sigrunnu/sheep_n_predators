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
                       'Close_to_attack'] == 'No'):
        sheep_data.loc[si,
                       'Attack_lat'] = attack_data.loc[ai, 'latitude']
        sheep_data.loc[si,
                       'Attack_long'] = attack_data.loc[ai, 'longitude']
        sheep_data.loc[si,
                       'Attack_id'] = attack_data.loc[ai, 'RovbaseID']
        sheep_data.loc[si,
                       'Attack_predator'] = attack_data.loc[ai, 'Skadeårsak']
        sheep_data.loc[si,
                       'Attack_distance'] = distance
        sheep_data.loc[si,
                       'Close_to_attack'] = 'Yes'
    else:
        sheep_data.loc[si,
                       'Attack_id'] = sheep_data.loc[si,
                                                     'Attack_id'] + " " + attack_data.loc[ai, 'RovbaseID']


def create_attack_data(skadet, sheep_data):
    sheep_data['Attack_distance'] = 0
    sheep_data['Close_to_attack'] = "No"
    sheep_data['Attack_predator'] = "No"
    sheep_data['Attack_id'] = "No"
    sheep_data['Attack_long'] = 0.0
    sheep_data['Attack_lat'] = 0.0

    for i in range(len(skadet)-1):
        for p in range(len(sheep_data)):
            sheep_date = sheep_data.loc[p, "date_time"].split(" ")[0] # Get only date with not time
            isDate = skadet.loc[i,
                                'Skadedato, fra'] == sheep_date
            if (isDate):
                distance_to_attack = calculate_distance(
                    sheep_data.loc[p, 'Lat'], sheep_data.loc[p, 'Long'], skadet.loc[i, 'latitude'], skadet.loc[i, 'longitude'])
                if (distance_to_attack <= 3000):
                    add_attack_features(
                        sheep_data, p, skadet, i, distance_to_attack)

    print(sheep_data)
    print(sheep_data.loc[sheep_data["Close_to_attack"] == "Yes"])

    return sheep_data


skadet = pd.read_csv('data/rovbase/rovviltskader_sikker_en_dato_meraker_2015-2022.csv')
koksvik = pd.read_csv('data/kaasa/kaasa_2021.csv')

k = create_attack_data(skadet, koksvik)
print(k.head(10))