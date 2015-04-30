from antcolony import AntColony
from antgraph import AntGraph

import pickle
import sys
import traceback

#default
num_nodes = 10

if __name__ == "__main__":   
    # has a default number of nodes; this lets you set the number of nodes
    if len(sys.argv) > 1 and sys.argv[1]:
        num_nodes = int(sys.argv[1])

    if num_nodes <= 10:
        num_ants = 20
        num_iterations = 12
        num_repetitions = 1
    else:
        num_ants = 28 # Do we want to increase the number of ants to be higher?
        num_iterations = 20 # Increase the number of iterations higher?
        num_repetitions = 1

    stuff = pickle.load(open("citiesAndDistances.pickled", "r"))
    cities = stuff[0] # do we need the pickling?
    cost_mat = stuff[1]

    if num_nodes < len(cost_mat): # If num_nodes is smaller than your matrix, truncate the matrix
        cost_mat = cost_mat[0:num_nodes] 
        for i in range(0, num_nodes): 
            cost_mat[i] = cost_mat[i][0:num_nodes]

    print cost_mat

    try:
        graph = AntGraph(num_nodes, cost_mat) # construct the graph
        best_path_vec = None 
        best_path_cost = sys.maxint # initialize cost to infinity
        for i in range(0, num_repetitions): # run multiple repetitions. Run multiple repetitions because each iteration is random.
            graph.reset_tau()  # reset trail level
            ant_colony = AntColony(graph, num_ants, num_iterations) # construct ant colony
            ant_colony.start()
            if ant_colony.best_path_cost < best_path_cost: # if we found a better path, take that path
                best_path_vec = ant_colony.best_path_vec
                best_path_cost = ant_colony.best_path_cost

        print "\n------------------------------------------------------------"
        print "                     Results                                "
        print "------------------------------------------------------------"
        print "\nBest path = %s" % (best_path_vec,)
        for node in best_path_vec:
            print cities[node] + " ",
        print "\nBest path cost = %s\n" % (best_path_cost,)
    
    except Exception, e:
        print "exception: " + str(e)
        traceback.print_exc()
