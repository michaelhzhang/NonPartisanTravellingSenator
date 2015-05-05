from ant_nptsp_runner import AntNPTSPRunner
from LocalSearch import *
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

def score_path(num_nodes,distances,path, one_index = True):
    """Calculates the cost of path (given as a list of nodes, 1 indexed) given an instances with distances matrix "distances".
    If one_index is False, assume that the path is zero indexed.
    """
    cost = 0
    for i in xrange(num_nodes - 1):
        if one_index:
            cur = path[i]-1
            next = path[i+1]-1
        else:
            cur = path[i]
            next = path[i+1]
        cost += distances[cur][next]

    return cost

if __name__ == "__main__":
    # TODO: Exception handling?
    NUM_INSTANCES = 495 # Default to 495

    # Check if answer.out already exits
    prev_answers = None
    if os.path.isfile("answer.out"):
        prev_answer_file = open("answer.out","r")
        prev_answers =[[] for i in xrange(0,NUM_INSTANCES)]
        for i in xrange(0,NUM_INSTANCES):
            prev_answers[i] = [int(x) for x in prev_answer_file.readline().split()]
        prev_answer_file.close()

    # Output file
    fout = open("answer.out","w")
    for i in xrange(0,NUM_INSTANCES):
        processed = process_input(str(i+1) + ".in") # Note for testing: 101.in is really small
        runner = AntNPTSPRunner(num_nodes, distances, colors)

        # print runner.get_best_path()
        # print runner.get_best_path_cost()
        # print runner.get_best_path_colors()

        # Output code
        best_path_vec = runner.get_best_path()

        # Only replace previous answer if new answer is better
        if prev_answers is not None:
            #print "Previously computed"
            prev_cost = score_path(num_nodes,distances,prev_answers[i])
            #print "prev_cost: " + str(prev_cost)
            if runner.get_best_path_cost() > prev_cost:
                assign = prev_answers[i]
                fout.write("%s\n" % " ".join(map(str, assign)))
            else:       
                assign = [0] * num_nodes
                for j in xrange(num_nodes):
                    assign[j] = best_path_vec[j] + 1 # 1 indexes the nodes
            fout.write("%s\n" % " ".join(map(str, assign)))
        else:       
            assign = [0] * num_nodes
            for j in xrange(num_nodes):
                assign[j] = best_path_vec[j] + 1 # 1 indexes the nodes
            fout.write("%s\n" % " ".join(map(str, assign)))

    fout.close()