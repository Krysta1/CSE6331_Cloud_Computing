import base64
import csv
from io import BytesIO

from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt


def loadDataSet():
    dataMat = []
    x1 = []
    x2 = []
    with open('static/dataSet.csv') as csvFile:
        r = csv.reader(csvFile)
        for row in r:
            x1.append(float(row[1]))
            x2.append(float(row[2]))
            dataMat.append([float(row[1]), float(row[2])])
        return dataMat, x1, x2


def kmean(dataMat, K):
    data = np.array(dataMat)
    print(data)
    kmeans = KMeans(n_clusters=K)
    kmeans.fit(data)
    label = kmeans.labels_
    print(label)
    return label


def plt1(label, x1, x2):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'b']
    markers = ['o', 's', 'D', 'v', '^', 'p', '*', '+']
    for i, l in enumerate(label):
        plt.plot(x1[i], x2[i], color=colors[l], marker=markers[l], ls='None')
    sio = BytesIO()
    plt.savefig(sio, format='png')
    data = base64.encodebytes(sio.getvalue()).decode()
    # plt.show()
    return data
