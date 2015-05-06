# Code based off of the publically available code at https://github.com/trevlovett/Python-Ant-Colony-TSP-Solver

from ant_colony import AntColony
from ant_graph import AntGraph

import sys
import traceback

# NOTE: CITIES ARE ASSUMED TO BE 0 INDEXED INTERNALLY. ONLY ON FILE OUTPUT ARE CITIES ONE INDEXED

class AntNPTSPRunner:
    def __init__(self, num_nodes, distances, colors):
        """Each instance of AntNPTSPRunner is responsible for running ant colonization on one input.
        Constructor takes in the number of nodes, matrix of distances and string of colors."""
        self.num_nodes = num_nodes
        self.distances = distances
        self.colors = colors
        self.best_path_vec = None
        self.best_path_cost = None
        self.best_path_colors = None
        self.__calculate()

    def __calculate(self):
        """Private method. Computes an optimal path using ant colonization."""
        # All values taken from paper
        self.num_ants = 10
        self.num_iterations = 200 #100 
        self.num_repetitions = 2 

        try:
            graph = AntGraph(self.num_nodes, self.distances,self.colors) # construct the graph
            self.best_path_cost = sys.maxint # initialize cost to infinity
            for i in range(0, self.num_repetitions): # run multiple repetitions. Run multiple repetitions because each iteration is random.
                graph.reset_tau()  # reset trail level
                ant_colony = AntColony(graph, self.num_ants, self.num_iterations) # construct ant colony
                ant_colony.start()
                if ant_colony.best_path_cost < self.best_path_cost: # if we found a better path, take that path
                    self.best_path_vec = ant_colony.best_path_vec
                    self.best_path_cost = ant_colony.best_path_cost
            self.best_path_colors = [graph.get_color(node) for node in self.best_path_vec]

        except Exception, e:
            print "exception: " + str(e)
            traceback.print_exc()

    def get_best_path(self):
        """Returns vector containing of the best path computed. This is 0 indexed. Raises an exception if calculate()
        has not yet been called"""
        if self.best_path_vec == None:
            raise Exception("No best path yet calculated")
        return self.best_path_vec

    def get_best_path_cost(self):
        """Returns cost of the best path computed."""
        if self.best_path_cost == None:
            raise Exception("No best path yet calculated")
        return self.best_path_cost

    def get_best_path_colors(self):
        """Returns colors of the best path computed. Use this to check validity of paths computed."""
        if self.best_path_colors == None:
            raise Exception("No best path yet calculated")
        return self.best_path_colors
    