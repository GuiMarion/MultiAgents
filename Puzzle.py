from random import randint
from math import sqrt
from Agent import Agent


class Puzzle:

	# @filling : un pourcentage entre 0 et 1
	def __init__(self, n, filling):
		self.size = n * n
		self.agents = [0] * self.size

		for i in range(1, round(filling * self.size) + 1):
			candidate = randint(0, self.size - 1)
			if(self.agents[candidate] == 0):
				goal = randint(0, self.size - 1)
				self.agents[candidate] = Agent(i, candidate, goal)
			else:
				i = i - 1

	def __repr__(self):
		toBePrint = ""
		for i in range(1, self.size + 1):
			if(self.agents[i - 1] != 0):
				toBePrint += " {:>2} ".format(print(self.agents[i - 1]))
			else:
				toBePrint += " {:>2} ".format('×')
			if(i % sqrt(self.size) == 0):
				toBePrint += "\n"
		return toBePrint

	def run(self):
		for i in range(0, self.size):
			if(self.agents[i] != 0):
				self.agents[i].start()
				self.agents[i].join()
