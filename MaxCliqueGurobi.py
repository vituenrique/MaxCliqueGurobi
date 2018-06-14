from gurobipy import *

def solverMaxClique(graph, model_name):
    try:
		m = Model(model_name)

		x = {}
		for i in range(len(graph)):
			x[i] = m.addVar(vtype=GRB.BINARY, name = 'x[' + str(i) + ']')
		m.update()

		m.addConstrs((x[i] + x[j] <= 1 for i in range(len(graph)) for j in range(len(graph)) if graph[i][j] == 0 and i != j), "C1")

		m.setObjective(sum([x[i] for i in range(len(graph))]), GRB.MAXIMIZE)

		m.optimize()

		solution = m.getAttr('x', x)

		m.write('Models/' + model_name + '.lp')
		
		return solution
    
    except GurobiError as e:
    	print('Error code ' + str(e.errno) + ": " + str(e))
    
    except AttributeError:
        print('Encountered an attribute error')

def createMatrixGraph(vertices, edges):
	graph = [[0 for x in range(int(vertices))] for y in range(int(vertices))] 
	for i in xrange(0, len(edges) - 1, 2):
		graph[int(edges[i]) - 1][int(edges[i + 1]) - 1] = 1	
		graph[int(edges[i + 1]) - 1][int(edges[i]) - 1] = 1	
	return graph

def processData(data):
	data = data.replace("p edge ", "").replace("e ", "").split("\n")
	#print data	
	_return = []
	for i in range(len(data)):
		if (i == 0): 
			vertices = data[i].split(" ")[0]
			nEdges = data[i].split(" ")[1]
			continue
			#print data[i].split(" ")
		_return.append(data[i].split(" ")[0])
		_return.append(data[i].split(" ")[1])
	return [vertices, nEdges, _return]

def readFile(filepath):
	with open(filepath, "r") as fileReader:
		file = fileReader.read()
		return file

def main():
	filepaths = []
	filepaths.append("Instances/1-FullIns_5.txt")
	filepaths.append("Instances/queen6-6.txt")
	filepaths.append("Instances/myciel5.txt")
	filepaths.append("Instances/miles750.txt")
	
	for i in range(len(filepaths)):
		filepath = filepaths[i]	
		
		file = readFile(filepath)
		
		data = processData(file)
		
		graph = createMatrixGraph(data[0], data[2])
		
		clique = solverMaxClique(graph, "Max-Clique-" + filepath.replace("Instances/", "").replace(".txt", ""))

if __name__ == '__main__':
	main()
