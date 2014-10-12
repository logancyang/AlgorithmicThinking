'''
Algorithmic Thinking Application 2:
Analysis of a computer network
'''
from collections import deque
import urllib2
import random
import time
import math
import matplotlib.pyplot as plt


############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order
    


##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


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


#######################################################################################
# My code
def make_complete_graph(num_nodes):
    '''
    input: num_nodes - the number of nodes in the digraph
    output: a complete ugraph with such number of nodes
    '''
    
    if num_nodes <= 0:
        return {}
    else:
        ugraph = {}
        for nodei in range(0, num_nodes):
            ugraph[nodei] =set([])
            
        for nodei in range(0, num_nodes):
            for nodej in range(0, num_nodes):
                if nodej != nodei:
                    ugraph[nodei].add(nodej)
                    ugraph[nodej].add(nodei)
        return ugraph

def make_ergraph(num_nodes, prob):
    '''
    input:
        num_nodes - the number of nodes in the digraph
        prob - the probability there is an edge
    output: a complete ugraph with such number of nodes
    '''
    
    if num_nodes <= 0:
        return {}
    else:
        ugraph = {}
        for nodei in range(0, num_nodes):
            ugraph[nodei] =set([])
            
        for nodei in range(0, num_nodes):
            for nodej in range(0, num_nodes):
                if nodej != nodei:
                    rand = random.uniform(0,1)
                    if rand < prob:
                        ugraph[nodei].add(nodej)
                        ugraph[nodej].add(nodei)
        return ugraph

def display_stat(ugraph):
    '''
    Display the number of nodes and edges of the ugraph
    '''
    print "------------------"
    print "num_node: ", len(ugraph)
    num_edge = 0
    for node, adjlist in ugraph.iteritems():
        num_edge += len(adjlist)
    num_edge = num_edge/2
    print "num_edge: ", num_edge
    print "------------------"

#######################################################################################    
def bfs_visited(ugraph, start_node):
    '''
    Takes the undirected graph ugraph and the node start_node and returns
    the set consisting of all nodes that are visited by a breadth-first search
    that starts at start_node.
    '''

    queue = deque()
    visited = set([start_node])
    queue.append(start_node)
    #print "queue: ", queue
    while len(queue) != 0:
        temp_node = queue.popleft()
        #print "1:", ugraph
        #print "2:", temp_node
        #print "3:", ugraph[temp_node]
        for neighbor in ugraph[temp_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited
    
def cc_visited(ugraph):
    '''
    Takes the undirected graph ugraph and returns a list of sets,
    where each set consists of all the nodes (and nothing else) in a connected
    component, and there is exactly one set in the list for each
    connected component in ugraph and nothing else.
    '''
    
    remaining_nodes = set(ugraph.keys())
    #print "remaining_nodes ", remaining_nodes
    connected_comp = []
    while len(remaining_nodes) != 0:
        rand_start = random.sample(remaining_nodes, 1)
        # sampled rand_start is a list
        current_comp = bfs_visited(ugraph, rand_start[0])
        #print "current_comp: ", current_comp
        remaining_nodes = remaining_nodes - current_comp
        #print "remaining_nodes ", remaining_nodes
        #current_comp = list(current_comp)
        connected_comp.append(current_comp)
    return connected_comp

def largest_cc_size(ugraph):
    '''
    Takes the undirected graph ugraph and returns the size (an integer) of
    the largest connected component in ugraph.
    '''
    
    connected_components = cc_visited(ugraph)
    #print "connected_components:", connected_components
    largest = 0
    for component in connected_components:
        if len(component) > largest:
            largest = len(component)
    return largest

def compute_resilience(ugraph, attack_order):
    '''
    input:
        ugraph: undirected graph
        attack_order: a list of nodes that will be removed
    output:
        resilience: a list of len(largest_connected_components)
        The k+1th entry is the len(largest_connected_components)
        after removing the first k nodes in attack_order.
        The 0th entry is the len(largest_connected_components) of the original ugraph
    '''
    resilience = [largest_cc_size(ugraph)]
    #print resilience
    for node_att in attack_order:
        # remove the nodes one by one
        for neighbor in ugraph[node_att]:
            ugraph[neighbor].remove(node_att)
        del ugraph[node_att]
        resilience.append(largest_cc_size(ugraph))
    return resilience


#######################################################################################
class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors
    
def UPA(n, m):
    '''
    generate a random ugraph
    n: total number of nodes in the output graph
    m: number of nodes in the start_graph (a complete digraph), avg degree of the simulated graph
    output: a UPA digraph with n nodes
    '''
    
    graphV = make_complete_graph(m)
    #print "V:", graphV
    graphUPA = UPATrial(m)
    for i in range(m, n):
        #print graphDPA._node_numbers
        new_neighbors = graphUPA.run_trial(m)
        #print "new_neighbors:", new_neighbors
        graphV[i] = new_neighbors
        for node in new_neighbors:
            graphV[node].add(i)
    return graphV

def random_order(ugraph):
    '''
    takes a graph and returns a list of the nodes in the graph in some random order. 
    '''
    nodelist = ugraph.keys()
    random.shuffle(nodelist)
    return nodelist

#######################################################################################
def fast_targeted_order(ugraph):
    '''
    input: an undirected graph
    output: the list of nodes with largest degree in descending order
    '''
    new_graph = copy_graph(ugraph)
    degree_sets = {}
    num_node = len(new_graph.keys())
    
    #print num_node
    
    for degree in range(num_node):
        degree_sets[degree] = set()
    for node, adjlist in new_graph.iteritems():
        deg = len(adjlist)
        degree_sets[deg].add(node)
        
    #print degree_sets
    
    tar_order = []
    #idx = 0
    for degree in range(num_node - 1, -1, -1):
        #print "for loop: degree_sets[", degree, "] = ", degree_sets[degree]
        while len(degree_sets[degree]) != 0:
            # node_u is a list with a single element here: [u]
            node_u = random.sample(degree_sets[degree], 1)
            degree_sets[degree].remove(node_u[0])
            #print node_u[0]
            #print "removed node_u degree_sets[degree]: ", degree_sets[degree]
            for neighbor in new_graph[node_u[0]]:
                deg_neighbor = len(new_graph[neighbor])
                #print "neigbor: ", neighbor
                #print "while degree = ", degree, ", degree_sets[", deg_neighbor, "]: ", degree_sets[deg_neighbor]
                if len(degree_sets[deg_neighbor]) != 0:
                    degree_sets[deg_neighbor].remove(neighbor)
                    #print "removed neighbor degree_sets[deg_neighbors]: ", degree_sets[deg_neighbor]
                degree_sets[deg_neighbor - 1].add(neighbor)
            tar_order.append(node_u[0])
            #idx += 1
            delete_node(new_graph, node_u[0])
            #print "it was here!"
    return tar_order
    


#######################################################################################
# Q1, Q2
#ER_graph = make_ergraph(1347, 0.00175)
#display_stat(ER_graph)
#ER_rand = random_order(ER_graph)
#ER_resilience = compute_resilience(ER_graph, ER_rand)
#
#UPA_graph = UPA(1347, 2)
#display_stat(UPA_graph)
#UPA_rand = random_order(UPA_graph)
#UPA_resilience = compute_resilience(UPA_graph, UPA_rand)
#
#ANS_graph = load_graph(NETWORK_URL)
#display_stat(ANS_graph)
#ANS_rand = random_order(ANS_graph)
#ANS_resilience = compute_resilience(ANS_graph, ANS_rand)
#
#
#plt.plot(ER_resilience, '-b', label='ER graph with p = 0.00175')
#plt.plot(UPA_resilience, '-r', label='UPA graph with m = 2')
#plt.plot(ANS_resilience, '-g', label='Computer network')
#plt.legend(loc='upper right')
#plt.ylabel('resilience')
#plt.xlabel('the number of nodes removed')
#plt.title('Resilience of ER, UPA and Computer Network Graphs')
#plt.show()

#######################################################################################
# Q3

def time_UPA_targeted():
    '''
    time the running time of UPA_targeted for UPA(n, 5), n in range(10, 1000, 10)
    output: a list of running times
    '''
    runningtime = []
    for n in range(10,1000,10):
        UPA_graph = UPA(n, 5)
        start_time = time.time()
        UPA_targeted = targeted_order(UPA_graph)
        end_time = time.time()
        t = end_time - start_time
        runningtime.append(t)
    return runningtime

def time_UPA_fast():
    '''
    time the running time of UPA_fast for UPA(n, 5), n in range(10, 1000, 10)
    output: a list of running times
    '''
    runningtime = []
    for n in range(10,1000,10):
        UPA_graph = UPA(n, 5)
        start_time = time.time()
        UPA_fast = fast_targeted_order(UPA_graph)
        end_time = time.time()
        t = end_time - start_time
        runningtime.append(t)
    return runningtime

#UPA_rand = random_order(UPA_graph)
#tar = time_UPA_targeted()
#fast = time_UPA_fast()
#
#plt.plot(tar, 'b-', label='targeted_order')
#plt.plot(fast, 'r-', label='fast_targeted_order')
#plt.legend(loc='upper left')
#plt.ylabel('runnning time (s)')
#plt.xlabel('n/10')
#plt.title('Running time of targeted_order vs fast_targeted_order for UPA(n, 5)')
#plt.show()

#######################################################################################
# Q4
ER_graph = make_ergraph(1347, 0.00175)
display_stat(ER_graph)
#ER_rand = random_order(ER_graph)
ER_fast = fast_targeted_order(ER_graph)
ER_resilience = compute_resilience(ER_graph, ER_fast)

UPA_graph = UPA(1347, 2)
display_stat(UPA_graph)
#UPA_rand = random_order(UPA_graph)
UPA_fast = fast_targeted_order(UPA_graph)
UPA_resilience = compute_resilience(UPA_graph, UPA_fast)

ANS_graph = load_graph(NETWORK_URL)
display_stat(ANS_graph)
#ANS_rand = random_order(ANS_graph)
ANS_fast = fast_targeted_order(ANS_graph)
ANS_resilience = compute_resilience(ANS_graph, ANS_fast)


plt.plot(ER_resilience, '-b', label='ER graph with p = 0.00175')
plt.plot(UPA_resilience, '-r', label='UPA graph with m = 2')
plt.plot(ANS_resilience, '-g', label='Computer network')
plt.legend(loc='upper right')
plt.ylabel('resilience')
plt.xlabel('the number of nodes removed')
plt.title('Resilience of ER, UPA and Computer Network under TARGETED attack')
plt.show()