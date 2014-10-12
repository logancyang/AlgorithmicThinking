'''
Algorithmic Thinking Project 3:
Closest pairs and clustering algorithms

four functions:

slow_closest_pairs(cluster_list)
fast_closest_pair(cluster_list) - implement fast_helper()
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a list of clusters in the plane
'''

import math
import alg_cluster


def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function to compute Euclidean distance between two clusters
    in cluster_list with indices idx1 and idx2
    
    Returns tuple (dist, idx1, idx2) with idx1 < idx2 where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    
    DONE
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))



def slow_closest_pairs(cluster_list):
    """
    Compute the set of closest pairs of cluster in list of clusters
    using O(n^2) all pairs algorithm
    
    Returns the set of all tuples of the form (dist, idx1, idx2) 
    where the cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.
    
    DONE
    """
    
    pairs = []
    closest_pairs = []
    temp_tuple = (1000000000.0, -1, -1)
    for ind_u, dummy_cluster_u in enumerate(cluster_list):
        for ind_v, dummy_cluster_v in enumerate(cluster_list):
            if ind_u < ind_v:
                pair_uv = pair_distance(cluster_list, ind_u, ind_v)
                pairs.append(pair_uv)
                if pair_uv[0] < temp_tuple[0]:
                    temp_tuple = pair_uv
    #print "temp_tuple: ", temp_tuple
    #print "pairs: ", pairs
    for pair in pairs:
        if pair[0] == temp_tuple[0]:
            closest_pairs.append(pair)
    
    return set(closest_pairs)



def fast_closest_pair(cluster_list):
    """
    Compute a closest pair of clusters in cluster_list
    using O(n log(n)) divide and conquer algorithm
    
    Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
    cluster_list[idx1] and cluster_list[idx2]
    have the smallest distance dist of any pair of clusters

    """
        
    def fast_helper(cluster_list, horiz_order, vert_order):
        """
        Divide and conquer method for computing distance between closest pair of points
        Running time is O(n * log(n))
        
        horiz_order and vert_order are lists of indices for clusters
        ordered horizontally and vertically
        
        Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
        cluster_list[idx1] and cluster_list[idx2]
        have the smallest distance dist of any pair of clusters
    
        """
        
        # base case
        num_clusters = len(horiz_order)     #"let n be the number of elements in H", for each recursive call, n is different
        if num_clusters <= 3:
            #print "--- Entering Base Case with", num_clusters, " Clusters ---"
            base_clusters = [cluster_list[idx] for idx in horiz_order]  #IMPORTANT!!!
            #print "base_clusters:", base_clusters
            temp_set = slow_closest_pairs(base_clusters)   #DO NOT PASS IN cluster_list HERE!!!
            temp = temp_set.pop()
            result = (temp[0], horiz_order[temp[1]], horiz_order[temp[2]])
            #print "base_result:", result
            return result
        
        else:
            # divide
            midpoint = int(math.ceil(num_clusters/2.0))
            #print "midpoint:", num_clusters, "/2.0 =", midpoint
            cluster_idx1 = horiz_order[midpoint - 1]
            cluster_idx2 = horiz_order[midpoint]
            hor_mid = (cluster_list[cluster_idx1].horiz_center() + cluster_list[cluster_idx2].horiz_center())/2.0
            #print "hor_mid =", hor_mid
            horiz_left = horiz_order[:midpoint]
            horiz_right = horiz_order[midpoint:]
            horiz_left_set = set(horiz_left)
            horiz_right_set = set(horiz_right)
            
            vert_left = []
            vert_right = []
            for vert_idx in vert_order:
                if vert_idx in horiz_left_set:
                    vert_left.append(vert_idx)
                if vert_idx in horiz_right_set:
                    vert_right.append(vert_idx)
            
            # conquer
            #fast_helper() returns one tuple
            left_result = fast_helper(cluster_list, horiz_left, vert_left)
            right_result = fast_helper(cluster_list, horiz_right, vert_right)
            
            if left_result[0] < right_result[0]:
                closest_pair = left_result
            else:
                closest_pair = right_result
            
            close_mid = []  #S
            for vert_idx in vert_order:
                if abs(cluster_list[vert_idx].horiz_center() - hor_mid) < closest_pair[0]:
                    close_mid.append(vert_idx)
            num_close_mid = len(close_mid)  #k
            for idx_u in range(num_close_mid - 1):
                start_v = idx_u + 1
                end_v = min(idx_u + 3, num_close_mid - 1)
                for idx_v in range(start_v, end_v + 1):
                    pair_uv = pair_distance(cluster_list, close_mid[idx_u], close_mid[idx_v])
                    if pair_uv[0] < closest_pair[0]:
                        closest_pair = pair_uv
            
        return closest_pair
            
    # compute list of indices for the clusters ordered in the horizontal direction
    hcoord_and_index = [(cluster_list[idx].horiz_center(), idx) 
                        for idx in range(len(cluster_list))]    
    hcoord_and_index.sort()
    horiz_order = [hcoord_and_index[idx][1] for idx in range(len(hcoord_and_index))]
     
    # compute list of indices for the clusters ordered in vertical direction
    vcoord_and_index = [(cluster_list[idx].vert_center(), idx) 
                        for idx in range(len(cluster_list))]    
    vcoord_and_index.sort()
    vert_order = [vcoord_and_index[idx][1] for idx in range(len(vcoord_and_index))]
    
    #print "horiz_order:", horiz_order
    #print "vert_order:", vert_order
    
    # compute answer recursively
    answer = fast_helper(cluster_list, horiz_order, vert_order) 
    return (answer[0], min(answer[1:]), max(answer[1:]))

    
    
def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function mutates cluster_list
    
    Input: List of clusters, number of clusters
    Output: List of clusters whose length is num_clusters
    
    DONE
    """
    
    num_remain = len(cluster_list)
    
    while num_remain > num_clusters:
        closest_pair = fast_closest_pair(cluster_list)
        idx_1 = closest_pair[1]
        idx_2 = closest_pair[2]
        cluster_list[idx_1] = cluster_list[idx_1].merge_clusters(cluster_list[idx_2])
        cluster_list.remove(cluster_list[idx_2])
        num_remain = len(cluster_list)
        #print "num_remain:", num_remain
    
    return cluster_list



def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    
    Input: List of clusters, number of clusters, number of iterations
    Output: List of clusters whose length is num_clusters
    """
    
    def center_distance(cluster_center, center_point):
        """
        input:
            cluster_center: a tuple
            center_point: a tuple
        output:
            the Euclidean distance between the two points
        """
        vert_dist = cluster_center[1] - center_point[1]
        horiz_dist = cluster_center[0] - center_point[0]
        return math.sqrt(vert_dist ** 2 + horiz_dist ** 2)
        
    # initialize k-means clusters to be initial clusters with largest populations
    pop_and_index = [(cluster_list[idx].total_population(), idx) 
                        for idx in range(len(cluster_list))]    
    pop_and_index.sort()
    pop_order = [pop_and_index[idx][1] for idx in range(len(pop_and_index))]
    centers = [(cluster_list[idx].horiz_center(), cluster_list[idx].vert_center()) for idx in pop_order[:-(num_clusters+1):-1]]
    print "initial centers: ", centers
    for dummy_iteration in range(num_iterations):
        #if iteration == 0:
        #    kmeans_clusters = list(centers)
        #else:
        kmeans_clusters = []
        for idx in range(num_clusters):
            kmeans_clusters.append(alg_cluster.Cluster(set([]), centers[idx][0], centers[idx][1], 0, 0.0))
        
        for cluster in cluster_list:
            cluster_center = (cluster.horiz_center(), cluster.vert_center())
            dists = [center_distance(cluster_center, center) for center in centers]
            min_idx = dists.index(min(dists))
            kmeans_clusters[min_idx].merge_clusters(cluster)
        
        centers = [(k_cluster.horiz_center(), k_cluster.vert_center()) for k_cluster in kmeans_clusters]
    
    return kmeans_clusters


