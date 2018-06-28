from random import randint
from math import sqrt
from Agent import Agent
from optparse import OptionParser
from threading import Lock

class Puzzle:
	def __init__(self, n, nb_agents):
		self.n = n
		self.size = n * n
		self.array = [0] * self.size
		self.lock_table = [] 
		self.Start = False
		self.Stop = False
		for i in range(self.size):
			#self.lock_table.append(Lock())
			self.lock_table.append(True)

		if(nb_agents > n*n):
			raise ValueError("The number of agents must be less then n*n")

		for i in range(nb_agents):
			candidate = randint(0, self.size - 1)
			goal = randint(0, self.size - 1)
			while(self.array[candidate] != 0 or self.array[goal] != 0):
				candidate = randint(0, self.size - 1)
				goal = randint(0, self.size - 1)
			self.array[candidate] = Agent(i + 1, candidate, goal, self)

	def __repr__(self):
		toBePrint = ""
		for i in range(self.size):
			if(self.array[i] != 0):
				toBePrint += " {:>2} ".format(str(self.array[i]))
			else:
				toBePrint += " {:>2} ".format('×')
			if((	i+1) % self.n == 0):
				toBePrint += "\n"
		return toBePrint

	def run(self):
		L = []
		for i in range(0, self.size):
			if(self.array[i] != 0):
				self.array[i].start()
				L.append(self.array[i])
		self.Start = True

		end = False
		while end == False:
			end = True
			for elem in L :
				if elem.position != elem.goal:
					end = False

		self.Stop = True

	def move2(self, agent, new_position):

		if self.lock_table[new_position].acquire(False) and self.lock_table[agent.position].acquire(False):
			self.lock_table[agent.position].acquire(False)
			self.lock_table[new_position].acquire(False)
			if self.array[new_position] == 0:
				self.array[new_position] = agent
				self.array[agent.position] = 0
				agent.position = new_position
				self.lock_table[new_position].release()
				self.lock_table[agent.position].release()
				print(self)
				return True
			else:
				self.lock_table[new_position].release()
				self.lock_table[agent.position].release()
				return False
		else:
			return False

	def acquire(self, index):
		if self.lock_table[index]:
			self.lock_table[index] = False
			return True
		else: 
			return False

	def release(self, index):
		self.lock_table[index] = True


	def move(self, agent, new_position):

		old_position = agent.position

		if self.acquire(new_position) and self.acquire(agent.position):
			if self.array[new_position] == 0:
				self.array[new_position] = agent
				self.array[agent.position] = 0
				agent.position = new_position
				self.release(new_position)
				self.release(old_position)
				print(self)
				return True
			else:
				self.release(new_position)
				self.release(old_position)
				return False
		else:
			return False

def main(size = 5, nb_agents = 1):
	P = Puzzle(size, nb_agents)
	print(P)
	P.run()

if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("-s", "--size", dest="size", help="n for the array (that is of size n*n)", metavar="SIZE")
	parser.add_option("-a", "--nb_agents", dest="nb_agents", help="number of agents", metavar="AGENTS")

	(options, args) = parser.parse_args()

	if len(args) == 0:
		try:
			if options.size is not None and options.nb_agents is not None:
				main(size = int(options.size), nb_agents = int(options.nb_agents))
			elif options.size is None and options.nb_agents is not None:
				main(nb_agents = int(options.nb_agents))
			elif options.size is not None and options.nb_agents is None:
				main(size = int(options.size))
			else:
				main()
		# print(distributions[(15,15,0)])
		except ValueError:
			print("Usage: Python3 Puzzle.py -s <size> -a <nb_agents> with integers")
	else:
		print("Usage: Python3 Puzzle.py -s <size> -a <nb_agents> with integers")

