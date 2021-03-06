# Code based off of the publically available code at https://github.com/trevlovett/Python-Ant-Colony-TSP-Solver

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

def score_path(num_nodes,distances,path, one_index = True):
    """Calculates the cost of path (given as a list of nodes, 1 indexed by default) given an instances with distances matrix "distances".
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

    #make output directory
    # if not os.path.exists("../output"):
    #     os.makedirs("../output")

    for i in xrange(236,NUM_INSTANCES):
        try:
            fout = open("../output_michael/" + str(i+1) + ".out","w")
            num_nodes,distances,colors = process_input(str(i+1) + ".in")
            #num_nodes, distances, colors = process_input("6.in") # For testing: 101.in is small


            if num_nodes <= 16:
                print "DP Case: " + str(i + 1)
                best_path_vec, best_path_cost = nptsp_dp(num_nodes,distances,colors)
                print best_path_cost

            else:
                print "Non-DP Case: " + str(i + 1)
                runner = AntNPTSPRunner(num_nodes,distances,colors)

                # print runner.get_best_path()
                # print "Current cost: " + str(runner.get_best_path_cost())
                # print runner.get_best_path_colors()

                # Output code
                best_path_vec = runner.get_best_path()
                best_path_cost = runner.get_best_path_cost()
                #Run LocalBeamSearch on Ant Colonization Output
                best_path_vec, best_path_cost = localBeamSearch(AntGraph(num_nodes,distances,colors),best_path_vec)
                
                #Run Local Beam Search on random inputs
                RandomResult = RandomStartLocalSearch(AntGraph(num_nodes,distances,colors))
                randomCost = RandomResult[1]
                randomPath = RandomResult[0]
                if best_path_cost > randomCost:
                    best_path_vec = randomPath
                    best_path_cost = randomCost

            # Hardcoded cases
            dumb_guess = [L+1 for L in range(0,num_nodes)]
            dumb_guess_cost = score_path(num_nodes,distances,dumb_guess)
            if (dumb_guess_cost < best_path_cost) and isLegit(AntGraph(num_nodes,distances,colors),dumb_guess):
                best_path_vec, best_path_cost = dumb_guess, dumb_guess_cost

            # Only replace previous answer if new answer is better
            if prev_answers is not None:
                #print "Previously computed"
                prev_cost = score_path(num_nodes,distances,prev_answers[i])
                # print "prev_cost: " + str(prev_cost)
                print best_path_cost, prev_cost
                if best_path_cost > prev_cost:
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
        except Exception, e:
            print "exception: " + str(e)
            traceback.print_exc()
    #fout.close()
