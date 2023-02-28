from sklearn import preprocessing
import pandas as pd
import numpy as np


def normalize(df, columns, a, b):  # normalizes the columns listed in the variable columns
    scaler = preprocessing.MinMaxScaler(feature_range=(a, b))
    for i in range(len(columns)):
        column = np.array(df[columns[i]]).reshape(-1, 1)
        scaled = pd.DataFrame(scaler.fit_transform(
            column), columns=[columns[i]])
        df.drop(columns=[columns[i]], inplace=True)
        df = pd.concat([scaled, df], axis=1)
    return df


def standardize(df, columns):  # standardizes the columns listed in the variable columns
    scaler = preprocessing.StandardScaler()
    for i in range(len(columns)):
        column = np.array(df[columns[i]]).reshape(-1, 1)
        scaled = pd.DataFrame(scaler.fit_transform(
            column), columns=[columns[i]])
        df.drop(columns=[columns[i]], inplace=True)
        df = pd.concat([scaled, df], axis=1)
    return df

# Eksempel:

#df1 = Normalize(df, ['velocity', 'temperature', 'altitude', 'distance', 'date_time'], 0, 1)
