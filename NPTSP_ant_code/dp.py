import itertools

def nptsp_dp(num_nodes, adj_mat, colors):
    """ Computes the shortest path satisfying
    all the conditions of the NPTSP.

    num_nodes -- number of nodes in the graph
    adj_mat -- an N x N symmetric matrix, where N == num_nodes
    start -- a list of length num_nodes
    """
    min_cost = 50000
    # the shortest path may start at any node
    for start in range(num_nodes):
        path = given_starting_node(num_nodes, adj_mat, colors, start)
        if path_cost(path) < min_cost:
            min_cost = path_cost(path)
            min_path = path
    return min_path

def given_starting_node(num_nodes, adj_mat, colors, start):
    """ Computes the shortest path starting at node start
    that satisfies all the conditions.

    num_nodes -- number of nodes in the graph
    adj_mat -- an N x N symmetric matrix, where N == num_nodes
    colors -- a list of length num_nodes
    start -- a number between 0 inclusive and num_nodes exclusive
    """
    last_three_colors = ["RRR", "RRB", "RBR", "RBB", "BRR", "BRB", "BBR", "BBB"]
    nodes = [node for node in range(num_nodes)].remove(start)
    subproblems = {}

    # C(S, c, j), where S is the set of visited nodes so far
    # c is the last three colors encountered
    # c should be of the form [a, b, c], where a is the lastest color
    # j is the end city
    subproblems[(set([]), (), start)] = [start]

    for subset_size in range(1, num_nodes): # iterate over increasing subset size
        subsets = set(itertools.combinations(set(nodes), subset_size))
        for subset in subsets: # iterate over all subsets of size subset_size
            for node in subset: # iterate over all nodes in the subset
                for triple in last_three_colors: # iterate over all possible last 3 colors
                    # update C(subset, triple, node)
                    subproblems = update(subproblems, adj_mat, colors, subset, triple, node)
    
    nodes_set = set(nodes)
    paths = [subproblems(nodes_set, c, j) for j in nodes_set for c in last_three_colors]
    return min(paths, key=lambda path: path_cost(adj_mat, path)) # return the shortest path 
    

def update(subproblems, adj_mat, colors, visited, triple, end):
    """ Updates the subproblems dictionary entry with the key (visited, triple, end).

    subproblems -- a dictionary of subproblem solutions
    adj_mat -- the adjacency matrix
    colors -- the list of node color assignments
    visited -- the set of visited nodes
    triple -- the last three node colors encountered
    end -- the ending node
    """
    last_three_colors = ["RRR", "RRB", "RBR", "RBB", "BRR", "BRB", "BBR", "BBB"]
    min_cost = 50000
    if triple[0] == colors[end]: # if the color of end matches the corresponding color in triple
        prev_visited = set(visited) # copy the set visited and take out the node end
        prev_visited.remove(end)
        for intermediate in visited: # loop through all possible intermediate nodes
            for prev_triple in last_three_colors: # loop through all possible color triples
                if prev_triple[:2] == triple[1:]: # only consider the triples that are valid
                    path = subproblems[(prev_visited, prev_triple, intermediate)]
                    if path_cost(adj_mat, path) + adj_mat[intermediate][end] < min_cost:
                        min_cost = path_cost(adj_mat, path) + adj_mat[intermediate][end]
                        min_triple = prev_triple
                        min_node = intermediate
        visited.add(end)
        subproblems[(visited, triple, end)] = subproblems[(prev_visited, min_triple, min_node)] + [min_node]
    else:
        visited.add(end)
        subproblems[(visited, triple, end)] = None
    return subproblems
  
def path_cost(adj_mat, path):
    """ Computes the path cost of a given path.

    adj_mat -- the adjacency matrix
    path -- a list of nodes
    """
    if path is None:
        return 50000
    cost = 0
    for i in range(len(path) - 1):
        cost += adj_mat[path[i]][path[i+1]]
    return cost

