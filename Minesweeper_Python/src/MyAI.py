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
		# self.startX = startX
		# self.startY = startY

		self.rowDimension = rowDimension
		self.colDimension = colDimension
		self.array = np.array([[UNKNOWN for _ in range(colDimension)] for _ in range(rowDimension)])
		# self.array[startX, startY] = 0
		# self.move = [(3,3), (2,2), (1,1)]
		self.x = startX
		self.y = startY
		self.startX = startX
		self.startY = startY
		self.array[self.x,self.y] = 0
		self.q = []
		self.q = self.addNeighbors(startX, startY)

		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self.array[self.x, self.y] = number
		_print(self.array)

		# print("(",self.x,",",self.y, ") neighbors: ",self.getNeighbors(self.x, self.y))
		# print(self.addNeighbors(self.x, self.y))
		"""
		if uncover any 0
		then get its all possible neighbors
		add to queue
		"""

		# if number == 0:
			# print(self.x, self.y)
			# if (self.x, self.y) == (self.startX, self.startY):

			# self.q = self.addNeighbors(self.x, self.y)
			# self.addNeighbors(self.x, self.y)
			# print(self.q)


		'''
		for now, this q is to uncover all neighbors around start cord 0
		'''
		if self.q:

			self.x, self.y = self.q.pop()
			print("NEXT CORD TO UNCOVER: (", self.x, ",", self.y, ")")
			print("ALL OTHER POSSIBLE CORDS:", self.q)
			return Action(AI.Action.UNCOVER, self.x, self.y)

		"""
		for testing purpose, this move is to uncover all cord listed in list move
		"""
		# if self.move:
		# 	self.x, self.y = self.move.pop()
		# 	print("NEXT CORD TO UNCOVER: (",self.x, ",", self.y, ")")
		# 	return Action(AI.Action.UNCOVER, self.x, self.y)



		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################
	def getNeighbors(self, a, b):
		possibleN = [(a-1, b-1),(a-1, b),(a-1, b+1),\
		       (a, b-1), (a, b+1), (a+1, b-1), (a+1, b), (a+1, b+1)]

		return [(i,j) for i,j in possibleN if (i >=0 and i < self.colDimension and j >= 0 and j < self.rowDimension)]


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

		for i,j in self.getNeighbors(a, b):
			if (i,j) not in self.q:
				self.q.append((i,j))
		return self.q
