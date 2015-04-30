import sys
import traceback

def best_graph(input_num_str, num_vertices_str, non_path_val):
    """Inputs:
    input_num = number of the input file; either 1, 2, or 3
    num_vertices = number of vertices in the graph


    Returns:
    graph[x][y] where x is the row number and y is the column number 
    """

    print("Creating input file number: " + input_num_str)
    input_num = int(input_num_str)
    num_vertices = int(num_vertices_str)
    M = int(non_path_val)
    
    graph = [[0 for x in range(num_vertices)] for x in range(num_vertices)]

    try:
        s = "SkysTheLimit" + input_num_str + ".in"
        print(s)
        file = open(s, "w")
        file.write(num_vertices_str + "\n")

        NS = set([8 * i + 2 for i in range(1, 6)] + [8 * i + 5 for i in range(6)]) #set of N and S vertices

        #vertices on the diamond paths (vertices on path numbered 1 - 48 in order)
        for i in range(num_vertices):
            for j in range(num_vertices):
                if i == j: 
                    graph[i][j] = 0
                elif i >= 48 or j >= 48:
                    graph[i][j] = 2 * M
                elif abs(i - j) == 47: #edge between first and last vertex on path
                    graph[i][j] = 2 * M 
                elif abs(i - j) == 1: #edges next to each other on the path
                    graph[i][j] = 1
                elif (((i % 8 == 0 and j % 8 == 4) or (i % 8 == 4 and j % 8 == 0)) and abs(i - j) == 4): 
                    #edges in the diamond that are not on the path
                    graph[i][j] = 0
                elif (((i % 8 == 3 and j % 8 == 7) or (i % 8 == 7 and j % 8 == 3)) and abs(i - j) == 4):
                    #edges in the diamond that are not on the path
                    graph[i][j] = 0
                elif i in NS and j in NS and abs(i - j) > 3: #if connecting any non-consecutive N and S vertices
                    graph[i][j] = 0
                elif (i == 2 and j in NS) or (j == 2 and i in NS): #first N vertex to any other edge in NS
                    graph[i][j] = M
                else:
                    graph[i][j] = 2 * M 

        #copying graph into file
        edges = ""
        for x in range(num_vertices):
            for y in range(num_vertices):
                if y == num_vertices - 1: #last column needs new line instead of trailing space
                    edges += str(graph[x][y]) + "\n"
                else:
                    edges += str(graph[x][y]) + " " 
        file.write(edges)

        #assigning colors to vertices
        colors = ""
        red = 0 
        for i in range(num_vertices - 1):
            if red >= 2:
                colors += "R"
                if red == 2:
                    red += 1
                else:
                    red = 0

            else:
                colors += "B"
                red += 1
        colors += "R"
        file.write(colors)
        file.close()
    except Exception as e:
        print("FAILED")
        print(e)
        sys.exit(0)


if __name__ == '__main__':
    """Note that input_num and num_vertices are strings"""
    input_num = sys.argv[1]
    num_vertices = sys.argv[2]
    non_path_val = sys.argv[3]
    best_graph(input_num, num_vertices, non_path_val)
