"""
=> Deal with NA in data files
"""

import matplotlib.pyplot as plt


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

