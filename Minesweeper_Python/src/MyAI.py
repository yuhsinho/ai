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

class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self.rowDimension = rowDimension
		self.colDimension = colDimension
		self.startX, self.startY = startX, startY
		self.totalMines = totalMines
		# a board B and square B_x,y
		self.B = np.array([[UNKNOWN for _ in range(colDimension)] for _ in range(rowDimension)])

		# initial B_x,y is given by (startX, startY)
		self.x, self.y = startX, startY

		# initial K(B_x,y) must be 0 and add it to board B
		self.B[self.x, self.y] = 0

		self.frontier = []
		self.explored = []
		self.flag = []

		# add R_x,y (as the set of all squares adjacent to B_x,y) to frontier list
		self.frontier = self.addNeighbors(startX, startY)

		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################

		# Add square B_x,y and its number K(B_x,y) to board B
		self.B[self.x, self.y] = number

		# Display my board B
		print("MY BOARD B:")
		_print(self.B)

		# Check if B_x,y is explored. If not, add B_x,y to explored list
		for i,j in self.isExplored(self.x, self.y):
			self.explored.append((i,j))
		print("explored: ", self.explored)

		# if K(B_x,y) == 0, add R_x,y to frontier list
		if number == 0:
			for i,j in self.addNeighbors(self.x, self.y):
				self.frontier.append((i,j))
		print("frontier:", self.frontier)

		# Apply Theorem 1
		for n in range(1,9):
			for a in range(self.rowDimension):
				for b in range(self.colDimension):
					if self.B[a,b] == n:
						for i,j in self.addToFlag(a,b,n):
							self.flag.append((i,j))
		print("flag:", self.flag)

		# Apply Theorem 2
		for n in range(1,9):
			for a in range(self.rowDimension):
				for b in range(self.colDimension):
					if self.B[a,b] == n:
						for i,j in self.addToUncover(a,b,n):
								self.frontier.append((i,j))

		# If TotalFlag == totalMines, add the rest unrevealed squares to frontier list
		if self.totalMines == self.TotalFlag():
			for i, j in self.addTheRest():
				self.frontier.append((i, j))

		# # for testing
		# if (1,3) not in self.frontier and (0,2) not in self.explored and (0,2) not in self.flag:
		# 	self.frontier.append((0,2))
		# if (1,1) not in self.flag:
		# 	self.flag.append((1,1))

		if self.frontier:
			self.x, self.y = self.frontier.pop()
			print("NEXT CORD TO UNCOVER: (", self.x, ",", self.y, ")")
			print("POP (", self.x, ",", self.y, ")", "ALL OTHER POSSIBLE TILES IN FRONTIER:", self.frontier)
			return Action(AI.Action.UNCOVER, self.x, self.y)

		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################
	'''
	function: getNeighbors(a, b)
	input: given coordinate(a,b)
	output: return a list of (a,b)'s all adjacent neighbors
	'''
	def getNeighbors(self, a, b):
		possibleN = [(a-1, b-1),(a-1, b),(a-1, b+1),\
		       (a, b-1), (a, b+1), (a+1, b-1), (a+1, b), (a+1, b+1)]

		return [(i,j) for i,j in possibleN if (i >=0 and i < self.colDimension and j >= 0 and j < self.rowDimension)]

	'''
	function: addNeighbors(a, b)
	input: given coordinate(a,b)
	output: return a list of (a,b)'s adjacent neighbors (filter: not in frontier list and not in explored list)
	'''
	def addNeighbors(self, a, b):
		L = []
		for i,j in self.getNeighbors(a, b):
			if (i,j) not in self.frontier and (i,j) not in self.explored:
				L.append((i,j))
		return L

	'''
	function: isExplored(a, b)	
	input: given coordinate(a,b)
	output: return (a,b) if it's not explored, return empty list if it's explored
	--> not sure why boolean dont work that well
	'''
	def isExplored(self, a, b):
		L = []
		if (a,b) not in self.explored:
			L.append((a,b))
		return L

	'''
	Theorem 1: 
	Given a board B and square B_x,y, 
	if # of unrevealed squares in R_x,y == K(B_x,y) (minus # of flagged squares in R_x,y),
	then all of those unrevealed squares contain a bomb.
	
	function: addToFlag(a, b, num)
	input: given coordinate(a, b)
	output: return a list (either empty or a list of UnrevealedSquares)
	'''
	def addToFlag(self, a, b, num):
		numOfUnrevealed = 0
		numOfFlag = 0
		UnrevealedSquares = []
		for i,j in self.getNeighbors(a,b):
			if (i,j) in self.flag:
				numOfFlag += 1
			if (i,j) not in self.explored and (i,j) not in self.flag:
				numOfUnrevealed +=1
				UnrevealedSquares.append((i,j))

		if numOfUnrevealed == (num - numOfFlag):
			return UnrevealedSquares
		else: return []

	'''
	Theorem 2:
	Given a board B and square B_x,y,
	if # of flagged squares surrounding B_x,y == K(B_x,y),
	every unrevealed square in R_x,y does not contain a bomb.
	
	function: addToUncover(a, b, num)
	input: given coordinate(a,b)
	output: return a list (either empty or a list of UnrevealedSquares)
	'''
	def addToUncover(self, a, b, num):
		numOfFlag = 0
		UnrevealedSquares = []
		for i,j in self.getNeighbors(a,b):
			if (i,j) in self.flag:
				numOfFlag += 1
			if (i,j) not in self.explored and (i,j) not in self.flag and (i,j) not in self.frontier:
				UnrevealedSquares.append((i,j))

		if numOfFlag == num:
			return UnrevealedSquares
		else:
			return []

	'''
	function: TotalFlag()
	input: None
	output: return total number of flags)
	'''
	def TotalFlag(self):
		numOfFlag = 0
		for i, j in self.flag:
			numOfFlag += 1
		return numOfFlag

	'''
	function: isCompleted()
	input: None
	output: return true/false
	# If TotalFlag == totalMines, add the rest unrevealed squares to frontier list
	'''
	def isCompleted(self):
		if self.totalMines == self.TotalFlag():
			return True

	'''
	function: getUnknownSquares() (define B_U as the set of all unknown squares)
	input: None
	output: return a list of unknown squares
	'''
	def getUnknownSquares(self):
		L = []
		for a in range(self.rowDimension):
			for b in range(self.colDimension):
				if self.B[a,b] == -1 and (a,b) not in self.flag and (a,b) not in self.frontier:
					L.append((a,b))
		return L

	'''
	function: getPerimeter()
	(define P_B as the set of unknown squares in B that are adjacent to any revealed numbered square)
	input: none
	output: return a list of P_B
	'''
	def getPerimeter(self):
		L = []
		for a, b in self.getUnknownSquares():
			for i,j in self.getNeighbors(a,b):
				if self.B[i,j] != -1 and (a,b) not in L:
					L.append((a,b))
		return L

	'''
	function: getSquaresAdjacentToP()
	input: none
	output: return a list of revealed numbered squares that are adjacent to PB
	'''
	def getSquaresAdjacentToP(self):
		L = []
		for a,b in self.getPerimeter():
			for i,j in self.getNeighbors(a,b):
				if self.B[i,j] != -1 and (i,j) not in L:
					L.append((i,j))
		return L

	# if PB is a neighbor to revealed numbered square, add those PB to a group



