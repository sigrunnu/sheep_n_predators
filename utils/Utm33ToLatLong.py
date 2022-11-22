
"""
 Adds a latitude and longitude column to the existing dataset.
 
 Returns the new dataset.

"""
import requests
import pandas as pd


def converter(data):
    x = data['Øst (UTM33/SWEREF99 TM)'].to_numpy()
    y = data['Nord (UTM33/SWEREF99 TM)'].to_numpy()

    coordinates = []
    for i in range(len(data)):
        x = data['Øst (UTM33/SWEREF99 TM)'][i]
        y = data['Nord (UTM33/SWEREF99 TM)'][i]
        d = {"x": str(x), "y": str(y)}

        coordinates.append(d)

    coordinates_to_string = str(coordinates)
    coordinates_w_doublequote = coordinates_to_string.replace("'", "\"")

    req = requests.post(
        "https://ws.geonorge.no/transformering/v1/transformer?fra=25833&til=4326", data=coordinates_w_doublequote)

    lat = []
    long = []
    for value in req.json():
        long.append(value['x'])
        lat.append(value['y'])

    data["latitude"] = lat
    data["longitude"] = long

    return data


skadet1 = pd.read_csv(
    'data/rovviltskader_sikker_en_dato_meraker_2015-2022.csv')
skadet2 = pd.read_csv('data/rovviltskader_vasket.csv')


converter(skadet1).to_csv(
    'data/rovviltskader_sikker_en_dato_meraker_2015-2022.csv', index=False)
converter(skadet2).to_csv('data/rovviltskader_vasket.csv', index=False)
