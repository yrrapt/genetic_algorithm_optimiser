# Genetic Algorithm Optimiser
#
#  Inspired by the tutorial:
#  http://lethain.com/genetic-algorithms-cool-name-damn-simple/
#
#  A number of functions need to be defined by the calling script
 
from random import randint, random
import random
from operator import add
import math
import json
from functools import reduce
from operator import itemgetter
from matplotlib import pyplot as plt


class genetic_algorithm_optimiser:
	"""
	An class which implements a simple genetic algorithm optimiser.
	The instantiating scope must create suitable a suitable fitness
	function and execute test function.

	A dictionary of the parameters of the system to optimise must also
	be specified in the following format:
		parameter = {	"name"	  :   name,
						"low"	   :   0,
						"high"	  :   10,
						"increment" :   0.1}
		parameter_info = [parameter]*10
	"""



	def __init__(self, 	parameter_info,
						population_size=100, 
						retain=0.2, 
						random_select=0.05, 
						mutate=0.01):
		"""
		Constructor which sets up the optimiser
		"""

		# save the evolution control parameters internally
		self.parameter_info = parameter_info
		self.retain = retain
		self.random_select = random_select
		self.mutate = mutate

		# create a population with the specified size
		self.population = self.populate(population_size)



	def random_param(self, parameter):
		"""
		Loop through each parameter creating random values
		each parameter is limited to the increment/resolution specified
		"""
		random_number = random.random() * float(( parameter["high"] - parameter["low"] ) + parameter["low"])
		rounded_number = parameter["increment"] * round( random_number / parameter["increment"] )
		return rounded_number



	def individual(self):
		"""
		Loop through each parameter creating random values
		each parameter is limited to the increment/resolution specified
		"""
		individual = []
		for parameter in self.parameter_info:
			individual.append( self.random_param(parameter) )
		return individual



	def populate(self, count):
		"""
		Create a number of individuals (i.e. a population). 
		"""
		return [ self.individual() for x in range(count) ]



	# create a way to determine how close an indivual is to our goal
	def fitness(self, individual):
		"""
		Determine the fitness of an individual. Lower is better.
	 
		individual: the individual to evaluate
		"""
		assert False, "No fitness function has been defined!"



	def grade(self):
		'''
		Find average fitness for a population.
		it's useful to have a way to gauge the populations average fitness
		'''
		summed = reduce(add, (self.fitness(_) for _ in self.population), 0)
		return summed / (len(self.population) * 1.0)



	def evolve(self):
		'''
		Create a way to evolve our population
		'''

		# calculate the fitness for each individual in the population
		graded = [ (self.fitness(_), _) for _ in self.population]

		# sort the population and keep the best
		graded = [ x[1] for x in sorted(graded) ]
		retain_length = int(len(graded) * self.retain)
		parents = graded[:retain_length]
	 
		# randomly add other individuals to promote genetic diversity
		for individual in graded[retain_length:]:
			if self.random_select > random.random():
				parents.append(individual)
	 
		# mutate some individuals
		for individual in parents:
			if self.mutate > random.random():
				pos_to_mutate = randint(0, len(individual)-1)
				individual[pos_to_mutate] = self.random_param(self.parameter_info[pos_to_mutate])
	 
		# crossover parents to create children
		parents_length = len(parents)
		desired_length = len(self.population) - parents_length
		children = []
		while len(children) < desired_length:
			male = randint(0, parents_length-1)
			female = randint(0, parents_length-1)

			if male != female:
				male = parents[male]
				female = parents[female]
				half = int( max(len(male), len(female)) / 2 )
				child = male[:half] + female[half:]
				children.append(child)

		parents.extend(children)
		self.population = parents



	def save_population(self, output_file='population.json'):
		"""
		Save the current state of the population
		"""

		with open(output_file, 'w') as f:
   			json.dump(self.population, f)


	def run(self, number_iterations=1000, update=False, save=False):
		"""
		Perform the optimisation
		"""

		# find the fitness of each memeber of the population
		self.fitness_history = [self.grade(),]
		self.best_history = []
		ind_grade = []
		for ind in self.population:
			ind_grade.append(self.fitness(ind))
		self.best_history.append(self.fitness(self.population[min(enumerate(ind_grade), key=itemgetter(1))[0]]))

		# evolve the population
		for i in range(number_iterations):
			self.evolve()
			self.fitness_history.append(self.grade())
		 
			ind_grade = []
			for ind in self.population:

				# save the current state of the population
				if save:
					self.save_population()

				ind_grade.append(self.fitness(ind))
			self.best_history.append(self.fitness(self.population[min(enumerate(ind_grade), key=itemgetter(1))[0]]))

			if update:
				print("Iteration %d complete, best fitness achieved is %f" % (i, self.best_history[-1]))



	def display_results(self, plot_en=True, print_en=True):
		"""
		Display the reuslts by plotting and printing the progression of the optimisation
		algorithm
		"""

		# plot the history of the population fitness
		if plot_en:
			plt.plot(self.fitness_history)
			plt.plot(self.best_history)
			plt.legend(['Average','Best'])
			plt.show()
		if print_en:
			print(self.fitness_history[-1])
		 		 
		# print the best result
		if print_en:
			ind_grade = []
			for ind in self.population:
				ind_grade.append(self.fitness(ind))
			best = self.population[min(enumerate(ind_grade), key=itemgetter(1))[0]]
			self.fitness(best)
			print(best)