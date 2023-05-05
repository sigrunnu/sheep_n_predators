from sklearn.preprocessing import MinMaxScaler, StandardScaler
import pandas as pd


def normalize(df, columns, a=0, b=1):
    """Normalizes the columns listed in 'columns' to the range (a, b)"""
    scaler = MinMaxScaler(feature_range=(a, b))
    for col in columns:
        col_arr = df[col].values.reshape(-1, 1)
        scaled = pd.DataFrame(scaler.fit_transform(col_arr), columns=[col])
        df = df.drop(columns=col).join(scaled)
    return df


def standardize(df, columns):
    """Standardizes the columns listed in 'columns'"""
    scaler = StandardScaler()
    for col in columns:
        col_arr = df[col].values.reshape(-1, 1)
        scaled = pd.DataFrame(scaler.fit_transform(col_arr), columns=[col])
        df = df.drop(columns=col).join(scaled)
    return df
