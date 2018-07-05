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
		self.time_last = time.time()
		self.Seen = [0] * self.puzzle.size
		self.must_move_randomly_for = 0

		# Tweak these parameters in order to improve average number of steps
		self.THRESHOLD_STUCK = 3 * self.puzzle.n
		self.RANDOM_MOVE = 2 * self.puzzle.n
		self.MAX_TIME = 10 * self.puzzle.size
		self.MAX_DONT_MOVE = int(0.2 * self.puzzle.n)


	def __repr__(self):
		return str(self.id)

	def print_seen(self):
		toBePrint = ""
		for i in range(len(self.Seen)):
			if(self.Seen[i] != 0):
				toBePrint += " {:>2} ".format(str(self.Seen[i]))
			else:
				toBePrint += " {:>2} ".format('×')
			if((	i+1) % self.n == 0):
				toBePrint += "\n"
		print("Seen", self.id, ":")
		print(toBePrint)

	def run(self):

		#print("Agent " + str(self.id) + " : je suis à la position " + str(self.position) + " et je vais à la position " + str(self.goal))

		while self.puzzle.Start == False: 
			time.sleep(0.001)

		if self.puzzle.to_print:
			print("Mon objectif (agent",self.id, ") est :", self.goal)

		while self.puzzle.Stop == False:

			if abs(time.time() - self.time_start) > self.MAX_TIME:
				#print("It seems that we are in a bad position, let's see : ")
				#print("Nombre de coups :", self.puzzle.nb_coups)
				#print(self.puzzle)
				#self.print_seen()
				self.puzzle.Fail = True
				self.puzzle.Stop = True


			# We don't move until the target changes its position
			ok = True
			if self.dontmove:
				if self.target[0].position == self.target[1] and abs(time.time() - self.time_last) < self.MAX_DONT_MOVE:
					ok = False
				else:
					if abs(time.time() - self.time_last) >= 1:
						self.time_last = time.time()
					self.dontmove = False
					self.taget = (None, -1)

			if ok :

				if self.Seen[self.position] > self.THRESHOLD_STUCK:
					#print("STUCK")

					# The agent is stuck in a position

					M = self.get_random_moove()

					if self.Seen[self.get_value_from_direction(M)] < self.THRESHOLD_STUCK:
						self.Seen[self.position] = 0

					self.must_move_randomly_for = self.RANDOM_MOVE
					self.go(M)

				elif self.must_move_randomly_for > 0:

					# The agent must move randomly to fix the situation

					M = self.get_random_moove()

					self.must_move_randomly_for -= 1
					self.go(M)


				elif self.must_move:

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

						## TODO if position == goal :
						## 			ortogonal with the agent that asked to move

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

						#print("kikou")

						neibo = [self.position - self.n, self.position + self.n,\
						self.position - 1, self.position + 1]

						for elem in neibo :
							if elem < self.puzzle.size and elem >= 0 and self.puzzle.array[elem] != 0:
								try:
									self.puzzle.array[elem].please_move(self) 
								except AttributeError:
									pass


						#raise NotImplemented("An agent is bloqued")


				elif self.position != self.goal:

					# There is no constraint on the agent.

					n = self.puzzle.n

					x = self.position // n
					y = self.position % n 

					x_goal = self.goal // n
					y_goal = self.goal % n

					dico = {}

					if self.position >= self.puzzle.n:
						dico['U'] = abs(x - 1  - x_goal) + abs(y - y_goal)
					else:
						dico['U'] = self.puzzle.size +1

					if self.position < self.puzzle.size - self.puzzle.n:
						dico['D'] = abs(x + 1 - x_goal) + abs(y - y_goal)
					else: 
						dico['D'] = self.puzzle.size +1

					if self.position % self.puzzle.n != 0 and self.position != 0:
						dico['L'] = abs(x - x_goal) + abs(y - 1 - y_goal)
					else: 
						dico['L'] = self.puzzle.size +1

					if (self.position + 1) % self.puzzle.n != 0:
						dico['R'] = abs(x - x_goal) + abs(y + 1 - y_goal)
					else : 
						dico['R'] = self.puzzle.size +1

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
					if self.puzzle.move(self, self.position - self.puzzle.n):
						self.Seen[self.position] += 1
				else:
					# We have to use try in case the agent moved					
					try:
						self.puzzle.array[self.position - self.puzzle.n].please_move(self)
					except AttributeError:
						pass
					

		elif(direction == 'D'): # 'D' for 'DOWN'
			if(self.position < self.puzzle.size - self.puzzle.n):
				if self.puzzle.array[self.position + self.puzzle.n] == 0:
					if self.puzzle.move(self, self.position + self.puzzle.n):
						self.Seen[self.position] += 1
				else:
					# We have to use try in case the agent moved					
					try:
						self.puzzle.array[self.position + self.puzzle.n].please_move(self)
					except AttributeError:
						pass

		elif(direction == 'L'): # 'L' for 'LEFT'
			if(self.position % self.puzzle.n != 0 and self.position >0):
				if self.puzzle.array[self.position - 1] == 0:
					if self.puzzle.move(self, self.position - 1):
						self.Seen[self.position] += 1
				else:
					# We have to use try in case the agent moved
					try:
						self.puzzle.array[self.position - 1].please_move(self)
					except AttributeError:
						pass

		elif(direction == 'R'): # 'R' for 'RIGHT'
			if((self.position + 1) % self.puzzle.n != 0 and self.position+1 <self.puzzle.size):
				if self.puzzle.array[self.position + 1] == 0:
					if self.puzzle.move(self, self.position + 1):
						self.Seen[self.position] += 1
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

	def get_random_moove(self):

		mooves = []


		if self.position >= self.puzzle.n:
			mooves.append('U')

		if self.position < self.puzzle.size - self.puzzle.n:
			mooves.append('D')

		if self.position % self.puzzle.n != 0 and self.position != 0:
			mooves.append('L')

		if (self.position + 1) % self.puzzle.n != 0:
			mooves.append('R')

		m = randint(0, len(mooves) -1)

		return mooves[m]


	def get_direction(self):

		if self.position == self.goal:
			return "OK"

		n = self.puzzle.n

		x = self.position // n
		y = self.position % n 

		x_goal = self.goal // n
		y_goal = self.goal % n

		dico = {}

		if self.position >= self.puzzle.n:
			dico['U'] = abs(x - 1  - x_goal) + abs(y - y_goal)
		else:
			dico['U'] = self.puzzle.size +1

		if self.position < self.puzzle.size - self.puzzle.n:
			dico['D'] = abs(x + 1 - x_goal) + abs(y - y_goal)
		else: 
			dico['D'] = self.puzzle.size +1

		if self.position % self.puzzle.n != 0 and self.position != 0:
			dico['L'] = abs(x - x_goal) + abs(y - 1 - y_goal)
		else: 
			dico['L'] = self.puzzle.size +1

		if (self.position + 1) % self.puzzle.n != 0:
			dico['R'] = abs(x - x_goal) + abs(y + 1 - y_goal)
		else : 
			dico['R'] = self.puzzle.size +1

		# We sort the directions to get the mins
		L = sorted(dico.items(), key=lambda kv: kv[1])

		if L[0][1] != L[1][1]:
			
			# The 2 mins are not equal, we are on the same row or column of the goal.
			# Therefore, there is only one move possible
			return L[0][0]
		elif L[0][1] == L[1][1]:

			# There is two moves possible, we choose uniformly between them. 
			return L[randint(0,1)][0]


	def get_direction_value(self):

		pos = self.position
		DIR = self.get_direction()

		Ret = self.position

		if DIR == 'U':
			Ret = pos - self.n
		elif DIR == 'D':
			Ret = pos + self.n 
		elif DIR == 'L':
			Ret =  pos - 1
		elif DIR == 'R':
			Ret =  pos + 1

		if Ret > self.puzzle.size or Ret < 0:
			Ret = self.position

		return Ret

	def get_value_from_direction(self, DIR):

		pos = self.position

		if DIR == 'U':
			return pos - self.n
		elif DIR == 'D':
			return pos + self.n 
		elif DIR == 'L':
			return pos - 1
		elif DIR == 'R':
			return pos + 1
		else : 
			return pos

	def please_move(self, Gus):

		# If the agent is not on its goal, there's no problem
		# because it wants to move even if it don't catch any ask.
		if self.position == self.goal or self.is_direction_opposed(Gus):
			#if self.position != self.goal:
			#	print("On est dedans", self.id)
			self.must_move = True
			self.dontmove = False
			self.target = (Gus, Gus.position)

		else:
			pos = self.position
			d = self.get_direction_value()

			try : 

				if d >= self.puzzle.size or d < 0:
					print(self.id + ".get_direction_value() = " + d)
					pass

				elif self.puzzle.array[d] != 0 and pos == self.position:

				# Case where there is a inter-block such as : 
				# 1 -> 2
				# 4 <- 3 with 4 -> 1 and 2 -> 3

					self.must_move = True
					self.dontmove = False
					self.target = (Gus, Gus.position)

			except IndexError:
				print("IndexError")
				print(d, ":",self.id)
				print(self.puzzle)
				self.puzzle.Stop = True
