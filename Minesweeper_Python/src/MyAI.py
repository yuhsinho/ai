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

		self.rowDimension = rowDimension
		self.colDimension = colDimension
		self.startX, self.startY = startX, startY
		self.totalMines = totalMines
		self.B = np.array([[UNKNOWN for _ in range(rowDimension)] for _ in range(colDimension)])
		self.x, self.y = startX, startY
		self.B[self.x, self.y] = 0
		self.frontier = set()
		self.explored = set()
		self.flag = []
		MyAI.add_list_elements_to_set(self.frontier, self.get_new_neighbors(startX, startY))

	@staticmethod
	def add_list_elements_to_set(set, the_list):
		for elm in the_list:
			set.add(elm)
	########################################################################
	def getAction(self, number: int) -> "Action Object":

		self.B[self.x, self.y] = number

		if self.not_explored_yet(self.x, self.y):
			self.explored.add((self.x, self.y))

		if number == 0:
			for i,j in self.get_new_neighbors(self.x, self.y):
				self.frontier.add((i,j))

		while True:
			applied_theorem = False
			for i,j in self.explored:
					applied_theorem |= self.apply_theorems(i,j)
			if not applied_theorem:
				break

		if self.frontier:
			self.x, self.y = self.frontier.pop()
			return Action(AI.Action.UNCOVER, self.x, self.y)

		self.apply_equation_strategy()

		if self.is_completed():
			for i, j in self.get_all_unknown_squares():
				self.frontier.add((i, j))

		if self.frontier:
			self.x, self.y = self.frontier.pop()
			return Action(AI.Action.UNCOVER, self.x, self.y)

		unknown_squares = self.get_all_unknown_squares()
		if unknown_squares:
			self.x, self.y = random.choice(self.get_all_unknown_squares())
			return Action(AI.Action.UNCOVER, self.x, self.y)

		return Action(AI.Action.LEAVE)
		########################################################################

	def get_neighbors(self, a, b):
		neighbors = [(a-1, b-1),(a-1, b),(a-1, b+1),\
		       (a, b-1), (a, b+1), (a+1, b-1), (a+1, b), (a+1, b+1)]
		return [(i,j) for i,j in neighbors if (i >=0 and i < self.colDimension and j >= 0 and j < self.rowDimension)]

	def get_new_neighbors(self, a, b):
		L = []
		for i,j in self.get_neighbors(a, b):
			if (i,j) not in self.frontier and (i,j) not in self.explored:
				L.append((i,j))
		return L

	def not_explored_yet(self, a, b):
		if (a,b) not in self.explored:
			return True

	def get_num_of_flag(self, a, b):
		num = 0
		for i,j in self.get_neighbors(a,b):
			if (i,j) in self.flag:
				num += 1
		return num

	def get_num_of_unrevearled(self, a, b):
		num = 0
		for i,j in self.get_neighbors(a,b):
			if (i,j) not in self.explored and (i,j) not in self.flag:
				num += 1
		return num

	def get_unrevealed(self, a,b ):
		L = []
		for i,j in self.get_neighbors(a,b):
			if (i,j) not in self.explored and (i,j) not in self.flag:
				L.append((i,j))
		return L

	def theroem1(self, a, b, value):
		num_of_unrevealed = self.get_num_of_unrevearled(a,b)
		num_of_flag = self.get_num_of_flag(a,b)
		unrevealed_squares = []
		if num_of_unrevealed == (value - num_of_flag):
			for i,j in self.get_unrevealed(a,b):
				unrevealed_squares.append((i,j))
		return unrevealed_squares

	def theorem2(self, a, b, value):
		num_of_flag = self.get_num_of_flag(a,b)
		unrevealed_squares = []
		if num_of_flag == value:
			for i,j in self.get_unrevealed(a,b):
				if (i,j) not in self.frontier:
					unrevealed_squares.append((i,j))
		return unrevealed_squares

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
			self.frontier.add((i,j))
		return applied_theorem1 or applied_theorem2

	def total_flag(self):
		num = 0
		for i, j in self.flag:
			num += 1
		return num

	def is_completed(self):
		if self.totalMines == self.total_flag():
			return True

	def get_all_unknown_squares(self):
		L = []
		for a in range(self.colDimension):
			for b in range(self.rowDimension):
				if self.B[a, b] == -1 and (a, b) not in self.flag and (a, b) not in self.frontier:
					L.append((a,b))
		return L

	def get_perimeter(self):
		L = []
		for a, b in self.get_all_unknown_squares():
			for i,j in self.get_neighbors(a,b):
				if self.B[i, j] != -1 and (a, b) not in L and (i, j) not in self.flag:
					L.append((a,b))
		return L

	def get_revealed_adjacent_to_p(self):
		L = []
		for a, b in self.get_perimeter():
			for i, j in self.get_neighbors(a,b):
				if self.B[i, j] != -1 and (i, j) not in L and (i, j) not in self.flag:
					L.append((i,j))
		return L

	def get_constraint_variables(self, a, b):
		L = []
		for i, j in self.get_perimeter():
			if (i,j) in self.get_neighbors(a,b):
				L.append((i,j))
		return L

	def get_constraint(self, a, b):
		num_of_flag = self.get_num_of_flag(a,b)
		sum = self.B[a,b] - num_of_flag
		L = []
		L.append([self.get_constraint_variables(a,b),sum])
		return L

	def get_all_constraints(self):
		L = []
		for i, j in self.get_revealed_adjacent_to_p():
			for c in self.get_constraint(i, j):
				L.append(c)
		return L

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
					self.equation_difference(csp)
		return csp

	def find_update_tiles(self, csp):
		update_list = []
		for i in range(len(csp)):
			if len(csp[i][0]) == 1:
				update_list.append(csp[i])
			# if csp[i][1] == 0:
			# 	update_list.append(csp[i])
		return update_list

	def apply_equation_strategy(self):
		all_cons = self.get_all_constraints()
		self.equation_difference(all_cons)
		for cons in self.find_update_tiles(all_cons):
			if cons[1] == 0:
				for a, b in cons[0]:
					if (a,b) not in self.frontier:
						self.frontier.add((a,b))
			if cons[1] == 1:
				for a, b in cons[0]:
					if (a,b) not in self.flag:
						self.flag.append((a,b))


