import pandas as pd


data = pd.read_csv('data/kaasa/kaasa_2021.csv')

data['position_t'] = pd.to_datetime(data['position_t'], yearfirst=True)
newd = data.sort_values(by=['individual', 'position_t'])
individuals = newd.groupby('individual').nunique()

data_info = pd.DataFrame()
individual_nr = []
first_date = []
last_date = []
nr_column = []

for individual in range(len(individuals)):
    new_row = pd.DataFrame()
    name = individuals.iloc[individual].name
    points = newd[newd['individual'] == name]
    points.reset_index(inplace=True)
    individual_nr.append(points.loc[0]['individual'])
    first_date.append(points.loc[0]['position_t'])
    last_date.append(points.loc[(len(points)-1)]['position_t'])
    nr_column.append(len(points))


data_info['individual'] = individual_nr
data_info['first_date'] = first_date
data_info['last_date'] = last_date
data_info['nr_data_points'] = nr_column
print(data_info)
data_info.to_csv('data/kaasa/info_kaasa.csv', index=False)
