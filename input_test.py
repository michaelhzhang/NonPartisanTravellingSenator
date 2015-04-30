import sys

# Run this on a specific input file, specified as command line arguments
if __name__ == "__main__":
	# allow multiple command line arguments corresponding to different files
	if len(sys.argv) > 1:
		for arg in sys.argv[1:]: # Start at index 1 to ignore the file name "input_test.py"
			fin = open(str(arg), "r")
			N = int(fin.readline())
			distances = [[] for i in range(N)]
			for i in xrange(N):
				distances[i] = [int(x) for x in fin.readline().split()]
			colors = fin.readline()
			print distances
			print colors
