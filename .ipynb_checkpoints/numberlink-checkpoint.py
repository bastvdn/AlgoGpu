#!/usr/bin/env python
#-*- coding: utf-8 -*-
import time
import sys
from search import *

#################
# Problem class #
#################

class NumberLink(Problem):
	def __init__(self, initial):
		continue

	def goal_test(self, state):
        return None
    
    def actions(self, state):
        return None
    
    def result(self, state, action):
        return None


######################
# Auxiliary function #
######################

directions = [ [0, -1], [0, 1], [-1, 0], [1, 0] ]

def pathExists(grid, start, end):
	visited = [ [0 for j in range(0, len(grid[0]))] for i in range(0, len(grid)) ]
	ok = pathExistsDFS(grid, start, end, visited)
	return ok

def pathExistsDFS(grid, start, end, visited):
	for d in directions:
		i = start[0] + d[0]
		j = start[1] + d[1]
		next = [i, j]
		if i == end[0] and j == end[1]:
			return True
		if inBounds(grid, next) and grid[i][j] == '.' and not visited[i][j]:
			visited[i][j] = 1
			exists = pathExistsDFS(grid, next, end, visited)
			if exists:
				return True
	return False

def inBounds(grid, pos):
	return 0 <= pos[0] and pos[0] < len(grid) and 0 <= pos[1] and pos[1] < len(grid[0])

#####################
# Launch the search #
#####################





