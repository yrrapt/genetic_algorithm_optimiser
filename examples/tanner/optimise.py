import subprocess
from genetic_algorithm_optimiser import genetic_algorithm_optimiser
import re


# T-Spice location and simulation inputs
tspice_location = "C:/Programs/MGC/Tanner EDA/Tanner Tools v2018.3/x64/tspcmd64.exe"
netlist_location = "schematic_oscillator_tb_n1a_tb_TSP.sp"
input_file_location = "schematic_oscillator_tb_n1a_tb_TSP/schematic_oscillator_tb_n1a_tb_TSP.measure"
log_file_location = "schematic_oscillator_tb_n1a_tb_TSP/schematic_oscillator_tb_n1a_tb_TSP.log"


# specify the setup of the object
population_size = 100
retain = 0.2
random_select = 0.1
mutate = 0.1
parameter_info = [
				{	"name"		:	"w_n1",
					"low"		:	1,
					"high"		:	10,
					"increment"	:	0.1},
				{	"name"		:	"l_n1",
					"low"		:	1,
					"high"		:	10,
					"increment"	:	0.1},
				{	"name"		:	"w_n2",
					"low"		:	1,
					"high"		:	10,
					"increment"	:	0.1},
				{	"name"		:	"l_n2",
					"low"		:	1,
					"high"		:	10,
					"increment"	:	0.1},
				{	"name"		:	"w_p1",
					"low"		:	1,
					"high"		:	10,
					"increment"	:	0.1},
				{	"name"		:	"l_p1",
					"low"		:	1,
					"high"		:	10,
					"increment"	:	0.1},
				{	"name"		:	"w_p2",
					"low"		:	1,
					"high"		:	10,
					"increment"	:	0.1},
				{	"name"		:	"l_p2",
					"low"		:	1,
					"high"		:	10,
					"increment"	:	0.1}]


# create the optimiser object
optimiser = genetic_algorithm_optimiser.genetic_algorithm_optimiser(parameter_info,
																	population_size,
																	retain,
																	random_select,
																	mutate)	


# create a fitness function
def fitness(individual, individual_print=False):


	"""  Perform the simulation  """
	params = []
	param_str = ""
	for i, param in enumerate(individual):
		# params.append("-param="+parameter_info[i]["name"] + "=" + str(param) + "u")
		# param_str += parameter_info[i]["name"] + "=" + str(param) + "u  "
		params.append("-param="+parameter_info[i]["name"] + "=" + "{:.2f}".format(param) + "u")
		param_str += parameter_info[i]["name"] + "=" + "{:.2f}".format(param) + "u  "

	# form the command list and begin the simulation
	command_list = [tspice_location] + params + [netlist_location]
	tspice_run = subprocess.run(command_list)

	if individual_print:
		print("-"*200)
		print("Running with params: " + param_str)


	"""  Open the operating point file to begin parsing  """
	input_file = open(input_file_location)

	# loop through each line in the text
	period = []
	for line_number, line in enumerate(input_file):

		# simulation has failed break out
		if "not found" in line:
			period = [1.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
			break

		# tm results
		if line_number == 1:
			period.append( float( re.findall(re.compile("[\d\.]+"), line)[0] ) * 1e-9 )

		# search for a number in scientific notation
		match = re.findall(re.compile("([+-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+))$"), line)

		# a matching regex has been found
		if match:
			period.append( float(match[0]) )


	# check that the simulation hasn't failed
	for log_line in open(log_file_location):
		if "Simulation failed" in log_line:
			period = [1.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
			break


	# covert to normalised difference
	error = []
	for _ in period[1:]:
		error.append( abs((_ - period[0]) / period[0]) )

	# return the largest error
	fitness = max(error)

	if individual_print:
		print("Periods = ", period)
		print("Fitness = ", fitness)

	# input("Press Enter to continue...")
	return fitness


# assign the fitness to the optimiser object
optimiser.fitness = fitness

# perform the optimisation
optimiser.run(number_iterations=100, update=True, save=True)

# display the results
optimiser.display_results()