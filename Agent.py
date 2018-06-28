from threading import Thread
from math import sqrt

class Agent(Thread):
	def __init__(self, id, position, goal, puzzle):
		Thread.__init__(self)
		self.id = id
		self.position = position
		self.goal = goal
		self.puzzle = puzzle


	def __repr__(self):
		return str(self.id)

	def run(self):
		#print("Agent " + str(self.id) + " : je suis à la position " + str(self.position) + " et je vais à la position " + str(self.goal))
		
		print("Mon objectif est :", self.goal)
		# while self.position != self.goal:

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

		min = 2*self.puzzle.n
		minkey = None

		for key in dico :
			if dico[key] < min: 
				min = dico[key]
				minkey = key
		print(dico)

		self.go(minkey)


	def go(self, direction):

		print("Kikou, j'aimerais bien me déplacer en :", direction)

		if(direction == 'U'): # 'U' for 'UP'
			if(self.position >= self.puzzle.n):
				if self.puzzle.array[self.position - self.puzzle.n] == 0:
					self.puzzle.move(self, self.position - self.puzzle.n)
				else:
					raise NotImplemented("Communication between agents")

		elif(direction == 'D'): # 'D' for 'DOWN'
			if(self.position < self.puzzle.size - self.puzzle.n):
				if self.puzzle.array[self.position + self.puzzle.n] == 0:
					self.puzzle.move(self, self.position + self.puzzle.n)
				else:
					raise NotImplemented("Communication between agents")

		elif(direction == 'L'): # 'L' for 'LEFT'
			if(self.position % self.puzzle.n != 0):
				if self.puzzle.array[self.position - 1] == 0:
					self.puzzle.move(self, self.position - 1)
				else:
					raise NotImplemented("Communication between agents")

		elif(direction == 'R'): # 'R' for 'RIGHT'
			if((self.position + 1) % self.puzzle.n != 0):
				if self.puzzle.array[self.position + 1] == 0:
					self.puzzle.move(self, self.position + 1)
				else:
					raise NotImplemented("Communication between agents")


