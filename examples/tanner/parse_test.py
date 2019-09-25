import re

# input_file_location = "schematic_oscillator_tb_n1a_tb_TSP/schematic_oscillator_tb_n1a_tb_TSP.measure"
# input_file_location = "schematic_oscillator_tb_n1a_tb_TSP/schematic_oscillator_tb_n1a_tb_TSP.log"
input_file_location = "_data/schematic_oscillator_tb_n1a_tb_TSP/schematic_oscillator_tb_n1a_tb_TSP.measure"


"""  Open the operating point file to begin parsing  """
input_file = open(input_file_location)

# loop through each line in the text
period = []
for line_number, line in enumerate(input_file):

	print(line)

	# tm results
	if line_number == 1:
		print(line)
		period.append( float( re.findall(re.compile("[\d\.]+"), line)[0] ) * 1e-9 )

	# search for a number in scientific notation
	match = re.findall(re.compile("([+-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+))$"), line)

	# a matching regex has been found
	if match:
		print(line)
		period.append( float(match[0]) )

# covert to normalised difference
error = []
for _ in period[1:]:
	print("-"*100)
	print(_)
	print( _ - period[0]) 
	print(period[0]) 
	print( (_ - period[0]) / period[0] )
	error.append( abs((_ - period[0]) / period[0]) )

print(period)
print(error)

# return the largest error
fitness = max(error)
print("Fitness = ", fitness)
