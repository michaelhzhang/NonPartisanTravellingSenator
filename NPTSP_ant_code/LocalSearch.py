from ant_graph import AntGraph
def scorePath(G,Path):
	total = 0
	if len(Path)>1:
		for i in range(0,len(Path)-1):
			total += G.delta(Path[i],Path[i+1])
	return total
def isLegit(G,Path):
	color = G.get_color(Path[0])
	k = 1
	for i in range(1,len(Path)):
		if color==G.get_color(Path[i]):
			k+=1
		else:
			k = 1
			color = G.get_color(Path[i])
		if k >= 4:
			return False
	return True

def localSearch(G, Path): #Return Path, Score
	ScoreOriginal = scorePath(G,Path)
	Improvements = [(Path,ScoreOriginal)] #(NewPath, Score) Basically compilation of all better paths than current
	if len(Path)>1:
		for i in range(0,len(Path)-2):
			for j in range(i+1,len(Path)-1):
						OldCost =  G.delta(Path[i], Path[i+1]) + G.delta(Path[j],Path[j+1])
						NewCost =  G.delta(Path[i],Path[j+1]) + G.delta(Path[len(Path)-1],Path[i+1])
						if NewCost < OldCost:
							A = Path[0:i+1] + Path[j+1:] + Path[i+1:j+1]
							if isLegit(G,A):
								Improvements.append((A ,ScoreOriginal + NewCost-OldCost))
						OldCost =  G.delta(Path[i], Path[i+1])
						NewCost =  G.delta(Path[len(Path)-1],Path[0])
						if NewCost < OldCost:
							A = Path[i+1:] + Path[0:i+1] 
							if isLegit(G,A):
								Improvements.append((A,ScoreOriginal + NewCost-OldCost))
						TWOOPT = Path[0:i+1] + Path[i+1:j+1][::-1] + Path[j+1:]   #2OPT
						if scorePath(G,TWOOPT) < ScoreOriginal:
							if isLegit(G,TWOOPT):
								Improvements.append((TWOOPT, scorePath(G,TWOOPT)))
	L =  min(Improvements, key=lambda x: x[1])
	Improvements.remove(L)
	M = None
	if Improvements != []:
		M = min(Improvements, key=lambda x: x[1])
	if L[1] < ScoreOriginal:
		L = localSearch(G,L[0])
	if M!= None and M[1] < ScoreOriginal:
		M = localSearch(G,M[0])
	if M!= None and M[1] < L[1]:
		return M
	return L

def NearestNeighbor(G): #TERRIBLE APPROXIMATIONS
	bestPath = []
	bestCost = 1000000
	for i in range(0,G.num_nodes):
		visited = set()
		visited.add(i)
		current = i
		Path = [i]
		while len(visited) != G.num_nodes:
			bestNeighbor = None
			cost = 101
			for j in range(0,G.num_nodes):
				if not j in visited:
					if G.delta(current,j) < cost and isLegit(G,Path + [j]):
						cost = G.delta(current,j)
						bestNeighbor = j
			Path.append(bestNeighbor)
			current = bestNeighbor
			visited.add(bestNeighbor)
		if len(Path) < G.num_nodes+1:
			if scorePath(G,Path) < bestCost:
				bestPath = Path
				bestCost = scorePath(G,Path)
	return bestPath,bestCost,localSearch(G,bestPath)

def RandomStartLocalSearch(G):
	K = [i for i in range(0,G.num_nodes)]
	best = []
	num = 100000
	import random
	for i in range(0,100):
		while not isLegit(G,K):
			random.shuffle(K)
		Z = localSearch(G,K)
		if Z[1] < num:
			best = list(Z[0])
			num = Z[1]
	return best,num
