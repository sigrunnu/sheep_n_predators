import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn import preprocessing, metrics
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
import seaborn as sns


def ElbowMethod(df):
    score = []
    for i in range(1, 21):
        kmeans = KMeans(n_clusters=i, max_iter=1000,  n_init=10).fit(df)
        df['clusters'] = kmeans.labels_
        score.append(kmeans.inertia_)
    plt.figure(figsize=(8, 4))
    plt.plot(range(1, 21), score)
    plt.title('Elbow method for Kmeans++')
    plt.xlabel('Number of clusters')
    plt.xticks(fontsize=20, ticks=[2, 4, 6, 8,
               10, 12, 14, 16, 18, 20])
    plt.ylabel('Score')
    plt.show()


# 3 dimention K-means
def Kmeans3Dim(df, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, n_init=10)
    kmeans.fit(df)
    clusters = kmeans.labels_  # samme som kmeans.predict(df1)
    df['cluster'] = clusters
    print('inertia:', kmeans.inertia_)
    print('iterations:', kmeans.n_iter_)
    print('n features:', kmeans.n_features_in_)
    print('features:', kmeans.feature_names_in_)
    fig = px.scatter_3d(df, x='sin_time', y='cos_time',
                        z="velocity", color='cluster', opacity=1)
    fig.update_traces(marker=dict(size=5, line=dict(
        width=1, color='white')), selector=dict(mode='markers'))
    fig.show()


# For polar plots
def Kmeans(df, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(df)
    clusters = kmeans.labels_  # samme som kmeans.predict(df1)s
    df['cluster'] = clusters
    print('inertia:', kmeans.inertia_)
    print('iterations:', kmeans.n_iter_)
    print('n features:', kmeans.n_features_in_)
    print('features:', kmeans.feature_names_in_)
    polar = df.groupby('cluster').mean().reset_index()
    polar1 = df.groupby('cluster').std().reset_index()
    polar = pd.melt(polar, id_vars=['cluster'])
    polar1 = pd.melt(polar1, id_vars=['cluster'])
    fig = px.line_polar(polar, r='value', theta='variable',
                        color='cluster', line_close=True, height=800, width=1400)
    fig1 = px.line_polar(polar1, r='value', theta='variable',
                         color='cluster', line_close=True, height=800, width=1400)
    fig.show()
    fig1.show()


'''

df2015 = pd.read_csv('../data/kaasa/kaasa_2015.csv', index_col=None, header=0)
df2016 = pd.read_csv('../data/kaasa/kaasa_2016.csv', index_col=None, header=0)
df2017 = pd.read_csv('../data/kaasa/kaasa_2017.csv', index_col=None, header=0)
df2018 = pd.read_csv('../data/kaasa/kaasa_2018.csv', index_col=None, header=0)
df2019 = pd.read_csv('../data/kaasa/kaasa_2019.csv', index_col=None, header=0)
df2020 = pd.read_csv('../data/kaasa/kaasa_2020.csv', index_col=None, header=0)
df2021 = pd.read_csv('../data/kaasa/kaasa_2021.csv', index_col=None, header=0)

files = [df2015, df2016, df2017, df2018, df2019, df2020, df2021]

df_tot = pd.concat(files, axis=0, ignore_index=True)
df_tot['date_time'] = pd.to_datetime(df_tot['date_time'])

for x in df_tot.index:
    df_tot.at[x, 'date_time'] = df_tot.at[x, 'date_time'].timestamp()

df1 = df_tot.drop(columns=['latitude', 'longitude', 'name', 'individual',
                        'source_id', 'owner_id', 'date_time', 'distance'])
'''
