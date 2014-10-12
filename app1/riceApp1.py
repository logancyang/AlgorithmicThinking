#!/usr/bin/env python

'''
Algorithmic Thinking Application 1:
Citation Graph Anaysis
'''

import math
import matplotlib.pyplot as plt
import random

"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import urllib2

# Set timeout for CodeSkulptor if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph



'''
Functions for computing the in-degree distribution
'''

def make_complete_graph(num_nodes):
    '''
    input: num_nodes - the number of nodes in the digraph
    output: a complete digraph with such number of nodes
    '''
    
    if num_nodes <= 0:
        return {}
    else:
        digraph = {}
        for nodei in range(0, num_nodes):
            digraph[nodei] =set([])
            for nodej in range(0, num_nodes):
                if nodej != nodei:
                    digraph[nodei].add(nodej)
        return digraph

    
def compute_in_degrees(digraph):
    '''
    input: a digraph
    output: the in-degree of every node
    '''
    
    in_degree = {}
    #initialize all values to 0
    for node, adjlist in digraph.iteritems():
        in_degree[node] = 0
    
    #count in-degrees for each node
    for node, adjlist in digraph.iteritems():
        for nodei in adjlist:
            in_degree[nodei] += 1
    
    return in_degree

def compute_out_degrees(digraph):
    '''
    computes the out-degree of a digraph
    '''
    
    out_degree = {}
    #initialize all values to 0
    for node, adjlist in digraph.iteritems():
        out_degree[node] = len(digraph[node])
    
    return out_degree    

def in_degree_distribution(digraph):
    '''
    input: a digraph
    output: the in-degree distribution of the digraph
    '''
    
    in_degree = compute_in_degrees(digraph)
    in_degree_vals = in_degree.values()
    in_degree_dist = dict.fromkeys(in_degree_vals, 0)
    # print "in_degree_dist initialized to", in_degree_dist
    
    # important: get the distribution from dict
    # if not loop over (val, count), just val, val will be (val, count)
    for val in in_degree_dist.iteritems():
        for degree in in_degree.iteritems():
            if degree[1] == val[0]:
                in_degree_dist[val[0]] += 1
    
    return in_degree_dist

def normalize(distribution):
    values = distribution.values()
    total = sum(values)
    new_values = [float(x)/total for x in values]
    new_dist = dict(zip(distribution.keys(), new_values))
    return new_dist


'''
Compute in-degree distribution for the citation graph
'''

#in_degree_citation = in_degree_distribution(citation_graph)
#in_degree_citation = normalize(in_degree_citation)
#degree_freq = in_degree_citation.values()
#degree = in_degree_citation.keys()

#print in_degree_citation

#plt.loglog(degree,degree_freq,'ro',basex=2,basey=2)
#plt.xlim([1, 2**13])
#plt.ylabel('frequency')
#plt.xlabel('in-degree')
#plt.title('Normalized in-degree distribution of the citation graph')
#plt.show()

def randomDigraph(num_nodes, prob):
    '''
    Generate a digraph with num_nodes nodes.
    Edge exists given probability prob
    '''
    
    keys = range(0, num_nodes)
    digraph = dict.fromkeys(keys)
    for nodei in range(0, num_nodes):
        for nodej in range(0, num_nodes):
            rand = random.uniform(0, 1)
            if nodei != nodej and rand < prob:
                if digraph[nodei] == None:
                    digraph[nodei] = set([nodej])
                else:    
                    digraph[nodei].add(nodej)
    # remove empty values
    digraph_new = dict((k, v) for k, v in digraph.iteritems() if v)
    return digraph_new


"""
Provided code for application portion of module 1

Helper class for implementing efficient version
of DPA algorithm
"""


class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors
    
def DPA(n, m):
    '''
    generate a random digraph
    n: total number of nodes in the output graph
    m: number of nodes in the start_graph (a complete digraph)
    output: a DPA digraph with n nodes
    '''
    
    graphV = make_complete_graph(m)
    #print "V:", graphV
    graphDPA = DPATrial(m)
    for i in range(m, n):
        #print graphDPA._node_numbers
        new_neighbors = graphDPA.run_trial(m)
        #print "new_neighbors:", new_neighbors
        graphV[i] = new_neighbors
    return graphV


#citation_graph = load_graph(CITATION_URL)
#cite_n = len(citation_graph)
#cite_outdeg = compute_out_degrees(citation_graph)
#totoutdeg = sum(cite_outdeg.values())
#avgoutdeg = totoutdeg/cite_n
#print totoutdeg, avgoutdeg


DPA_graph = DPA(27770, 12)
#print DPA_graph
#DPA_indeg = compute_in_degrees(DPA_graph)


#print len(DPA_indeg)
#print DPA_dist


#my_graph = randomDigraph(2770, 0.05)
in_degree_my = in_degree_distribution(DPA_graph)
in_degree_my = normalize(in_degree_my)
degree_freq = in_degree_my.values()
degree = in_degree_my.keys()


plt.loglog(degree,degree_freq,'ro',basex=2,basey=2)
plt.xlim([1, 2**13])
plt.ylabel('frequency')
plt.xlabel('in-degree')
plt.title('Normalized in-degree distribution of the DPA digraph')
plt.show()








"""
def DPA_my(n, m):
    '''
    generate a random digraph
    n: total number of nodes in the output graph
    m: number of nodes in the start_graph (a complete digraph)
    output: a DPA digraph with n nodes
    '''
    
    graphV = make_complete_graph(m)
    #print "V:", graphV
    for i in range(m, n):
        #print ""
        #print "i:", i
        #print "V:", graphV
        indegV = compute_in_degrees(graphV)
        #print "indegV:", indegV
        totindeg = sum(indegV.values())
        #print "totindeg:", totindeg
        # the new set of nodes j (maximum m nodes) for the new edges of i
        new_set = set([])
        counter = 0
        for j in range(0, i):
            #print "j:", j
            prob_addj = float((indegV[j] + 1))/(totindeg + len(graphV))
            graphV[i] = new_set
            rand = random.uniform(0,1)
            #print "rand, prob", rand, prob_addj
            if rand < prob_addj:
                new_set.add(j)
                counter += 1
                #print "counter:", counter
            if counter > m:
                break
    return graphV
"""

