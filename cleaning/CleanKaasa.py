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


# Replace all rows with individual_nr = (null) to actual number 0 for good type-casting
def clean_individual_nr_not_null(data):
    for x in data.index:
        if (data.loc[x, "individual"] == '(null)'):
            data.at[x, "individual"] = 0
    return data


# Fill in correct individual number based on source_id
def match_source_id_to_individual(data):

    empty_ind = data.loc[data['individual'] == 0]
    others = data.loc[data['individual'] != 0]

    for x in empty_ind.index:
       
        source_id = empty_ind.loc[x, 'source_id']

        if (others['source_id'] == source_id).any():
            row = others[others['source_id'] == source_id]
            nr = row['individual'].iloc[0]
            empty_ind.at[x, 'individual'] = nr
    
    res = pd.concat([empty_ind, others])
    return res
