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
		self.frontier = self.get_new_neighbors(startX, startY)

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
		# _print(self.B)

		# Check if B_x,y is explored. If not, add B_x,y to explored list
		if self.not_explored_yet(self.x, self.y):
			self.explored.append((self.x, self.y))

		# if K(B_x,y) == 0, add R_x,y to frontier list
		if number == 0:
			for i,j in self.get_new_neighbors(self.x, self.y):
				self.frontier.append((i,j))

		# apply theorems 1 and 2
		while True:
			applied_theorem = False
			for i,j in self.explored:
					applied_theorem |= self.apply_theorems(i,j)
			if not applied_theorem:
				break

		if self.frontier:
			self.x, self.y = self.frontier.pop()
			return Action(AI.Action.UNCOVER, self.x, self.y)

		# Equation Strategy
		self.apply_equation_strategy()

		# pick one for fifty
		# if self.colDimension != 8 and self.rowDimension != 8:
		# 	guess = self.guess()
		# 	if guess:
		# 		self.x, self.y = guess
		# 		return Action(AI.Action.UNCOVER, self.x, self.y)

		# If current_total_flag == total_mines, add the rest unrevealed squares to frontier list
		if self.is_completed():
			for i, j in self.get_all_unknown_squares():
				self.frontier.append((i, j))

		if self.frontier:
			self.x, self.y = self.frontier.pop()
			return Action(AI.Action.UNCOVER, self.x, self.y)

		# Random choice
		unknown_squares = self.get_all_unknown_squares()
		if unknown_squares:
			self.x, self.y = random.choice(self.get_all_unknown_squares())
			return Action(AI.Action.UNCOVER, self.x, self.y)

		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################
	'''
	function: get_neighbors(a, b)
	input: given coordinate(a,b)
	output: return a list of (a,b)'s all adjacent neighbors
	'''
	def get_neighbors(self, a, b):
		neighbors = [(a-1, b-1),(a-1, b),(a-1, b+1),\
		       (a, b-1), (a, b+1), (a+1, b-1), (a+1, b), (a+1, b+1)]
		return [(i,j) for i,j in neighbors if (i >=0 and i < self.colDimension and j >= 0 and j < self.rowDimension)]

	'''
	function: get_new_neighbors(a, b)
	input: given coordinate(a,b)
	output: return a list of (a,b)'s adjacent neighbors (filter: not in frontier list and not in explored list)
	'''
	def get_new_neighbors(self, a, b):
		L = []
		for i,j in self.get_neighbors(a, b):
			if (i,j) not in self.frontier and (i,j) not in self.explored:
				L.append((i,j))
		return L

	'''
	function: not_explored_yet(a, b)	
	input: given coordinate(a,b)
	output: return True if not explored yet 
	'''
	def not_explored_yet(self, a, b):
		if (a,b) not in self.explored:
			return True

	'''
	function: get_num_of_flag(a,b)
	input: given a cord(a,b)
	output: a number of flag in the flag list
	'''

	def get_num_of_flag(self, a, b):
		num = 0
		for i,j in self.get_neighbors(a,b):
			if (i,j) in self.flag:
				num += 1
		return num

	'''
	function: get_num_of_unrevealed(a,b)
	input: given a cord(a,b)
	output: a number of unrevealed squares
	'''
	def get_num_of_unrevearled(self, a, b):
		num = 0
		for i,j in self.get_neighbors(a,b):
			if (i,j) not in self.explored and (i,j) not in self.flag:
				num += 1
		return num

	'''
	function: get_unrevealed(a,b)
	input: given a cord(a,b)
	output: a list of unrevealed squares
	'''
	def get_unrevealed(self, a,b ):
		L = []
		for i,j in self.get_neighbors(a,b):
			if (i,j) not in self.explored and (i,j) not in self.flag:
				L.append((i,j))
		return L
	'''
	Theorem 1: 
	Given a board B and square B_x,y, 
	if # of unrevealed squares in R_x,y == K(B_x,y) (minus # of flagged squares in R_x,y),
	then all of those unrevealed squares contain a bomb.
	
	function: theorem1(a, b, value)
	input: given coordinate(a, b)
	output: return a list of unrevealed squares (ready to be flagged)
	'''
	def theroem1(self, a, b, value):
		num_of_unrevealed = self.get_num_of_unrevearled(a,b)
		num_of_flag = self.get_num_of_flag(a,b)
		unrevealed_squares = []
		if num_of_unrevealed == (value - num_of_flag):
			for i,j in self.get_unrevealed(a,b):
				unrevealed_squares.append((i,j))
		return unrevealed_squares

	'''
	Theorem 2:
	Given a board B and square B_x,y,
	if # of flagged squares surrounding B_x,y == K(B_x,y),
	every unrevealed square in R_x,y does not contain a bomb.
	
	function: theorem2(a, b, value)
	input: given coordinate(a,b)
	output: return a list of unrevealed squares (ready to uncover, so filter those who are already in frontier list)
	'''
	def theorem2(self, a, b, value):
		num_of_flag = self.get_num_of_flag(a,b)
		unrevealed_squares = []
		if num_of_flag == value:
			for i,j in self.get_unrevealed(a,b):
				if (i,j) not in self.frontier:
					unrevealed_squares.append((i,j))
		return unrevealed_squares

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
		list_of_bomb_cords = self.theroem1(a,b,x)
		applied_theorem1 = bool(list_of_bomb_cords)
		for i,j in list_of_bomb_cords:
			self.flag.append((i,j))
		#theorem 2
		list_of_safe_unrevealed_cords = self.theorem2(a,b,x)
		applied_theorem2 = bool(list_of_safe_unrevealed_cords)
		for i,j in list_of_safe_unrevealed_cords:
			self.frontier.append((i,j))
		return applied_theorem1 or applied_theorem2

	'''
	function: total_flag()
	input: None
	output: return total number of flags in board B
	'''
	def total_flag(self):
		num = 0
		for i, j in self.flag:
			num += 1
		return num

	'''
	function: is_completed()
	input: None
	output: return true or false
	# If TotalFlag == totalMines, add the rest unrevealed squares to frontier list
	'''
	def is_completed(self):
		if self.totalMines == self.total_flag():
			return True

	'''
	function: get_all_unknown_squares() (define B_U as the set of all unknown squares)
	input: None
	output: return a list of all unknown squares in board B
	'''
	def get_all_unknown_squares(self):
		L = []
		for a in range(self.colDimension):
			for b in range(self.rowDimension):
				if self.B[a, b] == -1 and (a, b) not in self.flag and (a, b) not in self.frontier:
					L.append((a,b))
		return L

	'''
	function: get_perimeter()
	(define PB as the set of unknown squares in B that are adjacent to any revealed numbered square)
	input: none
	output: return a list of PB
	'''
	def get_perimeter(self):
		L = []
		for a, b in self.get_all_unknown_squares():
			for i,j in self.get_neighbors(a,b):
				if self.B[i, j] != -1 and (a, b) not in L and (i, j) not in self.flag:
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
			for i, j in self.get_neighbors(a,b):
				if self.B[i, j] != -1 and (i, j) not in L and (i, j) not in self.flag:
					L.append((i,j))
		return L

	'''
	function: get_constraint_variables(a,b)
	input: given a cord(a,b), named vi: a revealed square adjacent to PB 
	output: return a list of perimeters adjacent to vi, vi = [ p1, p2,..]
	'''
	def get_constraint_variables(self, a, b):
		L = []
		for i, j in self.get_perimeter():
			if (i,j) in self.get_neighbors(a,b):
				L.append((i,j))
		return L

	'''
	function: get_constraint(a,b)
	input: given a cord(a,b), named vi: a revealed square adjacent to p
	output: return a list of constraint, named ci = [ [vi], sumi ]	
	'''
	def get_constraint(self, a, b):
		num_of_flag = self.get_num_of_flag(a,b)
		sum = self.B[a,b] - num_of_flag
		L = []
		L.append([self.get_constraint_variables(a,b),sum])
		return L

	'''
	function: get_all_contraints()
	input: none
	output: a list of constraints c = [c1,c2,..] = [ [ [v1], sum1 ], [ [v2], sum2 ], ...] 
	'''
	def get_all_constraints(self):
		L = []
		for i, j in self.get_revealed_adjacent_to_p():
			for c in self.get_constraint(i, j):
				L.append(c)
		return L

	'''
	function: _print_csp(csp) (for testing purpose)
	input: a list of constraints c = [ [ [v1], sum1 ], [ [v2], sum2 ], ...] 
	output: simple format to check the list
	'''
	def _print_csp(self, csp):
		for i in range(len(csp)):
			print(csp[i][0], csp[i][1])

	'''
	function: is_assignment_complete(csp)
	input: a list of constraints c
	output: return True (if each ci has a single value)
	'''
	def is_assignment_complete(self, csp):
		return all(len(csp[i][0]) == 1 for i in range(len(csp)))


	'''
	function: equation_difference(csp)
	input: a list of constraints c = [ [ [v1], sum1 ], [ [v2], sum2 ], ...] 
	output: a list of updated constraints
	'''
	def equation_difference(self, csp):
		# if self.is_assignment_complete(csp):
		# 	return csp
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
				update_list.append(csp[i])
				if self.rowDimension == 8 and self.colDimension == 8:
					if csp[i][1] == 0:
						update_list.append(csp[i])
		return update_list

	'''
	function: apply_equation_strategy()
	input:
	output:
	'''
	def apply_equation_strategy(self):
		all_cons = self.get_all_constraints()
		self.equation_difference(all_cons)
		for cons in self.find_update_tiles(all_cons):
			if cons[1] == 0:
				for a, b in cons[0]:
					if (a,b) not in self.frontier:
						self.frontier.append((a,b))
			if cons[1] == 1:
				for a, b in cons[0]:
					if (a,b) not in self.flag:
						self.flag.append((a,b))

	# def find_fifty(self, csp):
	# 	L = []
	# 	for i in range(len(csp)):
	# 		if len(csp[i][0]) == 2 and csp[i][1] == 1 and csp[i] not in L:
	# 			L.append(csp[i])
	# 	return L
	#
	# def pickone(self, csp):
	# 	guess_to_uncover = random.choice(csp[0][0])
	# 	for i in csp[0][0]:
	# 		if i != guess_to_uncover:
	# 			guess_bomb = i
	# 	if guess_bomb not in self.flag:
	# 		self.flag.append(guess_bomb)
	#
	# 	return guess_to_uncover
	# def guess(self):
	# 	all_cons = self.get_all_constraints()
	# 	self.equation_difference(all_cons)
	# 	cons = self.find_fifty(all_cons)
	# 	if cons:
	# 		guess = self.pickone(cons)
	# 		return guess
	# 	else: return

