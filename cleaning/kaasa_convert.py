import pandas as pd


def change_dtypes(data):
    data.rename(columns={'position_t': 'date_time'}, inplace=True)
    data['latitude'] = data['latitude'].fillna(0.0).astype('float64')
    data['longitude'] = data['longitude'].fillna(0.0).astype('float64')
    data['owner_id'] = data['owner_id'].fillna(0).astype('int64')
    data['source_id'] = data['source_id'].fillna(0).astype('int64')
    data['name'] = data['name'].fillna('-').astype('string')
    data['date_time'] = data['date_time'].astype('datetime64')
    data['individual'] = data['individual'].astype('int64')

    return data


def convert(data):
    for x in data.index:
        if (data.loc[x, "individual"] == '(null)'):
            data.at[x, "individual"] = 0
    return data
