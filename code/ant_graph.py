# Code based off of the publically available code at https://github.com/trevlovett/Python-Ant-Colony-TSP-Solver

from threading import Lock

# Everything is stored as a matrix. 

class AntGraph:
    # colors inputted as a string, taken from the input file
    def __init__(self, num_nodes, delta_mat, colors, tau_mat=None): 
        #print len(delta_mat)
        if len(delta_mat) != num_nodes:
            raise Exception("len(delta) != num_nodes")

        self.num_nodes = num_nodes
        self.delta_mat = delta_mat # matrix of node distance deltas
        self.lock = Lock()
        
        # initialize array of colors
        self.color_arr = []
        for char in colors:
            self.color_arr.append(char)

        # tau mat contains the amount of pheremone at node x,y. This block initializes tau_mat to all 0s
        if tau_mat is None:
            self.tau_mat = []
            for i in range(0, num_nodes):
                self.tau_mat.append([0]*num_nodes)

    def delta(self, r, s): # get method
        return self.delta_mat[r][s]

    def tau(self, r, s): # get method
        return self.tau_mat[r][s]

    # 1 / delta = eta or etha. Eta is the initial "attractiveness of the move", so this biases us towards a greedy implementation
    # TODO: What's a good value of eta to put on this when the distance is 0?
    def etha(self, r, s):
        if self.delta(r,s) == 0:
            return 2.5 # somewhat arbitrarily chosen
        return 1.0 / self.delta(r, s)

    # Returns color of city r
    def get_color(self,r):
        return self.color_arr[r]

    # Returns arry of colors of graph
    def get_colors(self):
        return self.color_arr

    # inner locks most likely not necessary
    def update_tau(self, r, s, val): # self explanatory
        lock = Lock()
        lock.acquire()
        self.tau_mat[r][s] = val
        lock.release()

    def reset_tau(self): # initializes all the taus to 1 / (num_nodes^2 * avg_distance)
        lock = Lock()
        lock.acquire()
        avg = self.average_delta()

        # initial tau 
        self.tau0 = 1.0 / (self.num_nodes * self.num_nodes * avg)

        #print "Average = %s" % (avg,)
        #print "Tau0 = %s" % (self.tau0)

        for r in range(0, self.num_nodes):
            for s in range(0, self.num_nodes):
                self.tau_mat[r][s] = self.tau0
        lock.release()

    # average delta in delta matrix
    def average_delta(self):
        return self.average(self.delta_mat)

    # average tau in tau matrix
    def average_tau(self):
        return self.average(self.tau_mat)

    # average val of a matrix
    def average(self, matrix):
        sum = 0
        for r in range(0, self.num_nodes):
            for s in range(0, self.num_nodes):
                sum += matrix[r][s]

        avg = sum / (self.num_nodes * self.num_nodes)
        return avg

