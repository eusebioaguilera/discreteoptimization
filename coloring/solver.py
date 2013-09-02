#!/usr/bin/python
# -*- coding: utf-8 -*-

from constraint import *

"""
    This program solves the problem of graph coloring using constraint 
    programming
"""


def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    nodeCount = int(firstLine[0])
    edgeCount = int(firstLine[1])

    edges = []
    for i in range(1, edgeCount + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
    
    edges_list = {}
    for edge in edges:
        if not edges_list.has_key( edge[ 0 ] ):
            edges_list[ edge[ 0 ] ] = [ edge[ 1 ] ]
        else:
            edges_list[ edge[ 0 ] ].append( edge[ 1 ] )
    
    problem = Problem( )
    
    for i in range( nodeCount ):
        #print i
        problem.addVariable( i, range( nodeCount ) )
    
    for key in edges_list:
        for item in edges_list[ key ]:
            problem.addConstraint( lambda a, b: a != b, [ key, item ] )
            
    ss = problem.getSolutionIter( )
    counter = 1
    min_colors = nodeCount
    try:
        sol = ss.next( )
        colors = set( )
        for item in sol:
            colors.add( sol[ item ] )
        
        if len( colors ) < min_colors:
            min_colors = len( colors )
        
    except StopIteration:
        pass
    
    print "Minimal color solution:", min_colors, "colors!"
    
    s = problem.getSolution()
    
    a = set()    
    
    for key in s:
        a.add( s[ key ] )
    
    convert = dict( )    
    
    counter = 0    
    
    for key in a:
        convert[ key ] = counter
        counter += 1
        
    solution = list( )
    
    for key in s:
        solution.append( convert[ s[ key ] ] )
            
    # build a trivial solution
    # every node has its own color
    #solution = range(0, nodeCount)

    # prepare the solution in the specified output format
    outputData = str(counter+1) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, solution))

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
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'

