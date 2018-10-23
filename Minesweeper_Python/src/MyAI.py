# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
import numpy as np

UNKNOWN = -1
def _print(array):
	print(np.flip(np.swapaxes(array, 0, 1), 0))

# class Queue():
# 	def __init__(self):
# 		self.queue = []


class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self.rowDimension = rowDimension
		self.colDimension = colDimension
		self.array = np.array([[UNKNOWN for _ in range(colDimension)] for _ in range(rowDimension)])
		# self.move = [(3,3), (2,2), (1,1)]
		self.startX, self.startY = startX, startY
		self.x, self.y = startX, startY                     #set (x,y) start from start (x,y)
		self.array[self.x, self.y] = 0                      #display my world to debug
		self.frontier = []                                  #ready to expand
		self.explored = []                                  #already explored
		self.flag = []                                      #these are bombs/mines
		self.frontier = self.addNeighbors(startX, startY)   #add start(x,y) all possible neighbors to frontier list

		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################

		# Display my own world: array
		# get cord(x,y) and its number
		# add cord(x,y) to array
		self.array[self.x, self.y] = number
		print("MY WORLD:")
		_print(self.array)

		# Add (x,y) to explored list after agent uncovered it
		if not self.isExplored(self.x, self.y):
			self.explored.append((self.x, self.y))
		print("explored: ", self.explored)

		# When agent uncovers any tile with number 0,
		# get all its possible neighbors and add them to frontier list
		if number == 0:
			for i,j in self.addNeighbors(self.x, self.y):
				self.frontier.append((i,j))
		print("frontier:", self.frontier)


		# Go through my world
		# if numer == 1 and it has the same amount of hiddenTile as the number on the square
		# Add (i,j) to flag list
		for a in range(self.rowDimension):
			for b in range(self.colDimension):
				if self.array[a,b] == 1:
					for i,j in self.addToFlag(a,b):
						if (i,j) not in self.flag:
							self.flag.append((i,j))
		print("flag:", self.flag)

		# Go through my world
		# if number == 1 and it has the same amount of flag as the number on the square
		# uncover all rest of (i,j)
		for a in range(self.rowDimension):
			for b in range(self.colDimension):
				if self.array[a,b] == 1:
					for i,j in self.addToUncover(a,b):
						if (i,j) not in self.flag and (i,j) not in self.frontier:
							self.frontier.append((i,j))


		# if frontier list is not empty, pop it as (x,y) to uncover
		if self.frontier:
			self.x, self.y = self.frontier.pop()
			print("NEXT CORD TO UNCOVER: (", self.x, ",", self.y, ")")
			print("POP (", self.x, ",", self.y, ")", "ALL OTHER POSSIBLE TILES IN FRONTIER:", self.frontier)
			return Action(AI.Action.UNCOVER, self.x, self.y)


		#just testing, this move is to uncover all cord listed in the list called move
		# if self.move:
		# 	self.x, self.y = self.move.pop()
		# 	print("NEXT CORD TO UNCOVER: (",self.x, ",", self.y, ")")
		# 	return Action(AI.Action.UNCOVER, self.x, self.y)

		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################
	'''
	function: getNeighbors
	input: given (a,b)
	output: return a list of (a,b)'s all possible neighbors, max: 8 neighbors
	'''
	def getNeighbors(self, a, b):
		possibleN = [(a-1, b-1),(a-1, b),(a-1, b+1),\
		       (a, b-1), (a, b+1), (a+1, b-1), (a+1, b), (a+1, b+1)]

		return [(i,j) for i,j in possibleN if (i >=0 and i < self.colDimension and j >= 0 and j < self.rowDimension)]

	'''
	function: addNeighbors
	input: given (a,b)
	output: return a list of (a,b)'s neighbors (filter: not in frontier list and not in explored list)
	'''
	def addNeighbors(self, a, b):
		# for i,j in self.getNeighbors(self.x, self.y):
		# 	if(i >= 0 and i < self.colDimension and j >= 0 and j < self.rowDimension):
		# 		print(i,j)
				# self.array[i,j] = "Q"
		"""
			get neighbors
			if cord is not in queue, then add to queue
			if already uncover or added in queue, don't add again
		"""
		# self.frontier

		L = []
		for i,j in self.getNeighbors(a, b):
			if (i,j) not in self.frontier and (i,j) not in self.explored:
				L.append((i,j))
		return L

	'''
	function: isExplored 
		if it's not explored yet, then add it to explored after uncover it
	input: given (a,b)
	output: return true(if already explored)/false(if not explored yet)
	'''
	def isExplored(self, a, b):
		if (a,b) not in self.explored:
			return False
		else: True


	'''
	for now, only deal with number 1
	given (a,b), if its 7 neighbors has been explored, then mark the last neighbor as Bomb
	add it to a Bomb list so as to skip this one
	also for other functions, need to consider bomb list before uncover
	'''

	# logic: if a tile has the same amount of flags around it as the number on the square
	#        then all remaining hidden tiles around it are not bombs

	'''
	function: addToFlag
	input: given (a,b)
	output: return a list (either empty or a list of HiddenTile)
	'''
	def addToFlag(self, a, b):
		numOfHiddenTile = 0
		HiddenTile = []
		for i,j in self.getNeighbors(a,b):
			if (i,j) not in self.explored:
				numOfHiddenTile +=1
				HiddenTile.append((i,j))

		if numOfHiddenTile == 1:
			return HiddenTile
		else:
			return []

	'''
	function: addToUncover
	input: given (a,b)
	output: return a list (either empty or a list of HiddenTile)
	'''
	def addToUncover(self, a, b):
		numOfFlag = 0
		numOfHiddenTile = 0
		HiddenTile = []
		for i,j in self.getNeighbors(a,b):
			if (i,j) in self.flag:
				numOfFlag += 1

			if (i,j) not in self.explored:
				numOfHiddenTile +=1
				HiddenTile.append((i,j))

		if numOfFlag == 1 and numOfHiddenTile > 0:
			return HiddenTile
		else:
			return []



		# numOfFlag = 0
		# numOfHiddenTile = 0
		# HiddenTile = []
		# for i,j in self.getNeighbors(a, b):
		# 	# get number of flags around (a,b)
		# 	# if (i,j) in self.flag:
		# 	# 	numOfFlag += 1
		#
		#
		# 	# get number of hidden tiles around (a,b)
		# 	# add those hidden tiles to a list
		# 	if (i,j) not in self.explored:
		# 		numOfHiddenTile += 1
		# 		HiddenTile.append((i,j))
		#
		# # if numOnSquare == numOfFlag:
		# 	# uncover all remaining hidden tiles
		# 	# if numOfHiddenTile > 0:
		# 		# return hiddenTile list to frontier list to uncover
		# 		# return HiddenTile
		# if numOnSquare > numOfFlag and numOnSquare == numOfHiddenTile:
		# 	# if numOnSquare == numOfHiddenTile:
		# 		# return hiddenTile list to flag list to mark it as bomb
		# 	return HiddenTile

		# else:
			# do nothing for current tile, and check next tile
			# return -1



	# def addToBomb(self, a, b):
	# 	pass
		# L = []
		# count = 0
		# for i,j in self.getNeighbors(a,b):
		# 	'''
		# 	if there are 7 (i,j) is explored, then add the last one to a bomb list
		# 	'''
		# 	if (i,j) in self.explored:
		# 		count += 1
		# if count == 7:
		# 	if (i,j) not in self.explored:
		# 		L.append((i, j))
		# 	return L
		# else:
		# 	'''
		# 	if count != 7, that means not sure which has a bomb
		# 	so find another number 1, and do addToBomb again
		# 	if there is no other number 1, then exit, and leave the game for now
		# 	'''