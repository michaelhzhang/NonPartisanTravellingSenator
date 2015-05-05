from compute_paths import *
from dp import *

def test_on_input(input):
    (num_nodes, adj_mat, colors) = process_input(input)
    path = nptsp_dp(num_nodes, adj_mat, colors)
    print path

