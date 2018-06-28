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
		print("Agent " + str(self.id) + " : je suis à la position " + str(self.position) + " et je vais à la position " + str(self.goal))
		# while self.position != self.goal:

		dico = {}

		dico['U'] = abs((self.position - self.puzzle.n) // n - (self.goal //n)) + abs((self.position - self.puzzle.n) % n - (self.goal % n))	
		dico['D'] = abs((self.position + self.puzzle.n) // n - (self.goal //n)) + abs((self.position + self.puzzle.n) % n - (self.goal % n))
		dico['L'] = abs((self.position - 1) // n - (self.goal //n)) + abs((self.position - 1) % n - (self.goal % n))	
		dico['R'] = abs((self.position + 1) // n - (self.goal //n)) + abs((self.position + 1) % n - (self.goal % n))	


	def go(direction):
		if(direction == 'U'): # 'U' for 'UP'
			if(self.position >= self.puzzle.n):
				if self.puzzle.array[self.position - self.puzzle.n] == 0:
					self.puzzle.move(self.id, self.position - self.puzzle.n)
				else:
					raise NotImplemented("Communication between agents")

		elif(direction == 'D'): # 'D' for 'DOWN'
			if(self.position < self.puzzle.size - self.puzzle.n):
				if self.puzzle.array[self.position + self.puzzle.n] == 0:
					self.puzzle.move(self.id, self.position + self.puzzle.n)
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
					self.puzzle.move(self.id, self.position + 1)
				else:
					raise NotImplemented("Communication between agents")


