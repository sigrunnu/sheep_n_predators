import pandas as pd
import plotly.express as px
from utm33_to_latlong import converter


data = converter(pd.read_csv('data/rovviltskader_meraker_2015-2022.csv'))


fig = px.scatter_mapbox(data, lat='latitude', lon='longitude',  color='Skadeårsak', hover_data=['Skadeårsak'], opacity=0.8, width=800, height=500,
                        center=dict(lat=63.546715, lon=11.971423), zoom=6,
                        mapbox_style="stamen-terrain")

fig.show()
