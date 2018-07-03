from random import randint
from math import sqrt
from Agent import Agent
from optparse import OptionParser
from threading import Lock
from datetime import datetime

class Puzzle:
	def __init__(self, n, nb_agents, to_print):
		self.n = n
		self.size = n * n
		self.array = [0] * self.size
		self.lock_table = [] 
		self.Start = False
		self.Stop = False
		self.to_print = to_print
		self.nb_coups = 0
		self.Fail = False

		for i in range(self.size):
			#self.lock_table.append(Lock())
			self.lock_table.append(True)

		if(nb_agents > n*n):
			raise ValueError("The number of agents must be less then n*n")

		Goals = []

		for i in range(nb_agents):
			candidate = randint(0, self.size - 1)
			goal = randint(0, self.size - 1)
			while(self.array[candidate] != 0 or goal in Goals):
				candidate = randint(0, self.size - 1)
				goal = randint(0, self.size - 1)

			self.array[candidate] = Agent(i + 1, candidate, goal, self)
			Goals.append(goal)

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
		while end == False and self.Stop == False:
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
				if self.to_print:
					print(self)
				self.nb_coups += 1
				return True
			else:
				self.release(new_position)
				self.release(old_position)
				return False
		else:
			return False

def main(size = 5, nb_agents = 1, to_print = True):

	to_print = to_print
	P = Puzzle(size, nb_agents, to_print)
	if to_print:
		print(P)
	P.run()

	if to_print:
		print("Number of steps :", P.nb_coups)

	if P.Fail:
		return -1

	return P.nb_coups

if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("-s", "--size", dest="size", help="n for the array (that is of size n*n)", metavar="SIZE")
	parser.add_option("-a", "--nb_agents", dest="nb_agents", help="number of agents", metavar="AGENTS")
	parser.add_option("-p", "--dontprint", action="store_true", dest="to_print", help="if you don't want to print", metavar="PRINT")
	parser.add_option("-r", "--repetitions", dest="repetitions", help="number of repetitions", metavar="REPETITIONS")
	parser.add_option("-t", "--test", action="store_true", dest="test", help="if you want to run the stats", metavar="TEST")

	(options, args) = parser.parse_args()

	if options.test :

		# Options that does the stats

		## Size max
		N = 5
		## Max fill
		C = 0.4
		# Nomber of répétitions
		R = 1

		file = open("Stats_"+datetime.now().strftime('%Y-%m-%d__%H:%M'),'w')

		print("Running the script for computing stats (may that a while).")
		file.write("Running the script for computing stats (may that a while). \n \n")

		for n in range(2, N+1):
			for nb_agents in range(1, int(n*n*C)):
				moy = 0
				fails = 0
				for i in range(R):
					res = main(size = n, nb_agents = nb_agents, to_print = False)
					if res != -1:
						moy += res
					else:
						fails += 1


				moy = moy/R

				if fails == R :
					moy = None

				print("n =", n, " ", nb_agents, "agents :")
				print("Average number of steps :", moy)
				if fails > 0 :
					print("Number of fails :", fails)
				print()

				file.write("n = " + str(n) + "  " + str(nb_agents) + " agents :\n")
				file.write("Average number of steps : " + str(moy) + "\n")
				if fails > 0 :
					file.write("Number of fails :" + str(fails) + "\n")
				file.write("\n")


		file.close()


	elif len(args) == 0:
		to_print = True
		if options.to_print is not None:
			to_print = False

		if options.repetitions is None:
			options.repetitions = 1

		moy = 0
		try:
			for i in range(int(options.repetitions)):
				if options.size is not None and options.nb_agents is not None:
					moy += main(size = int(options.size), nb_agents = int(options.nb_agents), to_print = to_print)
				elif options.size is None and options.nb_agents is not None:
					moy += main(nb_agents = int(options.nb_agents), to_print = to_print)
				elif options.size is not None and options.nb_agents is None:
					moy += main(size = int(options.size), to_print = to_print)
				else:
					moy += main(to_print = to_print)

			print("Average number of steps :",moy/int(options.repetitions))

		except ValueError:
			print("Please provide integers as options")
			exit(1)
	else:
		print("Usage: Python3 Puzzle.py -s <size> -a <nb_agents> with integers")

