'''
Algorithmic Thinking Application 3:
Clustering
'''
from collections import deque
import urllib2
import random
import time
import math
import matplotlib.pyplot as plt
import alg_cluster
import alg_clusters_matplotlib
import viz
import project3_solution as sol


def gen_random_clusters(num_clusters):
    singleton_list = []
    for i in range(num_clusters):
        coord_x = random.uniform(-1, 1)
        coord_y = random.uniform(-1, 1)
        singleton_list.append(alg_cluster.Cluster(set([]), coord_x, coord_y, 0, 0.0))
    
    return singleton_list

def time_slow_pair():
    runningtime = []
    for n in range(2,200):
        rand_clusters = gen_random_clusters(n)
        start_time = time.time()
        closest_pair = sol.slow_closest_pairs(rand_clusters)
        end_time = time.time()
        t = end_time - start_time
        runningtime.append(t)
    return runningtime

def time_fast_pair():
    runningtime = []
    for n in range(2,200):
        rand_clusters = gen_random_clusters(n)
        start_time = time.time()
        closest_pair = sol.fast_closest_pair(rand_clusters)
        end_time = time.time()
        t = end_time - start_time
        runningtime.append(t)
    return runningtime



#slow = time_slow_pair()
#fast = time_fast_pair()
#
#plt.plot(slow, 'b-', label='slow_closest_pairs')
#plt.plot(fast, 'r-', label='fast_closest_pair')
#plt.legend(loc='upper left')
#plt.ylabel('runnning time (s)')
#plt.xlabel('number of clusters')
#plt.title('Running time of slow_closest_pairs vs fast_closest_pair (desktop)')
#plt.show()