#!/usr/bin/env python
#-*- coding: utf-8 -*-
import time
import sys
import os
import os.path
import shutil
import copy

import search
from search import *
from search import Problem

#################
# Problem class #
#################

class NumberLink(Problem):
	def __init__(self, initial):
		self.initial = initial
		print(initial)

	def goal_test(self, state):


		for d in state.array:
			for n in d:
				if n == ".":
					return False
		return True

	def actions(self, state):
		actionsPossible = state.pathNextTo(state.lastPos)
		actionsValides = []
		for n in actionsPossible:
			if self.simulation(state,n):
				actionsValides.append(n)


		return actionsValides

	def result(self, state, action):
		pos = action
		newState = copy.deepcopy(state)
		newState.lastPos = pos
		newState.array[pos[0]][pos[1]] = state.activeLetter
		newState.pathEnded(state.activeLetter)
		#print(newState)
		return newState



	def simulation(self, state, action):
		newState = copy.deepcopy(state)
		newState.lastPos = action
		newState.array[action[0]][action[1]] = newState.activeLetter
		newState.pathEnded(state.activeLetter)
		if newState.deadEnd():
			return False
		else:
			return True

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


def openIn(name):
	pt = os.path.join("instances",name)
	monfichier = open(pt)
	text = monfichier.read()
	monfichier.close()
	text = text.split('\n')
	del text[-1]
	array = list()
	for n in text:
		array.append(list(n))

	return array


class State(object):

	def __init__(self, array):
		self.array = array
		self.remainingLetters =  self.getAllLetters()
		self.activeLetter = self.remainingLetters[0]
		[self.lastPos, self.targetPos] = self.getFirstPos()

		self.directions = [ [0, -1], [0, 1], [-1, 0], [1, 0] ]



	def __str__(self):
		for n in self.array:
			for i in n:
				print(i,end='')
			print()
		return ""

	def __lt__(self, other):
		return self.array[0] < other.array[0]

	def remaining(self):
		output = []
		for d in self.array:
			for n in d:
				if n not in output:
					output.append(n)
		output.remove(".")
		return output


	def pathEnded(self, letter):
		i = 0
		j = 0
		res = True
		list = []
		while i < len(self.array):
			while j < len(self.array[i]):
				if self.array[i][j] == letter:
					list.append([i,j])
				j +=1
			j = 0
			i += 1
		for start in list:
			if not self.isNextToLetter(start):
				res = False
				break
		if res == True:
			self.remainingLetters.remove(letter)
			if len(self.remainingLetters) != 0:
				self.activeLetter = self.remainingLetters[0]
				[self.lastPos, self.targetPos] = self.getFirstPos()

		return res

	def deadEnd(self):
		return not pathExists(self.array,self.lastPos,self.targetPos)


	def getAllLetters(self):
		output = []
		for d in self.array:
			for n in d:
				if n not in output:
					output.append(n)
		output.remove(".")
		return output

	def getFirstPos(self):
		res = []
		i=0
		j=0
		while i < len(self.array):
			while j < len(self.array[i]):

				if self.array[i][j] == self.activeLetter:
					res.append([i,j])

				j += 1
			j = 0
			i += 1
		return res


	def isNextTo(self,start,end):
		res = False
		for d in self.directions:
			i = start[0] + d[0]
			j = start[1] + d[1]
			if end == [i,j]:
				res = True
		return res

	def isNextToLetter(self,start):
		res = False
		for d in self.directions:
			i = start[0] + d[0]
			j = start[1] + d[1]

			if inBounds(self.array, [i,j]) and self.array[i][j] == self.array[start[0]][start[1]]:
				res = True
		return res

	def positionsOf(self, letter):
		i = 0
		j = 0
		pos=[]
		while i < len(self.array):
			while j < len(self.array[i]):
				if self.array[i][j] == letter:
					pos.append([i,j])
				j += 1
			j=0
			i += 1
		return pos

	def pathExistBetween(self,letter):
		pos = self.positionsOf(letter)
		return pathExists(self.array,pos[0],pos[1])

	def pathNextTo(self, pos):
		res = []
		for d in self.directions:
			i = pos[0] + d[0]
			j = pos[1] + d[1]
			next = [i, j]


			if inBounds(self.array, next) and self.array[i][j] == ".":
				res.append([i,j])

		return res


#####################
# Launch the search #
#####################


mystate = State(openIn("easy.in"))

prblm = NumberLink(mystate)
print(mystate)



node = search.depth_first_tree_search(prblm)
path=node.path()
for n in path:
	print(n.state)

#print(pathExists(mystate.array,[0,0],[0,1]))