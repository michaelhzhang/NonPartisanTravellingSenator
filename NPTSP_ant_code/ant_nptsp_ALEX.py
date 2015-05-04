from ant_colony import AntColony
from ant_graph import AntGraph
from LocalSearch import localSearch,RandomStartLocalSearch,NearestNeighbor

import sys
import traceback

# NOTE: CITIES ARE ASSUMED TO BE 0 INDEXED INTERNALLY. ONLY ON FILE OUTPUT ARE CITIES INDEXED EXTERNALLY

if __name__ == "__main__":   
    # Process input
    # Run this on a specific input file, specified as command line arguments
    if len(sys.argv) != 2:
        raise Exception("Invalid number of command line arguments")
    f = sys.argv[1] # Start at index 1 to ignore the file name "input_test.py"
    fin = open(str(f), "r")
    num_nodes = int(fin.readline())
    distances = [[] for i in range(num_nodes)]
    for i in xrange(num_nodes):
        distances[i] = [int(x) for x in fin.readline().split()]
    colors = fin.readline()

    # TODO: Figure out optimal number of ants (research paper suggests this might be 10)
    if num_nodes <= 10:
        #num_ants = 1 # for testing
        num_ants = 20
        num_iterations = 12
        num_repetitions = 1 # TODO: Increase number of repetitions?
    else:
        num_ants = 28 
        num_iterations = 30 # TODO: INCREASE THIS?
        num_repetitions = 3 # TODO: INCREASE THIS?

    try:
        graph = AntGraph(num_nodes, distances,colors) # construct the graph
                #EDIT
        best_path_vec = None 
        best_path_cost = sys.maxint # initialize cost to infinity
        for i in range(0, num_repetitions): # run multiple repetitions. Run multiple repetitions because each iteration is random.
            graph.reset_tau()  # reset trail level
            ant_colony = AntColony(graph, num_ants, num_iterations) # construct ant colony
            ant_colony.start()
            if ant_colony.best_path_cost < best_path_cost: # if we found a better path, take that path
                best_path_vec = ant_colony.best_path_vec
                best_path_cost = ant_colony.best_path_cost
        best_path_colors = [graph.get_color(node) for node in best_path_vec]


        print "\n------------------------------------------------------------"
        print "                     Results                                "
        print "------------------------------------------------------------"
        print "\nBest path = %s" % (best_path_vec,)
        print "\nBest path cost = %s\n" % (best_path_cost,)
        print "\nBest path colors = %s\n" % (best_path_colors,)
        print "\nBest Path, cost improvement", localSearch(graph,best_path_vec)        #Run local search on output of ant colonization 
        M = RandomStartLocalSearch(graph)                                           #Run random graph generator + Local Search
        print "\nBest Path Randomized", [i+1 for i in M[0]],M[1]

        out_string = str(f).rstrip("in") + "out"
        fout = open(out_string, "w")

        # Output code:
        # find an answer, and put into assign
        assign = [0] * num_nodes
        for i in xrange(num_nodes):
            assign[i] = best_path_vec[i] + 1 # 1 index the nodes

        fout.write("%s\n" % " ".join(map(str, assign)))
        fout.close()

    except Exception, e:
        print "exception: " + str(e)
        traceback.print_exc()