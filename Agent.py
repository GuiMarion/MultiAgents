from threading import Thread
from math import sqrt
import time
from random import *

class Agent(Thread):
	def __init__(self, id, position, goal, puzzle):
		Thread.__init__(self)
		self.id = id
		self.position = position
		self.goal = goal
		self.puzzle = puzzle
		self.must_move = False
		self.n = self.puzzle.n
		self.target = (None, -1)
		self.dontmove = False


	def __repr__(self):
		return str(self.id)

	def get_direction(self):

		n = self.puzzle.n

		x = self.position // n
		y = self.position % n 

		x_goal = self.goal // n
		y_goal = self.goal % n

		dico = {}

		dico['U'] = abs(x - 1  - x_goal) + abs(y - y_goal)
		dico['D'] = abs(x + 1 - x_goal) + abs(y - y_goal)
		dico['L'] = abs(x - x_goal) + abs(y - 1 - y_goal)
		dico['R'] = abs(x - x_goal) + abs(y + 1 - y_goal)

		# We sort the directions to get the mins
		L = sorted(dico.items(), key=lambda kv: kv[1])

		if L[0][1] != L[1][1]:
			
			# The 2 mins are not equal, we are on the same row or column of the goal.
			# Therefore, there is only one move possible
			return L[0][0]
		elif L[0][1] == L[1][1]:

			# There is two moves possible, we choose uniformly between them. 
			return L[randint(0,1)][0]


	def run(self):

		#print("Agent " + str(self.id) + " : je suis à la position " + str(self.position) + " et je vais à la position " + str(self.goal))

		while self.puzzle.Start == False: 
			time.sleep(0.001)

		if self.puzzle.to_print:
			print("Mon objectif (agent",self.id, ") est :", self.goal)

		while self.puzzle.Stop == False:

			# We don't move until the target changes its position
			ok = True
			if self.dontmove:
				if self.target[0].position == self.target[1]:
					ok = False
				else:
					self.dontmove = False

			if ok :

				if self.must_move:

					# It's possible to be better by choosing a moove that minimizes the
					# number of steps

					directions = {}

					directions['U'] = self.position - self.n
					directions['D'] = self.position + self.n
					directions['L'] = self.position - 1
					directions['R'] = self.position + 1

					L = []

					for key in directions :
						if directions[key] >= 0 and directions[key] < self.puzzle.size and self.puzzle.array[directions[key]] == 0:
							L.append(key)

					# If there is a least one free move we choose one uniformly
					if len(L) > 0:
						d = randint(0, len(L)-1)

						self.dontmove = True
						self.must_move = False

						self.go(L[d])

					else:
						raise NotImplemented("An agent is bloqued")


				elif self.position != self.goal:

					n = self.puzzle.n

					x = self.position // n
					y = self.position % n 

					x_goal = self.goal // n
					y_goal = self.goal % n

					dico = {}

					dico['U'] = abs(x - 1  - x_goal) + abs(y - y_goal)
					dico['D'] = abs(x + 1 - x_goal) + abs(y - y_goal)
					dico['L'] = abs(x - x_goal) + abs(y - 1 - y_goal)
					dico['R'] = abs(x - x_goal) + abs(y + 1 - y_goal)

					# We sort the directions to get the mins
					L = sorted(dico.items(), key=lambda kv: kv[1])

					if L[0][1] != L[1][1]:
						
						# The 2 mins are not equal, we are on the same row or column of the goal.
						# Therefore, there is only one move possible
						self.go(L[0][0])
					elif L[0][1] == L[1][1]:

						# There is two move possible, we choose uniformly between them. 
						self.go(L[randint(0,1)][0])
					else:
						raise ValueError("Should never append.")



				#else:



	def go(self, direction):

		if self.puzzle.to_print:
			print("Agent", self.id,", j'aimerais bien me déplacer en :", direction)

		if(direction == 'U'): # 'U' for 'UP'
			if(self.position >= self.puzzle.n):
				if self.puzzle.array[self.position - self.puzzle.n] == 0:
					self.puzzle.move(self, self.position - self.puzzle.n)
				else:
					# We have to use try in case the agent moved					
					try:
						self.puzzle.array[self.position - self.puzzle.n].please_move(self)
					except AttributeError:
						pass
					

		elif(direction == 'D'): # 'D' for 'DOWN'
			if(self.position < self.puzzle.size - self.puzzle.n):
				if self.puzzle.array[self.position + self.puzzle.n] == 0:
					self.puzzle.move(self, self.position + self.puzzle.n)
				else:
					# We have to use try in case the agent moved					
					try:
						self.puzzle.array[self.position + self.puzzle.n].please_move(self)
					except AttributeError:
						pass

		elif(direction == 'L'): # 'L' for 'LEFT'
			if(self.position % self.puzzle.n != 0 and self.position >0):
				if self.puzzle.array[self.position - 1] == 0:
					self.puzzle.move(self, self.position - 1)
				else:
					# We have to use try in case the agent moved
					try:
						self.puzzle.array[self.position - 1].please_move(self)
					except AttributeError:
						pass

		elif(direction == 'R'): # 'R' for 'RIGHT'
			if((self.position + 1) % self.puzzle.n != 0 and self.position+1 <self.puzzle.size):
				if self.puzzle.array[self.position + 1] == 0:
					self.puzzle.move(self, self.position + 1)
				else:
					# We have to use try in case the agent moved
					try :
						self.puzzle.array[self.position + 1].please_move(self)
					except AttributeError:
						pass

	def is_direction_opposed(self, Gus):

		Me = self.get_direction()
		He = Gus.get_direction()

		if Me == 'D' and He == 'U':
			return True

		elif Me == 'U' and He == 'D':
			return True

		elif Me == 'L' and He == 'R':
			return True

		elif Me == 'R' and He == 'L':
			return True

		else: 
			return False

	def please_move(self, Gus):

		# If the agent is not on its goal, there's no problem
		# because it wants to move even if it don't catch any ask.
		if self.position == self.goal or self.is_direction_opposed(Gus):
			self.must_move = True
			self.dontmove = False
			self.target = (Gus, Gus.position)












