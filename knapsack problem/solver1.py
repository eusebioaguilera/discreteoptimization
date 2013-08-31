#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict
import gc
import weakref

"""

    This program solves the knapsack problem using the branch & bound 
    algoritm. This program also destroy pruned parts of the tree for 
    avoiding memory problem of previous version.

"""

class Node(object):
	def __init__( self ):
         self.optimistic = 0.0
         self.value = 0.0
         self.remain_capacity = 0
         self.children = []
         self.father = None
         self.pruned = False
         self.taken = True
         self.level = 0

	def add_child(self, obj):
		obj.father = weakref.ref( self ) # Weak ref to break circular references
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
    feasibles_optimal = list()
    value_optimal = 0
    iteration = 0

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
        feasibles_optimal.append( 0 )
    
    # calculate optimistic solution
    optimal = calculateOptimistic( values, weights, capacity, feasibles )
    
    # Create root node for first-depth branch & bound algorithm
    root = Node( )
    root.optimistic = optimal
    root.remain_capacity = capacity
    root.optimistic = optimal
    father = root
    optimal_node = root
    move = "down"
    
    gc.enable( )
    
    while True:
        # Branch nodes
        
        if len( father.children ) == 0:
            # Generate left node
            node = Node()
            node.remain_capacity = father.remain_capacity - weights[ father.level ]
    
            if node.remain_capacity >= 0:
                node.value = father.value + values[ father.level ]
                node.optimistic = optimal
                node.taken = True
                move = "down"
            else:
                node.pruned = True # Because is not a feasible solution
                move = "up"
            
            father.add_child( node )
            
        elif len( father.children ) == 1:
            # Generate rigth node
            node = Node()
            node.remain_capacity = father.remain_capacity
            node.value = father.value
            
            feasibles[ father.level ] = 0
            
            for i in range( father.level + 1, items ):
                feasibles[ i ] = 1
            
            # Recalculate optimistic value not to taking 
            optimal = calculateOptimistic( values, weights, capacity, feasibles )
            
            node.optimistic = optimal
            
            if node.optimistic <= optimal_node.value:
                move = "up"
                node.pruned = True
            else:
                move = "down"
                node.taken = False
            
            father.add_child( node )
            
        else:
            # We have to go to up and prune this solution
            move = "up"
        
        if node.level == items:
            # Feasible solution
            if node.value > value_optimal:
                #optimal_node = node
                value_optimal = node.value
                for i in range( items ):
                    feasibles_optimal[ i ] = feasibles[ i ]
            
            # Move up
            move = "up"
        
        if move == "down":
            father = node
        else:
            if len( father.children ) == 2:
                to_destroy = father
                father = father.father( )
                
                for child in to_destroy.children:
                    to_destroy.children.remove( child )
                    child = None
                
#                iteration += 1
#                
#                if iteration % 100000 == 0:
#                    print gc.get_referrers( to_destroy )
#                    print "GC is enabled?", gc.isenabled()
#                    dump_garbage()
                
                #print gc.get_threshold(), gc.get_count()
                # Call garbage collector
                #gc.collect( )
        
        
        if father.level == 0 and len( father.children ) == 2:
            break

    
    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    #value = 0
    #weight = 0
    #taken = []

#    for i in range(0, items):
#        if weight + weights[i] <= capacity:
#            taken.append(1)
#            value += values[i]
#            weight += weights[i]
#        else:
#            taken.append(0)
    
    # Prepare the solution    
    #current_node = optimal_node
    value = int( value_optimal )
    taken = feasibles_optimal
    
#    for i in range( items ):
#        taken.append( 0 )
#    
#    while current_node.level != 0:
#        if current_node.taken:
#            taken[ current_node.level - 1 ] = 1
#        
#        current_node = current_node.father
    

    
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

