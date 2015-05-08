from dp import nptsp_dp, path_cost
from compute_paths import process_input, score_path
from LocalSearch import isLegit
from ant_graph import AntGraph
import os.path

import sys
import traceback

if __name__ == "__main__":
    NUM_INSTANCES = 495

    # Check if answer.out already exists
    prev_answers = None
    if os.path.isfile("../alex_full_answer.out"):
        prev_answer_file = open("../answer.out","r")
        prev_answers =[[] for i in xrange(0,NUM_INSTANCES)]
        for i in xrange(0,NUM_INSTANCES):
            prev_answers[i] = [int(x) for x in prev_answer_file.readline().split()]
    
    answer_file = open("../answer.out", "w")

    for i in xrange(0, NUM_INSTANCES):
        num_nodes,distances,colors = process_input(str(i + 1) + ".in")
        min_cost = 50000
        min_path = []
        output_folders = ["output_steph", "output_sky", "output_michael", "output_alex", "out_fix_dp"]
        for folder in output_folders:
            try:
                f = open("../" + folder + "/" + str(i + 1) + ".out", "r")
                path = [int(x) for x in f.readline().split()]
                if len(path) > 0:
                    if folder == ("out_fix_dp"):
                        curr_path_cost = 0
                        print("USING OUT_FIX_DP")
                    else:
                        curr_path_cost = score_path(num_nodes, distances, path)
                else:
                    curr_path_cost = 50000
                if curr_path_cost < min_cost and isLegit(AntGraph(num_nodes, distances, colors), path, Index=False):
                    min_cost = curr_path_cost
                    min_path = path
                f.close()
            except Exception, e:
                print "exception: " + str(e)
                traceback.print_exc()
        
        #checking path from answer.out
        path = prev_answers[i]
        if len(path) > 0:
            curr_path_cost = score_path(num_nodes, distances, path)
            if curr_path_cost < min_cost:
                min_cost = curr_path_cost
                min_path = path

        if len(min_path) == 0:
            print("NO PATH FOUND FOR CASE #: " + str(i + 1) + ".in")

        #write path to new answer_final.out
        answer_file.write("%s\n" % " ".join(map(str, min_path)))
    
    answer_file.close()
