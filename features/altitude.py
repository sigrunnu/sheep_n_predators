import requests
import math


def add_altitude(data):

    counter = 1
    old_range_count = 0
    range_count = 50
    data_len = len(data)
    altitude = []

    while counter <= math.ceil(data_len/50):
        coordinates = []
        for i in range(old_range_count, range_count):
            x = data['Long'][i]
            y = data['Lat'][i]
            d = [x, y]

            coordinates.append(d)

        req = requests.get(
            f'https://ws.geonorge.no/hoydedata/v1/punkt?koordsys=4326&geojson=false&punkter={coordinates}')

        for value in req.json()['punkter']:
            altitude.append(value['z'])

        old_range_count = range_count
        range_count += 50
        counter += 1

        if (range_count >= data_len-1):
            range_count -= 50
            range_count += (data_len - range_count)

    data['altitude'] = altitude

    return data
