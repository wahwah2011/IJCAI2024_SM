import numpy as np
import matplotlib.pyplot as plt

from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering

def plot_hac_dendogram(ax, fig, influence, players, linkage='ward'):
    # Normalize the influence to embed the players onto the unit sphere
    X = influence # / np.sum(np.abs(influence), axis=1)[:, np.newaxis]
    #np.fill_diagonal(X, 0)

    # Cluster using HAC
    # https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html
    model = AgglomerativeClustering(distance_threshold=0, n_clusters=None,
        affinity='euclidean' if linkage != 'ward' else 'euclidean',
        linkage=linkage)
    model = model.fit(X)

    print(model.children_)
    print(model.distances_)

    # Create linkage matrix and then plot the dendrogram
    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    print(counts)

    linkage_matrix = np.column_stack([model.children_, model.distances_, counts]).astype(float)

    print(linkage_matrix)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, truncate_mode='level', p=len(players), 
        labels=[p[:4] for p in players], ax=ax)
    fig.subplots_adjust(top=1.0)

if __name__ == '__main__':
    plrs = 5
    player_names = [f'P {i+1}' for i in range(plrs)]
    # inf_mat = np.random.normal(loc=0, scale=1, size=(plrs, plrs))
    inf_mat = [[0,.9,0,0,0],[.9,0,0,0,0],[0,0,1,0,0],[0,0,0,0,1],[0,0,0,1,0]]
    print(inf_mat)
    if np.any(inf_mat != 0):
        inf_mat = inf_mat / np.sum(inf_mat)
        inf_mat = np.linalg.matrix_power(inf_mat, plrs)

    print(inf_mat)

    fig, ax = plt.subplots(1, 1, figsize=(6, 6))

    linkages = [
        'ward',
        'average',
        'compelte',
        'single'
    ]

    plot_hac_dendogram(ax, fig, inf_mat, player_names, linkage=linkages[1])

    plt.show()