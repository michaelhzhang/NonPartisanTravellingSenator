import itertools

def nptsp_dp(num_nodes, adj_mat, colors):
    """ Computes the shortest path satisfying
    all the conditions of the NPTSP.

    num_nodes -- number of nodes in the graph
    adj_mat -- an N x N symmetric matrix, where N == num_nodes
    start -- a list of length num_nodes
    """
    # min_cost = 50000
    # the shortest path may start at any node
    # for start in range(num_nodes):
    #     path = given_starting_node(num_nodes, adj_mat, colors, start)
    #     if path_cost(path) < min_cost:
    #         min_cost = path_cost(path)
    #         min_path = path
    # return min_path

    # map each node to the best possible path starting at the node
    # return the path with least cost
    return min(map(lambda start: given_starting_node(num_nodes, adj_mat, colors, start), \
                   range(num_nodes)), \
                   key=lambda path: path_cost(adj_mat, path))

def given_starting_node(num_nodes, adj_mat, colors, start):
    """ Computes the shortest path starting at node start
    that satisfies all the conditions.

    num_nodes -- number of nodes in the graph
    adj_mat -- an N x N symmetric matrix, where N == num_nodes
    colors -- a list of length num_nodes
    start -- a number between 0 inclusive and num_nodes exclusive
    """
    last_three_colors = ["RRR", "RRB", "RBR", "RBB", "BRR", "BRB", "BBR", "BBB"]
    nodes = tuple([node for node in range(num_nodes) if node != start])

    # C(S, c, j), where S is the set of visited nodes so far
    # c is the last three colors encountered
    # c should be of the form [a, b, c], where a is the latest color
    # j is the end city
    subproblems = {}
    
    # base cases, when S = {}
    for triple in last_three_colors:
        subproblems[((), triple, start)] = [start]
        for node in nodes:
            subproblems[((), triple, node)] = None # not a valid path

    for subset_size in range(1, num_nodes): # iterate over increasing subset size
        subsets = itertools.combinations(set(nodes), subset_size)
        for subset in subsets: # iterate over all subsets of size subset_size
            for node in subset: # iterate over all nodes in the subset
                for triple in last_three_colors: # iterate over all possible last 3 colors
                    # update C(subset, triple, node)
                    # print "updating C" + str(subset) + " " + triple + " " + str(node)
                    update(subproblems, adj_mat, colors, subset, triple, node)
    
    # get all subproblems that visit every node
    paths = [subproblems[(nodes, c, j)] for j in nodes for c in last_three_colors]
    return min(paths, key=lambda path: path_cost(adj_mat, path)) # return the shortest path 
    

def update(subproblems, adj_mat, colors, visited, triple, end):
    """ Updates the subproblems dictionary entry with the key (visited, triple, end).

    subproblems -- a dictionary of subproblem solutions
    adj_mat -- the adjacency matrix
    colors -- the list of node color assignments
    visited -- the tuple of visited nodes, should be sorted
    triple -- the last three node colors encountered
    end -- the ending node
    """
    last_three_colors = ["RRR", "RRB", "RBR", "RBB", "BRR", "BRB", "BBR", "BBB"]

    # prev_triple contains the 2nd, 3rd, 4th last node colors
    # triple contains the 1st, 2nd, 3rd last node colors
    # so the first two colors of prev_triple must match the last two colors of triple
    valid_colors = [prev_triple for prev_triple in last_three_colors if prev_triple[:2] == triple[1:]]

    min_cost = 50000
    min_triple = triple
    min_node = end
    if triple[0] == colors[end]: # if the color of end matches the corresponding color in triple
        prev_visited = tuple([i for i in visited if i != end]) # copy the visited tuple and take out the node end
        if len(prev_visited) > 0:
            min_node = prev_visited[0]

        # finding the minimum path according to the recurrence
        for intermediate in prev_visited: # loop through all possible intermediate nodes
            for prev_triple in valid_colors: # loop through all valid color triples
                path = subproblems[(prev_visited, prev_triple, intermediate)]
                if path_cost(adj_mat, path) + adj_mat[intermediate][end] < min_cost:
                    min_cost = path_cost(adj_mat, path) + adj_mat[intermediate][end]
                    min_triple = prev_triple
                    min_node = intermediate
        
        # print (prev_visited, min_triple, min_node)
        # if min_node == 1:
            # print (prev_visited, min_triple, min_node)
        if subproblems[(prev_visited, min_triple, min_node)] is not None:
            subproblems[(visited, triple, end)] = subproblems[(prev_visited, min_triple, min_node)] + [min_node]
        else:
            subproblems[(visited, triple, end)] = None

    else: # subproblem is not valid
        subproblems[(visited, triple, end)] = None
  
def path_cost(adj_mat, path):
    """ Computes the path cost of a given path.

    adj_mat -- the adjacency matrix
    path -- a list of nodes
    """
    if path is None:
        return 50000

    # the zip puts each pair of neighbors in the path together in a tuple
    # then map each tuple (i.e. edge) to its length
    # then sum all the edge lengths up
    return sum(map(lambda (u, v): adj_mat[u][v], zip(path[:-1], path[1:])))

