import sys
import argparse
arg = sys.argv
method = arg[1]
input_filename = arg[2]
# reads the numbers from input file and puts them in list, each position in the list contains a cluster,sorted
def initdataset(input_filename):   
    listtryal = []
    with open(input_filename, "r") as file:
        # data = file.read()
        for line in file:
            text = line.split(" ")
    for s in text:
        listtryal.append(int(s))
    listtryal.sort()
    return listtryal
#initialize list of clusters
listtryal = initdataset(input_filename)
#calculates the distance of single clusters
def calulatedistofsingleclusters(listtryal):
    distmat = []
    for i in range(len(listtryal)) :
        help = []
        for j in range(len(listtryal)):

            dist = abs(listtryal[i]- listtryal[j])
            help.append(dist)
        distmat.append(help)
    return distmat
# makes the coefficients of the lance williams
def coeffmethod(method,s,t):
    if method == "single":
        a1 = 1/2
        a2 = 1/2
        b = 0
        g = -1/2
    elif method == "complete":
        a1 = 1/2
        a2 = 1/2
        b = 0
        g = 1/2
    else :
        a1 = countcluster(s) / (countcluster(s) + countcluster(t))
        a2 = countcluster(t) / (countcluster(s) + countcluster(t))
        b = 0
        g = 0
    return a1,a2,b,g
    #ward method pending
# calculates the distance when we have clusters with more than one elements
def newdistance(mincol,minrow,listtryal,distmat,clusterA,clusterB):
    a1,a2,b,g = coeffmethod(method,clusterA,clusterB)
    for i in range(len(listtryal)):
        help = []
        for j in range(len(listtryal)):
                dist = a1 * distmat[i][mincol] + a2 *distmat[minrow][j] + b * distmat[minrow][mincol] - g * abs(distmat[i][mincol]-distmat[minrow][j])
                help.append(dist)
        distmat.append(help)
#find min distance in the distance matrix
def initializemindistance(listtryal):
    minvalue = distmat[0][1]
    minrow = 0
    mincol = 1
    for i in range(len(listtryal)) :
        for j in range(len(listtryal)):
            if distmat[i][j] < minvalue and distmat[i][j] != 0 :
                minvalue = distmat[i][j]
                minrow = i
                mincol = j
    return minvalue,minrow,mincol
#counts how many elements a cluster has
def countcluster(cluster):

    if not isinstance(cluster,list) :
        return 1
    count = 0

    for el in cluster:
        count = count + countcluster(el)
    return count
#makes a new cluster and throws away the old ones
def makenewcluster(clusterA, clusterB, listtryal):
    cluster = []
    cluster.append(clusterA)
    cluster.append(clusterB)
    listtryal.remove(clusterA)
    listtryal.remove(clusterB)
    listtryal.append(cluster)
    return listtryal
#MAIN
distmat = calulatedistofsingleclusters(listtryal)
while len(listtryal) > 1:
    minvalue, minrow, mincol = initializemindistance(listtryal)
    minvalue = "{:.2f}".format(minvalue)
    clusterB = listtryal[minrow]
    clusterA = listtryal[mincol]
    count = countcluster(clusterA) + countcluster(clusterB)
    print(f"{listtryal[minrow]} {listtryal[mincol]} {minvalue} {count}")
    listtryal = makenewcluster(clusterA,clusterB,listtryal)
    newdistance(mincol,minrow,listtryal,distmat,clusterA,clusterB)
#correct clustering pending