import plotly.express as px
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from Scaling import standardize, normalize
import seaborn as sns
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# Find eps by using elbow method by KNN
def findEps(df, n_neighbors, radius=1, fig=False):
    knn = NearestNeighbors(n_neighbors=n_neighbors, radius=radius).fit(df) # radius = 1 as default
    neigh_dist, neigh_ind = knn.kneighbors(df) # find the k-neighbors of a point
    neigh_dist = np.sort(neigh_dist, axis=0) # sort the neighbor distances (lengths to points) in ascending order

    neigh_dist = neigh_dist[:, n_neighbors-1]

    if fig:
        plt.plot(neigh_dist)
        plt.title('Epsilon plot, all data', pad=15)
        plt.xlabel('Points in the dataset', labelpad=15)
        plt.ylabel('Sorted {}-nearest neighbor distance'.format(n_neighbors), labelpad=15)
        plt.grid(True)
        #plt.xticks(fontsize=20)
        #plt.yticks(fontsize=20)
        plt.ylim(-0.05, 1.9)
        plt.axhline(y=0.20, color='red', linewidth=1) # eps line
        plt.axhline(y=0.15, color='green', linewidth=1) # eps line
        plt.tight_layout()
        plt.show()


# Do DBSCAN algorithm and find number of outliers and the outlier cluster
def dbscan(df, epsilon, min, fig=False):
    dbscan = DBSCAN(eps=epsilon, min_samples=min, n_jobs=-1).fit(df)
    clusters = dbscan.labels_
    df['cluster'] = clusters # set cluster label to dataset

    print('n features:', dbscan.n_features_in_)
    print('features:', dbscan.feature_names_in_)

    no_clusters = len(np.unique(clusters))
    no_noise = np.sum(np.array(clusters) == -1, axis=0)
    no_points = np.sum(np.array(clusters) != -1, axis=0)


    print('Estimated no. of clusters: %d' % no_clusters)
    print('Estimated no. of points: %d' % no_points)
    print('Estimated no. of noise points: %d' % no_noise)

    if fig:
        
        #fig = px.scatter_3d(df, x='sin_time', y='cos_time', z='velocity', color='cluster', opacity=1, height=500, width=700)
        #fig.update_traces(marker=dict(size=5), selector=dict(mode='markers'))
        #fig.show()

        polar_mean = df.groupby('cluster').mean().reset_index()
        print(polar_mean)
        #print(polar['altitude'].describe(), polar['temperature'].describe(), polar['velocity'].describe(), polar['sin_time'].describe(), polar['cos_time'].describe())
        polar_std = df.groupby('cluster').std().reset_index()
        polar_mean = pd.melt(polar_mean, id_vars=['cluster'])
        polar_std = pd.melt(polar_std, id_vars=['cluster'])

        fig2 = px.line_polar(polar_mean, r='value', theta='variable', color='cluster', line_close=True, height=500, width=700, title='Polar line plot of the mean of the DBSCAN clustering for all numerical features and all data')
        fig3 = px.line_polar(polar_std, r='value', theta='variable', color='cluster', line_close=True, height=500, width=700, title='Polar line plot of the standard deviation of the DBSCAN clustering for all numerical features and all data')
        
        fig2.show()
        fig3.show()
        
        #p = sns.scatterplot(data=df, x="velocity", y="altitude", hue=clusters, legend="full", palette="deep")
        #sns.move_legend(p, "upper right", bbox_to_anchor=(1.17, 1.2), title='Clusters')
        #plt.show()

# Se hvordan man kjører i DBSCAN.ipynb