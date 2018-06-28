from threading import Thread
from math import sqrt

class Agent(Thread):
	def __init__(self, id, position, goal):
		Thread.__init__(self)
		self.id = id
		self.position = position
		self.goal = goal

	def __repr__(self):
		return str(self.id)

	def run(self):
		print("Agent " + str(self.id) + " : je suis à la position " + str(self.position) + " et je vais à la position " + str(self.goal))
		# while self.position != self.goal:

	def move(direction):
		if(direction == 'U'): # 'U' for 'UP'
			if(self.position >= sqrt(self.size)):
				self.position = position - sqrt(self.size)
		elif(direction == 'D'): # 'D' for 'DOWN'
			if(self.position < self.sizea - sqrt(self.size)):
				self.position = position + sqrt(self.size)
		elif(direction == 'L'): # 'L' for 'LEFT'
			if(self.position % sqrt(self.size) != 0):
				self.position = position - 1
		elif(direction == 'R'): # 'R' for 'RIGHT'
			if(self.position % sqrt(self.size) != sqrt(self.size) - 1):
				self.position = position + 1
