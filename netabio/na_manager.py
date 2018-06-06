"""
=> Deal with NA in data files
"""

import matplotlib
matplotlib.use('TkAgg') 
from matplotlib import pyplot as plt
import operator


def check_NA_proportion_in_file(data_file_name):
	"""
	-> data_file_name is a csv file, generate via the 
	   reformat_luminex_raw_data() function
	-> Evaluate the proportion of NA values in each variable
	-> return a dictionnary
	"""

	position_to_variable = {}
	variable_to_NA_count = {}

	## Count NA values for each variable
	## in data file.
	cmpt = 0
	input_data = open(data_file_name, "r")
	for line in input_data:
		line = line.split("\n")
		line = line[0]
		line_in_array = line.split(",")
		
		if(cmpt == 0):
			index = 0
			for variable in line_in_array:
				position_to_variable[index] = variable
				variable_to_NA_count[variable] = 0
				index +=1
		else:
			index = 0
			for scalar in line_in_array:
				if(scalar == "NA" or scalar == "" or scalar == " "):
					variable_to_NA_count[position_to_variable[index]] += 1
				index+=1

		cmpt += 1
	input_data.close()

	## Compute the %
	for key in variable_to_NA_count.keys():
		variable_to_NA_count[key] = float((float(variable_to_NA_count[key]) / float(cmpt)) * 100)

	## return dict
	return variable_to_NA_count



def display_NA_proportions(data_file_name):
	##
	## -> Generate bar chart of NA values for
	##    each variables in data_file_name
	## -> use the check_NA_proportion_in_file() function
	##    to get the NA proportion
	## -> Show the bar plot
	##

	## Get informations
	variable_to_NA_count = check_NA_proportion_in_file(data_file_name)
	
	## Create Plot
	plt.bar(range(len(variable_to_NA_count)), variable_to_NA_count.values(), align='center')
	plt.xticks(range(len(variable_to_NA_count)), variable_to_NA_count.keys(), rotation=90)

	## [DISABLE] Save plot
	#plt.savefig("")

	## Show plot
	plt.show()





def filter_NA_values(data_file_name):
	"""
	-> Evaluate the proportion of NA values in each variable
	   (use the check_NA_proportion_in_file() function).
	-> Find the minimum proportion of NA (minimum_score, i.e almost
		patient have non NA values for this feature, except a few ones
		wich have a lot of NA)
	-> Rewrite a file (data/Luminex_phase_I_raw_data_filtered.csv) with only
	   the selected variables
	"""

	## Structure initialization
	score_list = []
	variable_saved = []

	## Get information on NA proportion in data file
	variable_to_NA_proportion = check_NA_proportion_in_file(data_file_name)

	## find minimum score of NA among variables
	## Exluding OMICID and DISEASE (every patient should have one)
	for key in variable_to_NA_proportion.keys():
		if(key != "\\Clinical\\Sampling\\OMICID" and key != "\\Clinical\\Diagnosis\\DISEASE" and key != "Diagnostic" and key != "Disease"):
			score_list.append(variable_to_NA_proportion[key])
	minimum_score = min(score_list)

	## Use minimum score as a treshold for
	## selecting variables
	for key in variable_to_NA_proportion.keys():
		if(float(variable_to_NA_proportion[key]) > float(minimum_score)):
			variable_saved.append(key)

	## Log message
	print "[+] Selecting "+str(len(variable_saved))+" variables among "+str(len(variable_to_NA_proportion.keys())) +" ["+str((float(len(variable_to_NA_proportion.keys()))-float(len(variable_saved))) / float(len(variable_to_NA_proportion.keys()))*100)+"%]"

	## Create a new filtered data file
	index_to_keep = []
	cmpt = 0
	input_data_file = open(data_file_name, "r")
	output_data_file_name = data_file_name.split(".")
	output_data_file_name = output_data_file_name[0] +"_NA_filtered.csv"
	output_data_file = open(output_data_file_name, "w")
	for line in input_data_file:
		line = line.split("\n")
		line = line[0]
		line_in_array = line.split(",")
		if(cmpt == 0):
			header_in_line = ""
			index = 0
			for variable in line_in_array:
				score = float(variable_to_NA_proportion[variable])
				if(score <= minimum_score):
					header_in_line += str(variable) +","
					index_to_keep.append(index)
				index +=1
			header_in_line = header_in_line[:-1]
			output_data_file.write(header_in_line+"\n")
		else:
			line_to_write = ""
			index = 0
			for scalar in line_in_array:
				if(index in index_to_keep):
					line_to_write += str(scalar) + ","
				index += 1

			line_to_write = line_to_write[:-1]
			output_data_file.write(line_to_write+"\n") 
		cmpt += 1
	output_data_file.close()
	input_data_file.close()



def na_block_change(input_data_file, display):
	"""
	
	*input_data_file is a string, the name of the data file
	*display is a boolean, set to True to display grid
     optimization in console.

	Algorithm to deal with na values in data file.
	Tries to minimize the loss of information and
	drop all NA in datafile by perform only two type
	of actions:
		- drop patients (i.e lines)
		- drop variables (i.e col)

	each action is associated to a cost, given by the formula:
		- Cost = (1/nb_variable_type)*information_lost
		  Where nb_variable_type is the number of line or column
		  left in the dataset and information_lost is the number of 
		  scalar lost if the column/line is deleted.

	The algorithm stop if:
		- The number of patients left is too small (below a treshold)
		- The number of variables left is too small (below a treshold)
		- No missing values left in data file
		- Iteration reach the mawimum of authorized iteration (treshold)

	
	require operator

	Generate an csv output file with the tag "_NaBlockManaged"

	"""

	##--------------------##
	## General parameters ##
	##--------------------##
	

	## Tresholds and structure
	min_variable_authorized = 3
	min_patient_authorized = 3
	maximum_number_of_iteration = 1000
	na_values = ["NA", "na", "Na", ""]
	number_of_iteration = 0
	action_list = []

	## Check variable
	patients_left_in_grid = True
	variables_left_in_grid = True
	na_left_in_grid = True
	action_authorized = True
	under_max_iteration = True

	##---------------------##
	## Grid initialisation ##
	##---------------------##

	## Create Grid
	grid = []
	data_file = open(input_data_file, "r")
	for line in data_file:
		line = line.rstrip()
		vector = line.split(",")		
		grid.append(vector)
	data_file.close()

	
	##-------------------##
	## Grid optimisation ##
	##-------------------##

	while(action_authorized):

		##---------------------##
		## Check authorization ##
		##---------------------##

		## check the number of iteration
		if(number_of_iteration >= maximum_number_of_iteration):
			under_max_iteration = False
			print "[-] reach maximum number of iteration :"+str(number_of_iteration)

		## count variables in grid
		if(len(grid[0]) < min_variable_authorized):
			variables_left_in_grid = False
			print "[-] reach minimum number of variables :"+str(len(grid[0]))

		## count patients in grid
		if(len(grid) < min_patient_authorized):
			patients_left_in_grid = False
			print "[-] reach minimum number of patients :"+str(len(grid))

		## count NA values in grid
		na_count = 0
		for vector in grid:
			for scalar in vector:
				if(scalar in na_values):
					na_count += 1
		if(na_count == 0):
			na_left_in_grid = False

		## Check if we can do something
		if(na_left_in_grid and patients_left_in_grid and variables_left_in_grid and under_max_iteration):
			action_authorized = True
		else:
			action_authorized = False


		##--------------##
		## Optimization ##
		##--------------##
		if(action_authorized):


			##--------------##
			## Display grid ##
			##--------------##
			if(display):
				print "-"*len(grid[0])*3
				display_grid = []
				na_char = "?"
				good_char = "#"
				na_values = ["NA", "na", "Na", ""]

				## create display grid
				for vector in grid:
					display_vector = []
					for elt in vector:
						if(elt in na_values):
							display_vector.append(na_char)
						else:
							display_vector.append(good_char)
					display_grid.append(display_vector)

				## display
				display_grid_in_string = ""
				for display_vector in display_grid:
					display_vector_in_string = ""
					for scalar in display_vector:
						display_vector_in_string += " " + str(scalar)+ " "
			
					print display_vector_in_string
				print "-"*len(grid[0])*3


			##-------------------------##
			## Screen possible actions ##
			##-------------------------##
			## compute cost of deleting patients
			possibles_action = {}
			na_in_vector = 0
			number_of_patients = len(grid)
			cmpt = 0
			for vector in grid:
				deleting_cost = 0 
				na_in_vector = 0
				information_in_vector = 0
				for scalar in vector:
					if(scalar in na_values):
						na_in_vector += 1
					else:
						information_in_vector += 1
				## cost of deleting this specific patient
				deleting_cost = float((1.0/number_of_patients)*information_in_vector)
				cmpt += 1
				
				possibles_action["line_"+str(cmpt)] = deleting_cost

			## compute cost of deleting columns
			columns_list = []
			for scalar in grid[0]:
				columns_list.append([])
			for vector in grid:
				index = 0
				for scalar in vector:
					columns_list[index].append(scalar)
					index += 1
			number_of_columns = len(columns_list)
			cmpt = 0
			for vector in columns_list:
				deleting_cost = 0 
				na_in_vector = 0
				information_in_vector = 0
				for scalar in vector:
					if(scalar in na_values):
						na_in_vector += 1
					else:
						information_in_vector += 1

				## cost of deleting this specific variable
				deleting_cost = float((1.0/number_of_columns)*information_in_vector)
				cmpt += 1

				possibles_action["col_"+str(cmpt)] = deleting_cost

			## Select best possible action (i.e the lowest cost)
			possibles_action = sorted(possibles_action.items(), key=operator.itemgetter(1))
			action_selected = possibles_action[0]


			##----------------##
			## Perform action ##
			##----------------##
			instruction = action_selected[0].split("_")
			variable_type = instruction[0]
			target = int(instruction[1]) - 1
			action_list.append(action_selected)

			## => delete patient
			if(variable_type == "line"):
				new_grid = []
				cmpt = 0
				for vector in grid:
					if(cmpt != target):
						new_grid.append(vector)
					cmpt += 1

			## => delete variable
			elif(variable_type == "col"):
				new_grid = []

				cmpt = 0
				for vector in grid:
					new_vector = []
					index = 0
					for scalar in vector:
						if(index != int(target)):
							new_vector.append(scalar)
						index += 1
					cmpt += 1

					new_grid.append(new_vector)

			## Update grid
			grid = new_grid
			number_of_iteration += 1

		##-------------------------##
		## Write the new data file ##
		##-------------------------##
		output_filename = input_data_file.split(".")
		output_filename = str(output_filename[0])+"_NaBlockManaged.csv"
		output_file = open(output_filename, "w")
		cmpt = 1
		for vector in grid:
			line_to_write = ""
			for scalar in vector:
				line_to_write += str(scalar)+","
			if(cmpt != len(grid)):
				line_to_write = line_to_write[:-1]+"\n"
			else:
				line_to_write = line_to_write[:-1]
			output_file.write(line_to_write)
			cmpt += 1

		output_file.close()
