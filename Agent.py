from threading import Thread
from math import sqrt
import time
from random import *
import os

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
		self.time_start = time.time()


	def __repr__(self):
		return str(self.id)

	def get_direction(self):

		if self.position == self.goal:
			return "OK"

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

			if abs(time.time() - self.time_start) > 10:
				print("It seems that we are in a bad position, let's see : ")
				print(self.puzzle)
				os._exit(1)

			# We don't move until the target changes its position
			ok = True
			if self.dontmove:
				if self.target[0].position == self.target[1] and abs(time.time() - self.time_start) < 1:
					ok = False
				else:
					self.dontmove = False
					self.taget = (None, -1)

			if ok :

				if self.must_move:

					directions = {}

					directions['U'] = self.position - self.n
					directions['D'] = self.position + self.n

					if (self.position) % 5 != 0:
						directions['L'] = self.position - 1
					else:
						directions['L'] = -1

					if (self.position + 1) % 5 != 0:
						directions['R'] = self.position + 1
					else:
						directions['R'] = -1	

					L = []

					for key in directions :
						if directions[key] >= 0 and directions[key] < self.puzzle.size and self.puzzle.array[directions[key]] == 0:
							L.append(key)

					# If there is a least one free move we choose one uniformly
					if len(L) > 0:

						moves = []

						# We prefer to choose the orthogonal ones
						for move in L :
							if self.is_orthogonal(move):
								moves.append(move)

						if len(moves) >  0:
							L = moves

						d = randint(0, len(L)-1)

						self.dontmove = True
						self.must_move = False

						self.go(L[d])

					else:

						# The agent must move but it's blocked by others

						# TODO
						# We can maybe choose a better moove that minimises number of steps

						print("kikou")

						neibo = [self.position - self.n, self.position + self.n,\
						self.position - 1, self.position + 1]

						for elem in neibo :
							if elem < self.puzzle.size and elem >= 0 and self.puzzle.array[elem] != 0:
								self.puzzle.array[elem].please_move(self) 


						#raise NotImplemented("An agent is bloqued")


				elif self.position != self.goal:

					# There is no constraint on the agent.

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

	def is_orthogonal(self, move):

		Me = self.get_direction()

		if Me == 'D' and move == 'U':
			return False

		elif Me == 'U' and move == 'D':
			return False

		elif Me == 'L' and move == 'R':
			return False

		elif Me == 'R' and move == 'L':
			return False

		else: 
			return True

	def please_move(self, Gus):

		# If the agent is not on its goal, there's no problem
		# because it wants to move even if it don't catch any ask.
		if self.position == self.goal or self.is_direction_opposed(Gus):
			#if self.position != self.goal:
		#		print("On est dedans", self.id)
			self.must_move = True
			self.dontmove = False
			self.target = (Gus, Gus.position)












