import requests

"""
 Adds a latitude and longitude column to the existing dataset.
 
 Returns the new dataset.
"""


def converter(data):
    x = data['Øst (UTM33/SWEREF99 TM)'].to_numpy()
    y = data['Nord (UTM33/SWEREF99 TM)'].to_numpy()

    coordinates = []
    for i in range(len(data)):
        x = data['Øst (UTM33/SWEREF99 TM)'][i] # Longitude (lengdegrad)
        y = data['Nord (UTM33/SWEREF99 TM)'][i] # Latitude (breddegrad)
        d = {"x": str(x), "y": str(y)}

        coordinates.append(d)

    coordinates_to_string = str(coordinates)
    coordinates_w_doublequote = coordinates_to_string.replace("'", "\"")

    req = requests.post(
        "https://ws.geonorge.no/transformering/v1/transformer?fra=25833&til=4326", data=coordinates_w_doublequote)

    lat = []
    long = []
    for value in req.json():
        long.append(value['x']) # Lengdegrad
        lat.append(value['y']) # Breddegrad

    data["latitude"] = lat
    data["longitude"] = long

    return data
