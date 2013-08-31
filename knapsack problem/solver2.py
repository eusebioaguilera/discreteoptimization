#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

    This program solves the knapsack problem calculating the value/weight
    rate. The it sort theese values and keep selecting the objects until
    it have space into the knapsack

"""

from collections import OrderedDict

class Node(object):
	def __init__(self, value, optimistic, remain_capacity, taken):
		self.value = value
		self.optimistic = optimistic
		self.remain_capacity = remain_capacity
		self.children = []
		self.father = None
		self.pruned = False
		self.optimal = False
		self.taken = taken
		self.level = 0

	def add_child(self, obj):
		obj.father = self
		obj.level = self.level + 1
		self.children.append(obj)


def calculateOptimistic( values, weights, capacity, feasibles ):
    
    # calculate optimal value
    opt_dict = {}
    for i in range( len( feasibles ) ):
        if feasibles[ i ] == 1:
            opt_dict[ i ] = values[ i ] * 1.0 / weights[ i ]
    
    # sort dictionary
    sorted_dict = OrderedDict( sorted( opt_dict.items( ), key=lambda t: t[ 1 ], reverse=True ) )
    
    remain_capacity = capacity
    
    optimal = 0.0
    
    for item in sorted_dict:
        #print item, sorted_dict[ item ]
        if remain_capacity >= weights[ item ]:
            remain_capacity = remain_capacity - weights[ item ]
            #print remain_capacity, "=", remain_capacity+weights[ item ], "-", weights[ item ]
            optimal = optimal + values[ item ]
            #print optimal, "=", optimal-values[item], "+", values[ item ]
        else:
            # Sum remain value
            optimal = optimal + ( values[ item ] * ( remain_capacity * 1.0 / weights[ item ] ) )
            #print optimal, "=", optimal-( values[ item ] * ( remain_capacity * 1.0 / weights[ item ] ) ), "+", "(", values[ item ], "* (", remain_capacity, "* 1.0", "/", weights[ item ], ") )"
            break
    
    return optimal
    


def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    items = int(firstLine[0])
    capacity = int(firstLine[1])

    values = []
    weights = []

    for i in range(1, items+1):
        line = lines[i]
        parts = line.split()

        values.append(int(parts[0]))
        weights.append(int(parts[1]))

    items = len(values)

    
    feasibles = list()
    
    for i in range( items ):
		feasibles.append( 1 )
    
    # calculate optimal value
    opt_dict = {}
    for i in range( len( feasibles ) ):
        if feasibles[ i ] == 1:
            opt_dict[ i ] = values[ i ] * 1.0 / weights[ i ]
    
    # sort dictionary
    sorted_dict = OrderedDict( sorted( opt_dict.items( ), key=lambda t: t[ 1 ], reverse=True ) )
    
    remain_capacity = capacity
    value = 0
    weight = 0
    taken = []
    
    for i in range(items):
		taken.append(0)
    
    for item in sorted_dict:
		
		if remain_capacity - weights[ item ] >= 0:
			
			value += values[ item ]
			remain_capacity = remain_capacity - weights[ item ]
			weight += weights[ item ]
			taken[ item ] = 1
			
			#print remain_capacity, item, weights[ item ]
	
	
	
		
    
    
    
    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    #value = 0
    #weight = 0
    #taken = []

    #for i in range(0, items):
        #if weight + weights[i] <= capacity:
            #taken.append(1)
            #value += values[i]
            #weight += weights[i]
        #else:
            #taken.append(0)

    # prepare the solution in the specified output format
    outputData = str(value) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, taken))
    return outputData


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

