'''
Algorithmic Thinking Project 1:
Degree Distributions for Graphs
'''

EX_GRAPH0 = {0: set([1, 2]), 1: set([]), 2: set([]) }
EX_GRAPH1 = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3]), 3: set([0]), 4: set([1]), 5: set([2]), 6: set([]) }
EX_GRAPH2 = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3, 7]), 3: set([7]), 4: set([1]), 5: set([2]), 6: set([]),
    7: set([3]), 8: set([1, 2]), 9: set([0, 3, 4, 5, 6, 7])}

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
    for node, adjlist in digraph.iteritems():
        in_degree[node] = 0
    
    for node, adjlist in digraph.iteritems():
        for nodei in adjlist:
            in_degree[nodei] += 1
    
    return in_degree

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

#print make_complete_graph(0)
#print make_complete_graph(5)
#
#degree_2 = compute_in_degrees(EX_GRAPH2)
#print degree_2
#
#print in_degree_distribution(EX_GRAPH2)
