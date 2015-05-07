from ant_nptsp_runner import AntNPTSPRunner
from LocalSearch import *
from dp import nptsp_dp
import os.path

import sys
import traceback

def process_input(filename):
    """Opens a file of name "filename" in the instances directory"""
    fin = open("../instances/" + filename, "r")
    num_nodes = int(fin.readline())
    distances = [[] for i in range(num_nodes)]
    for i in xrange(num_nodes):
        distances[i] = [int(x) for x in fin.readline().split()]
    colors = fin.readline().rstrip("\n") # Make sure to remove the \n
    return (num_nodes,distances,colors)

if __name__ == "__main__":
    NUM_INSTANCES = 495 #
    node_dict = {L+1:0 for L in xrange(0,50)}
    for i in xrange(0,NUM_INSTANCES):
        num_nodes,distances,colors = process_input(str(i+1) + ".in")
        node_dict[num_nodes] = node_dict[num_nodes] + 1

    print node_dict

