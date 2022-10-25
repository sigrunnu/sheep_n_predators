import pandas as pd
import numpy as np
import plotly as pl
import requests
import math
import os

data = pd.read_csv('data/2012_koksvik_6051_2224.csv', sep='\t+', skiprows=[
                   1, 2], engine='python', index_col=False, usecols=range(1, 18))


data['Date'] = pd.to_datetime(data['Date'], yearfirst=True)
dfc['Time_of_Sail'] = pd.to_datetime(
    dfc['Time_of_Sail'], format='%H:%M:%S').dt.time


print(data.head(20))

# data.to_csv('cleanedData/2012_koksvik_6051_2224_cleaned.csv')
