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

UNKNOWN = "."
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
		self.x, self.y = startX, startY
		self.array[self.x, self.y] = 0
		self.frontier = []
		self.ep = []
		self.frontier = self.addNeighbors(startX, startY) #save all 8 neighbors to q
		# self.explored = [(startX, startY)]

		# self.ep = self.addToExplored(startX, startY)

		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################


		'''
		display my own world: array
		'''
		self.array[self.x, self.y] = number
		_print(self.array)

		'''
		add it to explored after uncover it
		'''
		for i,j in self.addToExplored(self.x, self.y):
			self.ep.append((i,j))
		print("explored: ",self.ep)

		'''
		when uncover any place with number 0, 
		get all its possible neighbors and add them to frontier
		'''
		if number == 0:
			for i,j in self.addNeighbors(self.x, self.y):
				self.frontier.append((i,j))
		print("frontier:", self.frontier)


		'''
		if frontier is not empty, pop it to uncover
		for now, i can pop all neighbors adjacent to (startX,startY)
		'''
		if self.frontier:

			self.x, self.y = self.frontier.pop()
			print("NEXT CORD TO UNCOVER: (", self.x, ",", self.y, ")")
			print("ALL OTHER POSSIBLE CORDS:", self.frontier)
			return Action(AI.Action.UNCOVER, self.x, self.y)

		"""
		just testing, this move is to uncover all cord listed in the list called move
		"""
		# if self.move:
		# 	self.x, self.y = self.move.pop()
		# 	print("NEXT CORD TO UNCOVER: (",self.x, ",", self.y, ")")
		# 	return Action(AI.Action.UNCOVER, self.x, self.y)

		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################
	'''
	given (a,b), get its all adjacent neighbors, 8 possible neighbors
	'''
	def getNeighbors(self, a, b):
		possibleN = [(a-1, b-1),(a-1, b),(a-1, b+1),\
		       (a, b-1), (a, b+1), (a+1, b-1), (a+1, b), (a+1, b+1)]

		return [(i,j) for i,j in possibleN if (i >=0 and i < self.colDimension and j >= 0 and j < self.rowDimension)]

	'''
	given (a,b), add its all neighbors to a list
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
			# if (i,j) not in self.frontier and (i,j) != (self.startX, self.startY):
			if (i,j) not in self.frontier and (i,j) not in self.ep:
				L.append((i,j))
		return L



	def addToExplored(self, a, b):

		L = []
		if (a,b) not in self.ep:
			L.append((a,b))
		return L
