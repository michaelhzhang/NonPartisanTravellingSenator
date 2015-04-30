import math
import random
import sys
from threading import *

class Ant(Thread): # Each ant is its own thread of execution
    def __init__(self, ID, start_node, colony):
        Thread.__init__(self)
        self.ID = ID
        self.start_node = start_node
        self.colony = colony
        self.graph = self.colony.graph
        
        # Number of freds and blues remaining. We're guaranteed there are an equal number of reds and blues at the beginning.
        self.reds_left = self.graph.num_nodes / 2
        self.blues_left = self.graph.num_nodes / 2

        # Keep track of last 3 colors. First entry is most recent.
        self.last_3_colors = (None, None, None)

        # Initizlize stuff
        self.curr_node = self.start_node
        self.path_vec = [] # Keeps track of current path
        self.path_vec.append(self.start_node)
        self.path_cost = 0

        # Make sure to keep track of color for start node
        self.color_bookkeeping(self.curr_node)

        # same meaning as in standard equations
        self.Beta = 1 # Beta is the parameter that controls the influence of eta (the attractiveness)
        #self.Q0 = 1  # Q0 = 1 works just fine for 10 city case (no explore)
        self.Q0 = 0.5 # A constant used to determine how much pheremone to deposit
        self.Rho = 0.99 # Pheremone evaporation coefficient

        # store the nodes remaining to be explored here
        self.nodes_to_visit = {}

        for i in range(0, self.graph.num_nodes): 
            if i != self.start_node:
                self.nodes_to_visit[i] = i

        # create n X n matrix 0'd out to start
        self.path_mat = [] 

        for i in range(0, self.graph.num_nodes):
            self.path_mat.append([0]*self.graph.num_nodes)

    # overide Thread's run()
    def run(self):
        graph = self.colony.graph
        while not self.end():
            # we need exclusive access to the graph
            graph.lock.acquire()
            new_node = self.state_transition_rule(self.curr_node) # Choose next node according to probability from formula
            self.path_cost += graph.delta(self.curr_node, new_node) 

            # Update color stuff
            self.color_bookkeeping(new_node)

            self.path_vec.append(new_node)
            self.path_mat[self.curr_node][new_node] = 1  #adjacency matrix representing path

            #print "Ant %s : %s, %s" % (self.ID, self.path_vec, self.path_cost,)
            
            self.local_updating_rule(self.curr_node, new_node)
            graph.lock.release()

            self.curr_node = new_node

        # don't forget to close the tour
        # NOTE: Don't need to close the tour because this problem is on paths, not tours
        # self.path_cost += graph.delta(self.path_vec[-1], self.path_vec[0])

        # send our results to the colony
        self.colony.update(self)
        #print "Ant thread %s terminating." % (self.ID,)

        # allows thread to be restarted (calls Thread.__init__)
        self.__init__(self.ID, self.start_node, self.colony)

    def end(self):
        return not self.nodes_to_visit 

    def color_bookkeeping(self,node):
        # Update color tracking
        node_color = self.graph.get_color(node)
        self.last_3_colors = (node_color, self.last_3_colors[0], self.last_3_colors[1])
        if node_color == 'R':
            self.reds_left -= 1
        else:
            self.blues_left -= 1

    # Test to make sure not visiting same 3 colors in a row
    def valid_color(self,next_node):
        next_node_color = self.colony.graph.get_color(next_node)
        if ((self.last_3_colors[0]  == 'R') and (self.last_3_colors[1]  == 'R') and (self.last_3_colors[2]  == 'R') and (next_node_color == 'R')):
            return False
        elif ((self.last_3_colors[0]  == 'B') and (self.last_3_colors[1]  == 'B') and (self.last_3_colors[2]  == 'B') and (next_node_color == 'B')):
            return False
        else:
            return True

    # Test to make sure we will never run into paths where we don't have enough reds or blues to balance each other out
    def completable_path(self,next_node):
        next_node_color = self.colony.graph.get_color(next_node)
        next_reds_left = self.reds_left
        next_blues_left = self.blues_left
        if (next_node_color == 'B'):
            next_blues_left -= 1
        else:
            next_reds_left -= 1

        reds_in_a_row = 0
        blues_in_a_row = 0
        for i in xrange(len(self.last_3_colors)):
            if (i > 0) and (self.last_3_colors[i] != self.last_3_colors[i-1]):
                break
            if self.last_3_colors[i] == 'B':
                blues_in_a_row += 1
            elif self.last_3_colors[i] == 'R':
                reds_in_a_row += 1
        if next_node_color == 'R':
            reds_in_a_row += 1
        elif next_node_color == 'B':
            blues_in_a_row += 1

        # Can not complete path if we have to switch colors but there are none of the opposite color left
        if (next_reds_left == 0) and ((blues_in_a_row + next_blues_left) > 3):
            return False
        elif (next_blues_left == 0) and ((reds_in_a_row + next_reds_left) > 3):
            return False
        # Can not complete the path if ratio of reds to blues or blues to reds is 3:1
        elif (next_reds_left != 0) and ((next_blues_left / (next_reds_left * 1.0)) > 3):
            return False
        elif (next_blues_left != 0) and ((next_reds_left / (next_blues_left * 1.0)) > 3):
            return False
       
        return True


    # described in report -- determines next node to visit after curr_node
    def state_transition_rule(self, curr_node):
        graph = self.colony.graph
        q = random.random()
        max_node = -1
        iteration = 0

        #print self.last_3_colors
        while (max_node == -1):
            iteration += 1
            if (iteration > 100):
                # Probable error here
                raise Exception("Infinite Loop in Ant" + str(self.ID))
            if q < self.Q0: # Exploitation means deterministically visit the most "promising" adjacent node 
                #print "Exploitation"
                max_val = -1
                val = None

                for node in self.nodes_to_visit.values():
                    if graph.tau(curr_node, node) == 0:
                        raise Exception("tau = 0")

                    if self.valid_color(node) and self.completable_path(node):
                        val = graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta)
                        if val > max_val:
                            max_val = val
                            max_node = node
            else:
                #print "Exploration"
                pheremone_sum = 0

                # sentinel pattern
                node = -1

                for node in self.nodes_to_visit.values():
                    if self.valid_color(node) and self.completable_path(node):
                        if graph.tau(curr_node, node) == 0:
                            raise Exception("tau = 0")
                        pheremone_sum += graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta)
                if pheremone_sum == 0:
                    raise Exception("pheremone_sum = 0")

                avg = pheremone_sum / len(self.nodes_to_visit)

                #print "avg = %s" % (avg,)

                # Choose nodes semi-deterministically; true randomness comes from initial random placement of ants
                for node in self.nodes_to_visit.values():
                    if self.valid_color(node) and self.completable_path(node):
                        p = graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta) 
                        if p > avg:
                            #print "p = %s" % (p,)
                            max_node = node
        
            # If fail the first time, introduce more randomness
            q = random.random()

        if max_node < 0:
            raise Exception("max_node < 0")

        del self.nodes_to_visit[max_node]
        
        return max_node

    # phermone update rule for indiv ants
    def local_updating_rule(self, curr_node, next_node):
        graph = self.colony.graph
        val = (1 - self.Rho) * graph.tau(curr_node, next_node) + (self.Rho * graph.tau0)
        graph.update_tau(curr_node, next_node, val)

