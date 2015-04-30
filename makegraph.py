import sys

def best_graph(input_num_str, num_vertices_str):
    """Inputs:
    input_num = number of the input file; either 1, 2, or 3
    num_vertices = number of vertices in the graph


    Returns:
    graph[x][y] where x is the row number and y is the column number 
    """

    print("Creating input file number: " + input_num_str)
    input_num = int(input_num_str)
    num_vertices = int(num_vertices_str)
    
    graph = [[0 for x in range(num_vertices)] for x in range(num_vertices)]

    try:
        s = "SkysTheLimit" + input_num_str + ".in"
        print(s)
        file = open(s, "w")
        file.write(num_vertices_str + "\n")
        #vertices on the diamond paths
        #for i in range (6):
        #copying graph into file
        edges = ""
        """
        for x in range(num_vertices):
            for y in range(num_vertices):
                if y == num_vertices - 1: #last column needs new line instead of trailing space
                    if x == num_vertices - 1: #last row needs no new line or trailing space
                        edges += graph[x][y].str()
                    else:
                        edges += graph[x][y].str() + "\n"
                else:
                    edges += graph[x][y].str() + " " 
        """
        file.close()
    except:
        print("FAILED")
        sys.exit(0)


if __name__ == '__main__':
    """Note that input_num and num_vertices are strings"""
    input_num = sys.argv[1]
    num_vertices = sys.argv[2]
    best_graph(input_num, num_vertices)
