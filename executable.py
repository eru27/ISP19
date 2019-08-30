import graph as gp
import evaluating as el
import optimization as opt

from datetime import datetime
import math

FOLDER_GRAPH = 'res/graphs/'
FOLDER_PARAMETERS = 'res/parameters/'

VERSION = 'mgmi'


minminmin = 999999
'''
minminGraph = None
minAvgCost = -1
minP0 = -1
minPG = -1
minG = -1
minMaxG = -1
'''

AVG_COST = 100

P0 = 0.9
PG = 0.01
MAX_G = 600
G = int(MAX_G * 0.2)

TEMPERATURE_0 = (-AVG_COST) / (math.log(P0))
TEMPERATURE = TEMPERATURE_0
STEP = (-AVG_COST / (TEMPERATURE_0 * math.log(PG))) ** (1 / G)

def writeParameters(fileName, energy):
    f = open(fileName, 'w')
    
    f.write('Energy' + ',' + energy + '\n')

    '''
    f.write('AVG_COST' + ',' + str(minAvgCost) + '\n')
    f.write('P0' + ',' + str(minP0) + '\n')
    f.write('PG' + ',' + str(minPG) + '\n')
    f.write('G' + ',' + str(minG) + '\n')
    f.write('MAX_G' + ',' + str(minMaxG) + '\n')
    f.write('\n')
    '''

    f.write('NUMBER_OF_HARD_CONSTRAINTS' + ',' + str(el.NUMBER_OF_HARD_CONSTRAINTS) + '\n')
    f.write('NUMBER_OF_SOFT_CONSTRAINTS' + ',' + str(el.NUMBER_OF_SOFT_CONSTRAINTS) + '\n')
    f.write('MAX_LECTURES_PER_DAY_FOR_PROF' + ',' + str(el.MAX_LECTURES_PER_DAY_FOR_PROF) + '\n')
    f.write('H0_PENALTY' + ',' + str(el.H0_PENALTY) + '\n')
    f.write('S1_PENALTY' + ',' + str(el.S1_PENALTY) + '\n')
    f.write('S2_PENALTY' + ',' + str(el.S2_PENALTY) + '\n')
    f.write('S3_PENALTY' + ',' + str(el.S3_PENALTY) + '\n')
    f.write('S4_PENALTY' + ',' + str(el.S4_PENALTY) + '\n')
    f.write('S5_PENALTY' + ',' + str(el.S5_PENALTY) + '\n')
    f.write('S6_PENALTY' + ',' + str(el.S6_PENALTY) + '\n')
    f.write('S7_PENALTY' + ',' + str(el.S7_PENALTY) + '\n')
    f.write('S8_PENALTY' + ',' + str(el.S8_PENALTY) + '\n')

    f.close()

def getFileName():
    fN = str(datetime.now())
    fN = fN.replace('-', '').replace(' ', '').replace(':', '').replace('.', '')

    return fN

def getParameters():
    return [P0, PG, G, MAX_G]

def getMin():
    graph = gp.getGraph()

    #print(len(graph.nodes))

    Energy = el.calculateEnergy(graph, opt.banLecturesForProfessors, opt.banLecturesForGrades)

    changesCounter = 0

    global TEMPERATURE

    generation = 0
    minPenalty = Energy[0]
    minEnergy = Energy
    minGraph = graph
    #k = 1
    
    while generation < MAX_G:
        graph, Energy, change = opt.annealing(graph, Energy, TEMPERATURE)
        changesCounter += change

        if minPenalty > Energy[0]:
            minPenalty = Energy[0]
            minEnergy = Energy
            minGraph = graph
        '''
        if generation % 100 == 0:
            print(generation, changesCounter, Energy[0], TEMPERATURE)
        '''
        #if TEMPERATURE > 1:    
        TEMPERATURE = TEMPERATURE * STEP
        
        '''
        print('jebiii seeee')
        else:
            TEMPERATURE = TEMPERATURE_0 * (STEP ** k)
            k += 1
        '''
        generation += 1
    '''
    fileName = getFileName()

    gp.writeGraph(minGraph, getParameters(), fileName)
    '''
    '''
    print(minPenalty, minEnergy[1][0])
    print(TEMPERATURE_0, TEMPERATURE, STEP)
    print(AVG_COST)
    print(P0, PG)
    print(G, MAX_G)
    print(dee/MAX_G)
    print('-')
    '''
    #print(minEnergy[1][0], minEnergy[2][0][0], minEnergy[2][1][0], minEnergy[2][2][0], minEnergy[2][3][0], minEnergy[2][4][0], minEnergy[2][5][0], minEnergy[2][6][0], minEnergy[2][7][0])

    return minGraph, minEnergy

def mejn():
    global MAX_G
    global minminmin

    global G
    global STEP

    for MAX_G in [100, 200, 500, 1000]:
        G = int(MAX_G * 0.2)
        STEP = (-AVG_COST / (TEMPERATURE_0 * math.log(PG))) ** (1 / G)

        graph1, energy1 = getMin()
        graph2, energy2 = getMin()
        graph3, energy3 = getMin()
        
        minE = min(energy1[0], energy2[0], energy3[0])

        if energy1[0] == minE:
            graph = graph1
        elif energy2[0] == minE:
            graph = graph2
        else:
            graph = graph3

        if minE < minminmin:
            minminmin = minE

        gp.writeGraph(graph, [minE] + getParameters(), 'outForMaxg/' + VERSION + getFileName())

    print(minminmin)   
        

mejn()

'''
def mejn():
    avgCostVal = [20]
    maxGVal = [100, 200, 400]
    GVal = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    P0Val = [0.99, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]
    PGVal = [0.05, 0.04, 0.03, 0.02, 0.01, 0.005]

    global AVG_COST
    global MAX_G
    global G
    global P0
    global PG
    
    global minminmin
    global minminGraph
    global minAvgCost
    global minP0
    global minPG
    global minG
    global minMaxG

    minGraph = None
    minEnergy = None

    for avgCost in avgCostVal:
        AVG_COST = avgCost
        for maxG in maxGVal:
            MAX_G = maxG
            for g in GVal:
                G = g * MAX_G
                for p0 in P0Val:
                    P0 = p0
                    for pg in PGVal:
                        PG = pg

                        global TEMPERATURE_0
                        global TEMPERATURE
                        global STEP

                        TEMPERATURE_0 = (-AVG_COST) / (math.log(P0))
                        TEMPERATURE = TEMPERATURE_0
                        STEP = (-AVG_COST / (TEMPERATURE_0 * math.log(PG))) ** (1 / G)

                        graph1, energy1 = getMin()
                        graph2, energy2 = getMin()
                        graph3, energy3 = getMin()

                        if energy1[0] <= energy2[0] and energy1[0] < energy3[0]:
                            minGraph = graph1
                            minEnergy = energy1
                        elif energy2[0] <= energy1[0] and energy2[0] < energy3[0]:
                            minGraph = graph2
                            minEnergy = energy2
                        else:
                            minGraph = graph3
                            minEnergy = graph3
                        
                        #print(minGraph)
                        #print(minEnergy[0], '.')
                        if minEnergy[0] < minminmin:
                            minminmin = minEnergy[0]
                            minminGraph = minGraph
                            minAvgCost = AVG_COST
                            minP0 = P0
                            minPG = PG
                            minG = G
                            minMaxG = MAX_G

                        print('.')

                print(minminmin)

                fileName = getFileName()
                gp.writeGraph(minminGraph, [minminmin] + getParameters(), FOLDER_GRAPH + VERSION + fileName)
                writeParameters(FOLDER_PARAMETERS + VERSION + fileName)
'''
