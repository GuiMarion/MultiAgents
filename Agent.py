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

	def __str__(self):
		return str(self.id)

	def run(self):
		print("Agent " + str(self.id) + " : je suis à la position " + str(self.position) + " et je vais à la position " + str(self.goal))
		# while self.position != self.goal:

	def go(direction):
		if(direction == 'U'): # 'U' for 'UP'
			if(self.position >= self.puzzle.n):
				if self.puzzle[position - self.puzzle.n] == 0:
					if self.puzzle.move(position - self.puzzle.n):
						self.position = position - self.puzzle.n
				else:
					raise NotImplemented("Communication between agents")

		elif(direction == 'D'): # 'D' for 'DOWN'
			if(self.position < self.puzzle.size - self.puzzle.n):
				self.position = position + self.puzzle.n
		elif(direction == 'L'): # 'L' for 'LEFT'
			if(self.position % self.puzzle.n != 0):
				self.position = position - 1
		elif(direction == 'R'): # 'R' for 'RIGHT'
			if((self.position+1) % self.puzzle.n != 0):
				self.position = position + 1

