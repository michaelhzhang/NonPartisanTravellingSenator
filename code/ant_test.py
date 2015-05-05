from ant import Ant
from ant_graph import AntGraph 
from ant_colony import AntColony 

import math
import random
import sys
from threading import *

def test_valid_color():
	num_nodes = 6
	delta_mat = [[0,1,1,1,1,1],[1,0,1,1,1,1],[1,1,0,1,1,1],[1,1,1,0,1,1],[1,1,1,1,0,1],[1,1,1,1,1,0]]
	num_ants = 1
	num_iterations = 10
	colors1 = "RRRRRR"
	colors2 = "RRRBBB"
	colors3 = "BBBBBB"
	
	graph1 = AntGraph(num_nodes,delta_mat,colors1)
	colony1 = AntColony(graph1,num_ants,num_iterations)
	ant1 = Ant(1, 1, colony1)
	ant1.last_3_colors = ("R","R","R")
	print "False: " + str(ant1.valid_color(1))
	ant1.last_3_colors = ("B","B","B")
	print "True: " + str(ant1.valid_color(1))
	ant1.last_3_colors = ("R","R","B")
	print "True: " + str(ant1.valid_color(1))

	graph2 = AntGraph(num_nodes,delta_mat,colors2)
	colony2 = AntColony(graph2,num_ants,num_iterations)
	ant2 = Ant(1, 1, colony2)
	ant2.last_3_colors = ("R","R","R")
	print "True: " + str(ant2.valid_color(3))
	print "False: " + str(ant2.valid_color(1))

	graph3 = AntGraph(num_nodes,delta_mat,colors3)
	colony3 = AntColony(graph3,num_ants,num_iterations)
	ant3 = Ant(1, 1, colony3)
	ant3.last_3_colors = ("R","R","R")
	print "True: " + str(ant3.valid_color(1))
	ant3.last_3_colors = ("B","B","B")
	print "False: " + str(ant3.valid_color(1))
	ant3.last_3_colors = ("B","R","B")
	print "True: " + str(ant3.valid_color(1))

def test_completable_path():
	num_nodes = 8
	delta_mat = [[0,1,1,1,1,1,1,1],[1,0,1,1,1,1,1,1],[1,1,0,1,1,1,1,1],[1,1,1,0,1,1,1,1],[1,1,1,1,0,1,1,1],[1,1,1,1,1,0,1,1],[1,1,1,1,1,1,0,1],[1,1,1,1,1,1,1,0]]
	num_ants = 1
	num_iterations = 10
	colors1 = "RRRRBBBB"

	graph1 = AntGraph(num_nodes,delta_mat,colors1)
	colony1 = AntColony(graph1,num_ants,num_iterations)

	
	ant1 = Ant(1, 1, colony1)

	print "testing reds_left initialization: " + str(ant1.reds_left)

	#Visited: 1,2,3
	ant1.currNode = 3 
	ant1.last_3_colors = ("R","R","R")
	self.reds_left = 1



