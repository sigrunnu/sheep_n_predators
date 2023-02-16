import requests
import time
from threading import Thread, Lock
import pandas as pd

lock = Lock()

time0 = time.time()


"""
Add altitude to the dataframe by calling an external API (Kartverket). 
Kartverket can handle 50 coordinates at once. We send in 50 coordinates as a list, and then apply them to our data.
"""
def add_altitude(data, start, stop):

    exceptions = 0

    old_range_count = start # start position for every iteration
    range_count = start + 50 # end position for every iteration (Kartverket can handle up to 50 coordinates at once)
    
    # these two list will always correspond, e. g index nr. 0 has the altitude nr. 0, index1 has altitude1..
    altitudes = [] # list with all returned altitudes
    indexes = [] # list of indexes of the dataframe for the 50 coordinates

    rest = len(data) % 50 # the rest, f. ex 320 % 50 will return 20

    while range_count <= stop: # as long as end position of iteration is less than stop position

        try: 
            if (range_count % 1000) == 0:
                print("Reached number: ", i, '--------')

            global lock
            with lock:
       
                coordinates = [] # temporary list of coordinates to be sent with GET-request

                for x in range(old_range_count, range_count): # loop 50 times
                    lat = data.at[x, 'latitude']
                    long = data.at[x, 'longitude']
                    coordinate = [long, lat]

                    coordinates.append(coordinate)
                    indexes.append(x)

                req = requests.get(
                    f'https://ws.geonorge.no/hoydedata/v1/punkt?koordsys=4326&geojson=false&punkter={coordinates}')

                for value in req.json()['punkter']: # from the returned response, get z-value which is altitude
                    altitudes.append(value['z'])

                old_range_count = range_count # update old range count so we can iterate over 50 next points
                range_count += 50 # update end position of next iteration

                if (range_count > stop) and rest > 0: # if new end position is more than stop index
                    range_count -= 50 # remove the added +50
                    range_count += rest # add the rest instead
                
        except Exception as e:
            exceptions += 1
            print('There were ', exceptions, 'exceptions: ', e)

        # add altitudes to the data based on index
        for a, i in zip(altitudes, indexes): # loop through in parallell index0 has altitude0
            data.at[i, 'altitude'] = a 
    
    print('Done adding altitudes for one thread')

"""
Get start and stop index/position for every thread.
"""
def GetValues(data):
    interval = int((len(data)) / 6)
    start = 0
    first = interval
    second = 2*interval
    third = 3*interval
    four = 4*interval
    five = 5*interval
    end = len(data)
    return start, first, second, third, four, five, end


"""
Function to start threading. The data is splitted in 6 threads.
"""
def runner(data):
    start1, first1, second1, third1, four1, five1, end1 = GetValues(data)
    print(start1, first1, second1, third1, four1, five1, end1)

    data1 = data.iloc[start1:first1, :]
    data2 = data.iloc[first1:second1, :]
    data3 = data.iloc[second1:third1, :]
    data4 = data.iloc[third1:four1, :]
    data5 = data.iloc[four1:five1, :]
    data6 = data.iloc[five1:end1, :]

    threads = [
        Thread(target=add_altitude, args=(data1, start1, first1)),
        Thread(target=add_altitude, args=(data2, first1, second1)),
        Thread(target=add_altitude, args=(data3, second1, third1)),
        Thread(target=add_altitude, args=(data4, third1, four1)),
        Thread(target=add_altitude, args=(data5, four1, five1)),
        Thread(target=add_altitude, args=(data6, five1, end1))
    ]

    for t in threads:
        t.start()
    
    for j in threads:
        j.join()
    
    datatot = pd.concat([data1, data2, data3, data4])

    return datatot

"""
Need to add a new column to the data before adding altitude (only initial time). 
"""
def add_new_column(data):
    data['altitude'] = [0.0] * len(data)
    return data

"""
Check if altitudes are less than 0 and higher than 1441 (highest mountain in Merkåker)
"""
def check_wrong_altitudes(data):
    i = 0
    while i < len(data):
        if data.at[i, 'altitude'] < float(0):
            print('this row has altitude less than 0 masl.: ', data.iloc[[i]])
        if data.at[i, 'altitude'] > float(1441):
            print('this row has altitude higher than 1441 masl.: ', data.iloc[[i]])
        i += 1


k2015 = pd.read_csv('data/kaasa/kaasa_2015.csv')
k2016 = pd.read_csv('data/kaasa/kaasa_2016.csv')
k2017 = pd.read_csv('data/kaasa/kaasa_2017.csv')
k2018 = pd.read_csv('data/kaasa/kaasa_2018.csv')
k2019 = pd.read_csv('data/kaasa/kaasa_2019.csv')
k2020 = pd.read_csv('data/kaasa/kaasa_2020.csv')
k2021 = pd.read_csv('data/kaasa/kaasa_2021.csv')

#k2015 = add_new_column(k2015)
#k2016 = add_new_column(k2016)
#k2017 = add_new_column(k2017)
#k2018 = add_new_column(k2018)
#k2019 = add_new_column(k2019)
#k2020 = add_new_column(k2020)
#k2021 = add_new_column(k2021)

#k2015_done = runner(k2015)
#k2015_done.to_csv('data/kaasa/kaasa_2015.csv', index=False)
#print('number of rows with different altitudes: ', k2015_done['altitude'].value_counts())

#k2016_done = runner(k2016)
#k2016_done.to_csv('data/kaasa/kaasa_2016.csv', index=False)
#print('number of rows with different altitudes: ', k2016_done['altitude'].value_counts())

#k2017_done = runner(k2017)
#k2017_done.to_csv('data/kaasa/kaasa_2017.csv', index=False)
#print('number of rows with different altitudes: ', k2017_done['altitude'].value_counts())

#k2018_done = runner(k2018)
#k2018_done.to_csv('data/kaasa/kaasa_2018.csv', index=False)
#print('number of rows with different altitudes: ', k2018_done['altitude'].value_counts())

#k2019_done = runner(k2019)
#k2019_done.to_csv('data/kaasa/kaasa_2019.csv', index=False)
#print('number of rows with different altitudes: ', k2019_done['altitude'].value_counts())

#k2020_done = runner(k2020)
#k2020_done.to_csv('data/kaasa/kaasa_2020.csv', index=False)
#print('number of rows with different altitudes: ', k2020_done['altitude'].value_counts())

#k2021_done = runner(k2021)
#k2021_done.to_csv('data/kaasa/kaasa_2021.csv', index=False)
#print('number of rows with different altitudes: ', k2021_done['altitude'].value_counts())

check_wrong_altitudes(k2015)
check_wrong_altitudes(k2016)
check_wrong_altitudes(k2017)
check_wrong_altitudes(k2018)
check_wrong_altitudes(k2019)
check_wrong_altitudes(k2020)
check_wrong_altitudes(k2021)

print('the program took ', time.time() - time0, 'seconds')