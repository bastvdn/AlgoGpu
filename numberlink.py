#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
import os
import os.path
import shutil
import copy
import time
import math

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
            if "." in d:
                return False
        return True

    def actions(self, state):
        actionsPossible = state.pathNextTo(state.lastPos)
        actionsValides = [n for n in actionsPossible if self.simulation(state, n)]
        # actionsValidesOpti = self.sortActions(actionsValides, state)

        # actionsValidesOpti.reverse()
        return actionsValides

    def result(self, state, action):

        newState = copy.deepcopy(state)
        newState.action(action)
        print(newState)

        return newState

    # not working, it actually add time of execution
    def sortActions(self, array, state):
        distances = {}
        for action in array:
            dist = math.sqrt((action[0] - state.targetPos[0]) ** 2 + (action[1] - state.targetPos[1]) ** 2)
            actStr = str(action[0]) + str(action[1])
            distances[actStr] = dist

        return [[int(i[0][0]), int(i[0][1])] for i in sorted(distances.items(), key=lambda x: x[1], reverse=False)]

    def simulation(self, state, action):
        newState = copy.deepcopy(state)
        newState.action(action)
        return not newState.isInvalid()


######################
# Auxiliary function #
######################

directions = (0, -1), (0, 1), (-1, 0), (1, 0)


def pathExists(grid, start, end):
    visited = [[0 for j in range(0, len(grid[0]))] for i in range(0, len(grid))]
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
    return 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0])


def openIn(name):
    pt = os.path.join("instances", name)
    myFile = open(pt)
    text = myFile.read()
    myFile.close()
    text = text.split('\n')
    del text[-1]

    return [list(n) for n in text]


class State(object):

    def __init__(self, array):
        self.array = array
        self.remainingLetters = self.getAllLetters()
        self.activeLetter = self.remainingLetters[0]
        [self.lastPos, self.targetPos] = self.getFirstPos(self.activeLetter)

        self.directions = ((0, -1), (0, 1), (-1, 0), (1, 0))

    def __str__(self):
        for n in self.array:
            for i in n:
                print(i, end='')
            print()
        return ""

    def __lt__(self, other):
        return self.array[0] < other.array[0]

    def action(self, pos):
        self.lastPos = pos
        self.array[pos[0]][pos[1]] = self.activeLetter
        # newState.pathEnded(state.activeLetter)
        if self.isPathEnded():
            self.remainingLetters.remove(self.activeLetter)

            if len(self.remainingLetters) != 0:
                self.activeLetter = self.remainingLetters[0]
                [self.lastPos, self.targetPos] = self.getFirstPos(self.activeLetter)

        return None

    def isPathEnded(self):
        return self.isNextTo(self.lastPos, self.targetPos)

    def isInvalid(self):
        return self.deadEnd() or self.blockOtherPath()

    def deadEnd(self):
        return not pathExists(self.array, self.lastPos, self.targetPos)

    def blockOtherPath(self):

        for letter in self.remainingLetters:
            if letter != self.activeLetter:
                [start, end] = self.getFirstPos(letter)
                if not pathExists(self.array, start, end):
                    return True
        return False

    def getAllLetters(self):
        output = []
        for d in self.array:
            for n in d:
                if n not in output:
                    output.append(n)
        output.remove(".")
        return output

    def getFirstPos(self, letter):
        return [[i, j] for i, line in enumerate(self.array) for j, elem in enumerate(line) if elem == letter]

    def isNextTo(self, start, end):
        res = False
        for d in self.directions:
            i = start[0] + d[0]
            j = start[1] + d[1]
            if end == [i, j]:
                res = True
        return res

    def pathNextTo(self, pos):
        res = []
        for d in self.directions:
            i = pos[0] + d[0]
            j = pos[1] + d[1]
            next = [i, j]
            if inBounds(self.array, next) and self.array[i][j] == ".":
                res.append([i, j])

        return res

#####################
# Launch the search #
#####################


if __name__ == "__main__":
    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        name = "level2m.in"

    mystate = State(openIn(name))
    prblm = NumberLink(mystate)
    print(mystate)

    start_time = time.time()
    node = search.depth_first_graph_search(prblm)
    # node = search.breadth_first_graph_search(prblm)
    path = node.path()
    for n in path:
        print(n.state)
    print("--- Temps de recherche : %s secondes---" % (time.time() - start_time))
