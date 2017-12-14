import csv
import numpy
import matplotlib.pyplot as plt
from sklearn import cluster
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import fcluster

#reader = csv.reader(open("XkmeansIIA.csv", "rb"), delimiter=",")
#reader = csv.reader(open("XslinkII.csv", "rb"), delimiter=",")

#x = list(reader)
#result = numpy.array(x).astype("float");
orig = np.loadtxt('./Complexity_Data-test.csv', delimiter=',')
# k-means
a = numpy.array([[4,5], [11,8]]);
k_means = cluster.KMeans(n_clusters=2, init=a)
k_means.fit(result)
print(k_means.labels_)
plt.scatter(result[:,0],result[:,1],c=k_means.labels_)
#plt.scatter(10,50, c="green");
#plt.scatter(10,-50, c="green");
plt.title("CKmeansI")
plt.xlabel("x-axis")
plt.ylabel("y-axis")
#plt.show()


# Slink
Z = linkage(result, 'single')
final = fcluster(Z, 2, 'maxclust')
#plt.scatter(result[:,0],result[:,1],c=final)
#print(final)
#plt.title("CKMeansII")
plt.xlabel("x-axis")
plt.ylabel("y-axis")
plt.show()

