import networkx as nx

IDFK_counter = 0

NUMBER_OF_PROFF = 0
NUMBER_OF_GRADES = 0

WORKING_DAYS = 5
LECTURES_PER_DAY = 8
NUMBER_OF_COLOURS = WORKING_DAYS * LECTURES_PER_DAY #Number of lectures slots

SOURCE = 'sources/legithehe.csv'
OUT = 'f.csv'

class Node:
    def __init__(self, proff = -1, grade = -1):
        'Creates node with def: proff = -1, grade = -1'
        self.proff = proff
        self.grade = grade
    
    def printNode(self):
        'Prints node as "proff,grade"'
        print(str(self.proff) + ',' + str(self.grade))


def initGraph(nodes):
    'Creates graph with Node as nodes and connects two nodes that have same .proff or .grade'
    graph = nx.Graph()
    graph.add_nodes_from(nodes) #Adds all Nodes form the list

    for i, node_1 in enumerate(nodes):
        for j, node_2 in enumerate(nodes[i + 1:]): #Checks for every node and every node that is after it in the list
            if node_1.proff == node_2.proff or node_1.grade == node_2.grade:
                graph.add_edge(nodes[i], nodes[i + j + 1])

    return graph

def colourGraph(graph):
    'Colours graph with greedy algorith first colouring nodes with highest degree'
    global IDFK_counter #Does nothing
    maxColour = 0 #Number of lecture slots used
    sortedNodes = sorted(list(graph.nodes()), key = lambda node: graph.degree[node], reverse = True) #Makes list of nodes sorted by node's degree 
        #with first having the highest degree
    for node in sortedNodes:
        listOfUsedColours = [0] * NUMBER_OF_COLOURS
        for neighbour in list(graph.adj[node]):
            try: #If != None doesn't work ig
                listOfUsedColours[graph.nodes[neighbour]['colour']] = 1 #Sets 1 in the listOUC for the colour neighbour is coloured
            except:
                IDFK_counter = IDFK_counter + 1 #Stil doesn't do anything
        colour = 0
        while listOfUsedColours[colour]: #Finding the first available colour ########Got to write exeption
            colour += 1
        if colour > maxColour: #Checks if new lecture slot is being used
            maxColour = colour
        graph.nodes[node]['colour'] = colour
    print(maxColour)
    
    return graph

def loadNodes(fileName):
    'Loads nodes form csv file with rows being proffesors and values being grades'
    f = open(fileName, 'r')
    nodes = []
    maxGrade = -1
    maxProff = -1
    '''
    for line in f.readlines():
        l = line.split(',')
        nodes.append(Node(int(l[0]), int(l[1])))
        if int(l[0]) > maxProff:
            maxProff = int(l[0])
        if int(l[1]) > maxGrade:
            maxGrade = int(l[1])
    '''
    for proff, line in enumerate(f.readlines()):
        grades = line.split(',') 
        for grade in grades[:-1]:
            nodes.append(Node(proff, int(grade)))
            if int(grade) > maxGrade:
                maxGrade = int(grade)
        if proff > maxProff:
            maxProff = proff
    f.close()
    global NUMBER_OF_PROFF
    NUMBER_OF_PROFF = maxProff + 1
    global NUMBER_OF_GRADES
    NUMBER_OF_GRADES = maxGrade + 1

    return nodes

def writeGraph(graph, fileName):
    'Writes graph in file by nodes as proff,grade,colour'
    f = open(fileName, 'w')
    for node in list(graph.nodes):
        f.write(str(node.proff) + ',' + str(node.grade) + ',' + str(graph.nodes[node]['colour']) + '\n')
    f.close()

def getGraph():
    nodes = loadNodes(SOURCE)

    g = initGraph(nodes)

    g = colourGraph(g)

    return g
'''
nodes = loadNodes(SOURCE)

for node in nodes:
    print(node.proff, node.grade)

g = initGraph(nodes)

print(g.number_of_edges())
print(g.number_of_nodes())

g = colourGraph(g)

writeGraph(g, OUT)
'''