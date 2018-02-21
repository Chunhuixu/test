#!/usr/bin/python  
# -*- coding: utf-8 -*-  
  
from numpy import *  
import matplotlib.pyplot as plt  
 
  
# 计算距离平方  
def euclDistance(vector1, vector2):  
    return sum(power(vector2 - vector1, 2))  
  
  
# 用随机样本初始化centroids  
def initCentroids(dataSet, k):  
    numSamples, dim = dataSet.shape  
    centroids = zeros((k + 1, dim))  
  
    s = set()  
    for i in range(1, k + 1):  
        while True:  
            index = int(random.uniform(0, numSamples))  
            if index not in s:  
                s.add(index)  
                break  
        # index = int(random.uniform(0, 2))  
        print "random index:"  
        print index  
        centroids[i, :] = dataSet[index, :]  
  
    # centroids[0, :] = dataSet[0, :]  
    # centroids[1, :] = dataSet[2, :]  
  
    # centroids[1, :] = dataSet[0, :]  
    # centroids[2, :] = dataSet[2, :]  
    return centroids  
  
# 获得cost  
def getcost(clusterAssment):  
    len = clusterAssment.shape[0]  
    Sum = 0.0  
    for i in xrange(len):  
        Sum = Sum + clusterAssment[i, 1]  
    return Sum  
  
# k-means主算法  
def kmeans(dataSet, k):  
    numSamples = dataSet.shape[0]  
  
    # 第一列存这个样本点属于哪个簇  
    # 第二列存这个样本点和样本中心的误差  
    clusterAssment = mat(zeros((numSamples, 2)))  
    for i in xrange(numSamples):  
        clusterAssment[i, 0] = -1  
    clusterChanged = True  
  
    # step 1: 初始化centroids  
    centroids = initCentroids(dataSet, k)  
  
    # 如果收敛完毕，则clusterChanged为False  
    while clusterChanged:  
        clusterChanged = False  
        # 对于每个样本点  
        for i in xrange(numSamples):  
            minDist = 100000.0  
            minIndex = 0  
            # 对于每个样本中心  
            # step 2: 找到最近的样本中心  
            for j in range(1, k + 1):  
                distance = euclDistance(centroids[j, :], dataSet[i, :])  
                if distance < minDist:  
                    minDist = distance  
                    minIndex = j  
  
            # step 3: 更新样本点与中心点的分配关系  
            if clusterAssment[i, 0] != minIndex:  
                clusterChanged = True  
                clusterAssment[i, :] = minIndex, minDist  
            else:  
                clusterAssment[i, 1] = minDist  
  
        # step 4: 更新样本中心  
        print "clusterAssment before:"  
        print clusterAssment  
        for j in range(1, k + 1):  
            # 骚操作  
            pointsInCluster = dataSet[nonzero(clusterAssment[:, 0].A == j)[0]]  
            centroids[j, :] = mean(pointsInCluster, axis=0)  
  
    print 'Congratulations, cluster complete!'  
    return centroids, clusterAssment  
  
  
# 以2D形式可视化数据  
def showCluster(dataSet, k, centroids, clusterAssment):  
    numSamples, dim = dataSet.shape  
    if dim != 2:  
        print "Sorry! I can not draw because the dimension of your data is not 2!"  
        return 1  
  
    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']  
    if k > len(mark):  
        print "Sorry! Your k is too large!"  
        return 1  
  
    # 绘制所有非中心样本点  
    for i in xrange(numSamples):  
        markIndex = int(clusterAssment[i, 0])  
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex - 1])  
  
    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']  
    # 绘制中心点  
    for i in range(1, k + 1):  
        plt.plot(centroids[i, 0], centroids[i, 1], mark[i - 1], markersize=12)  
  
    plt.show()  
  
# step 1: 载入数据  
print "step 1: load data..."  
dataSet = []  
fileIn = open('~/testSet.txt')  
for line in fileIn.readlines():  
    lineArr = line.strip().split('\t')  
    dataSet.append([float(lineArr[0]), float(lineArr[1])])  
  
  
# step 2: 开始聚合...  
print "step 2: clustering..."  
dataSet = mat(dataSet)  
print "dataSet:"  
print dataSet  
k = 4  
centroids, clusterAssment = kmeans(dataSet, k)  
  
# 我就瞅瞅里面有啥  
print "center:"  
print centroids  
print "clusterAssment:"  
print clusterAssment  
print "cost:"  
print getcost(clusterAssment)  
  
# step 3: 显示结果  
print "step 3: show the result..."  
showCluster(dataSet, k, centroids, clusterAssment)  