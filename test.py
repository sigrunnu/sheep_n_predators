import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv('telespor.csv', sep=';')
df = data.copy(deep=True).head(20)

print(data.head(10))

def remove_rows_with_empty_position():
    for x in df.index: 
        if np.isnan(df.loc[x, "Lengdegrad"]) or np.isnan(df.loc[x, "Breddegrad"]):
            df.drop(x, inplace=True)

remove_rows_with_empty_position()

print(df)