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
import random

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
		self.B = np.array([[UNKNOWN for _ in range(rowDimension)] for _ in range(colDimension)])

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
		print("Explored list: ", self.explored)

		# if K(B_x,y) == 0, add R_x,y to frontier list
		if number == 0:
			for i,j in self.addNeighbors(self.x, self.y):
				self.frontier.append((i,j))

		# apply theorems 1 and 2
		while True:
			applied_theorem = False
			# for i in range(self.colDimension):
			# 	for j in range(self.rowDimension):
			for i,j in self.explored:
					applied_theorem |= self.apply_theorems(i,j)
			if not applied_theorem:
				break


		if self.frontier:
			self.x, self.y = self.frontier.pop()
			print("FLAG LIST: ", self.flag)
			print("NEXT CORD TO UNCOVER: (", self.x, ",", self.y, ")")
			print("POP (", self.x, ",", self.y, ")")
			print("ALL OTHER POSSIBLE TILES IN FRONTIER:", self.frontier)
			return Action(AI.Action.UNCOVER, self.x, self.y)

		# CSP or Equation Strategy
		all_cons = self.all_constraints()
		self.equation_difference(all_cons)
		safe = []
		bomb = []
		for cons in self.find_update_tiles(all_cons):
			if cons[1] == 0:
				for a, b in cons[0]:
					safe.append((a, b))
			if cons[1] == 1:
				for a,b in cons[0]:
					bomb.append((a,b))
		for i,j in safe:
			self.frontier.append((i,j))
		for i,j in bomb:
			self.flag.append((i,j))

		# If current_total_flag == total_mines, add the rest unrevealed squares to frontier list
		if self.isCompleted():
			for i, j in self.getUnknownSquares():
				self.frontier.append((i, j))

		if self.frontier:
			self.x, self.y = self.frontier.pop()
			print("FLAG LIST: ", self.flag)
			print("NEXT CORD TO UNCOVER: (", self.x, ",", self.y, ")")
			print("POP (", self.x, ",", self.y, ")")
			print("ALL OTHER POSSIBLE TILES IN FRONTIER:", self.frontier)
			return Action(AI.Action.UNCOVER, self.x, self.y)

		# Random choice
		unknown_squares = self.getUnknownSquares()
		if unknown_squares:
			self.x, self.y = random.choice(self.getUnknownSquares())
			return Action(AI.Action.UNCOVER, self.x, self.y)

		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################
	'''
	function: apply_theorems(a,b)
	input: given coordinate(a,b)
	output: return True or False
	'''
	def apply_theorems(self, a, b):
		x = self.B[a,b]
		if x == -1:
			return False
		#theorem 1
		list_of_bomb_cords = self.addToFlag(a,b,x)
		applied_theorem1 = bool(list_of_bomb_cords)
		for i,j in list_of_bomb_cords:
			self.flag.append((i,j))
		#theorem 2
		list_of_safe_unrevealed_cords = self.addToUncover(a,b,x)
		applied_theorem2 = bool(list_of_safe_unrevealed_cords)
		for i,j in list_of_safe_unrevealed_cords:
			self.frontier.append((i,j))
		return applied_theorem1 or applied_theorem2

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
		# else: return False

	'''
	function: getUnknownSquares() (define B_U as the set of all unknown squares)
	input: None
	output: return a list of unknown squares
	'''
	def getUnknownSquares(self):
		L = []
		for a in range(self.colDimension):
			for b in range(self.rowDimension):
				if self.B[a,b] == -1 and (a,b) not in self.flag and (a,b) not in self.frontier:
					L.append((a,b))
		return L

	'''
	function: get_perimeter()
	(define P_B as the set of unknown squares in B that are adjacent to any revealed numbered square)
	input: none
	output: return a list of P_B
	'''
	def get_perimeter(self):
		L = []
		for a, b in self.getUnknownSquares():
			for i,j in self.getNeighbors(a,b):
				# revealed numbered square: explored, not in flag list?!
				if self.B[i,j] != -1 and (a,b) not in L and (i,j) not in self.flag:
					L.append((a,b))
		return L

	'''
	function: get_revealed_adjacent_to_p()
	input: none
	output: return a list of revealed numbered squares that are adjacent to PB
	'''
	def get_revealed_adjacent_to_p(self):
		L = []
		for a, b in self.get_perimeter():
			for i, j in self.getNeighbors(a,b):
				# revealed numbered square: explored, not in flag list
				if self.B[i,j] != -1 and (i,j) not in L and (i,j) not in self.flag:
					L.append((i,j))
		return L

	'''
	function: get_constraint_variables()
	input: given a cord(a,b) (a revealed square adjacent to p)
	output: return a list of constraint variables(perimeters) vi = [ p1, p2,..]
	'''
	def get_constraint_variables(self, a, b):
		perimeter_list = self.get_perimeter()
		L = []
		for i, j in perimeter_list:
			if (i,j) in self.getNeighbors(a,b):
				L.append((i,j))
		return L

	'''
	function: get_constraints()
	input: given a cord(a,b) ( a revealed square adjacent to p)
	output: return a list of constraints ci = [ [v], sum ]
	after go through each (a,b), it will be c = [ [ [v1], sum1 ], [ [v2], sum2 ], ...] 
	'''
	def get_constraints(self, a, b):
		bomb = 0
		for i,j in self.getNeighbors(a,b):
			if (i,j) in self.flag:
				bomb += 1
		sum = self.B[a,b] - bomb
		L = []
		L.append([self.get_constraint_variables(a,b),sum])
		return L

	'''
		function: all_contraints()
		input: none
		output: a list of contraints c = [ [ [v1], sum1 ], [ [v2], sum2 ], ...] 
		'''

	def all_constraints(self):
		cons = []
		for i, j in self.get_revealed_adjacent_to_p():
			for c in self.get_constraints(i, j):
				cons.append(c)
		return cons

	'''
	function: _print_csp(csp)
	input: a list of constraints c = [ [ [v1], sum1 ], [ [v2], sum2 ], ...] 
	output: simple format to check the list
	'''
	def _print_csp(self, csp):
		for i in range(len(csp)):
			print(csp[i][0], csp[i][1])

	'''
	function: equation_difference(csp)
	input: a list of contraints c = [ [ [v1], sum1 ], [ [v2], sum2 ], ...] 
	output: a list of updated constraints
	'''
	def equation_difference(self, csp):
		for i in range(len(csp) - 1):
			con0 = csp[i]
			for j in range(i + 1, len(csp)):
				con1 = csp[j]
				if set(con0[0]) == set(con1[0]):
					continue
				if (set(con0[0]) & set(con1[0]) == set(con0[0])) or (set(con0[0]) & set(con1[0]) == set(con1[0])):
					if len(con0[0]) > len(con1[0]):
						con0[0] = list(set(con0[0]).difference(set(con1[0])))
						con0[1] = con0[1] - con1[1]
					elif len(con1[0]) > len(con0[0]):
						con1[0] = list(set(con1[0]).difference(set(con0[0])))
						con1[1] = con1[1] - con0[1]
					# when we are in this if statement, that means ci is updated
					# once ci is updated, repeat the function again
					self.equation_difference(csp)
		return csp

	'''
	function: find_updated_squares(csp)
	input: a list of contraints c = [ [ [v1], sum1 ], [ [v2], sum2 ], ...] (after equation_difference(csp))
	output: a list of updated square ci = [ [ [p1], 0 ], [ [p2], 1], .. ]
	'''
	def find_update_tiles(self, csp):
		update_list = []
		for i in range(len(csp)):
			if len(csp[i][0]) == 1:
				# [ [p1], 0 ]
				update_list.append(csp[i])

			# not sure if necessary
			elif csp[i][1] == 0:
				# [ [p1,p2,p3], 0]
				update_list.append(csp[i])

		return update_list

	def get_unknown_without_p(self):
		L = []
		for i,j in self.getUnknownSquares():
			if (i,j) not in self.get_perimeter():
				L.append((i,j))
		return L


	# def update_c(self,csp):
	# 	L = []
	# 	for i in self.find_update_tiles(csp):
	# 		for a,b in i[0]:
	# 			L.append((a,b))
	# 	return L

	# def guess_corner(self):
	# 	L = []
	# 	corner = [(0,0), (0,self.colDimension-1), (self.rowDimension-1,0),(self.rowDimension-1, self.colDimension-1)]
	# 	for i,j in corner:
	# 		if (i,j) not in self.flag and (i,j) not in self.explored:
	# 			L.append((i,j))
	# 	return L
