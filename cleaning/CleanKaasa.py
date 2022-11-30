import pandas as pd

# Fill in correct individual number based on source_id if they exist
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


# Remove source_id where its less than 10 occurances
def remove_sheep_with_less_than_10_points(data):
    
    empty_ind = data.loc[data['individual'] == 0]

    if not empty_ind.empty:
        source_count = empty_ind['source_id'].value_counts()
        
        for x in source_count.index:
            if source_count[x] < 10:
                data = data.drop(data[data.source_id == x].index)
    
    return data               
