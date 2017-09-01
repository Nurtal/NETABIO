"""
This file extract data from raw data file
and generate new data files
"""

import biotoolbox



def generate_HLA_data_file(input_data_file):
	"""
	=> Create a csv file with only the HLA Variables
	and the diagnostic from the file input_data_file
	"""
	## preprocessing input file
	biotoolbox.change_file_format(input_data_file, ",")
	data_reformated_file = input_data_file.split(".")
	data_reformated_file = data_reformated_file[0]+"_reformated.csv"

	## Extract HLA Variables, add the Diagnostic
	index_to_keep = []
	diagnostic_index = -1
	data = open(data_reformated_file, "r")
	output = open("HLA_data.csv", "w")
	cmpt = 0
	for line in data:
		line = line.split("\n")
		line = line[0]
		line_in_array = line.split(",")
		diagnostic = "poulet" # init the variable

		if(cmpt == 0):
			index = 0
			header_in_string = ""
			for element in line_in_array:
				element_in_array = element.split("\\")
				if("HLA" in element_in_array):
					index_to_keep.append(index)
					header_in_string += str(element)+","
				elif("DISEASE" in element_in_array):
					diagnostic_index = index
				index += 1

			header_in_string = header_in_string[:-1]+",Diagnostic"
			header_in_string = header_in_string.replace(" ", "")
			output.write(header_in_string+"\n")

		else:
			index = 0
			line_in_string = ""
			diagnostic = line_in_array[diagnostic_index]
			if(diagnostic == ""):
				diagnostic = "control"
			for element in line_in_array:
				if(index in index_to_keep):
					line_in_string += str(element)+","
				index += 1

			line_in_string = line_in_string[:-1]+","+str(diagnostic)
			line_in_string = line_in_string.replace(" ", "")
			output.write(line_in_string+"\n")
		cmpt += 1

	output.close()
	data.close()



def generate_Luminex_data_file(input_data_file, **optional_args):
	"""
	=> Create a csv file with only the Luminex Variables
	and the diagnostic

	- input_data_file is the name of the input data file
	- optional_args contains the optional parameters, such as:
	- "phase": The selected phase, could be:
		- "all" -> get all patients
		- "I" -> get only phase I patients
		- "II" -> get only phase II patients
	"""
	## preprocessing input file
	biotoolbox.change_file_format(input_data_file, ",")
	data_reformated_file = input_data_file.split(".")
	data_reformated_file = data_reformated_file[0]+"_reformated.csv"


	## Looking for optional arguments
	specific_phase_selected = False
	if("phase" in optional_args):
		specific_phase_selected = True
		phase_selected = optional_args['phase']


	## Extract Luminex Variables, add the Diagnostic
	index_to_keep = []
	diagnostic_index = -1
	phase_index = -1
	data = open(data_reformated_file, "r")
	output = open("Luminex_data.csv", "w")
	cmpt = 0
	for line in data:
		line = line.split("\n")
		line = line[0]
		line_in_array = line.split(",")
		diagnostic = "poulet" # init the variable
		phase = "choucroute"

		if(cmpt == 0):
			index = 0
			header_in_string = ""
			for element in line_in_array:
				element_in_array = element.split("\\")
				if("Luminex" in element_in_array):
					index_to_keep.append(index)
					header_in_string += str(element)+","
				elif("DISEASE" in element_in_array):
					diagnostic_index = index
				elif("CSPHASE" in element_in_array):
					phase_index = index
				index += 1

			header_in_string = header_in_string[:-1]+",Diagnostic"
			header_in_string = header_in_string.replace(" ", "")
			output.write(header_in_string+"\n")

		else:
			index = 0
			line_in_string = ""
			diagnostic = line_in_array[diagnostic_index]
			phase = line_in_array[phase_index]
			if(diagnostic == ""):
				diagnostic = "control"
			for element in line_in_array:
				if(index in index_to_keep):
					line_in_string += str(element)+","
				index += 1

			line_in_string = line_in_string[:-1]+","+str(diagnostic)
			line_in_string = line_in_string.replace(" ", "")

			if(specific_phase_selected):
				if(phase == "\"I\"" and phase_selected == "I"):
					output.write(line_in_string+"\n")
				elif(phase == "\"II\"" and phase_selected == "II"):
					output.write(line_in_string+"\n")
				elif(phase_selected == "all"):
					output.write(line_in_string+"\n")
			else:
				output.write(line_in_string+"\n")

		cmpt += 1

	output.close()
	data.close()



def generate_Flow_data_file(input_data_file):
	"""
	=> Create a csv file with only the Flow cytometry Variables
	and the diagnostic
	"""
	## preprocessing input file
	biotoolbox.change_file_format(input_data_file, ",")
	data_reformated_file = input_data_file.split(".")
	data_reformated_file = data_reformated_file[0]+"_reformated.csv"

	## Extract Flow cytometry Variables, add the Diagnostic
	index_to_keep = []
	diagnostic_index = -1
	data = open(data_reformated_file, "r")
	output = open("FlowCytometry_data.csv", "w")
	cmpt = 0
	for line in data:
		line = line.split("\n")
		line = line[0]
		line_in_array = line.split(",")
		diagnostic = "poulet" # init the variable

		if(cmpt == 0):
			index = 0
			header_in_string = ""
			for element in line_in_array:
				element_in_array = element.split("\\")
				if("Flowcytometry" in element_in_array):
					index_to_keep.append(index)
					header_in_string += str(element)+","
				elif("DISEASE" in element_in_array):
					diagnostic_index = index
				index += 1

			header_in_string = header_in_string[:-1]+",Diagnostic"
			header_in_string = header_in_string.replace(" ", "")
			output.write(header_in_string+"\n")

		else:
			index = 0
			line_in_string = ""
			if(diagnostic == ""):
				diagnostic = "control"
			diagnostic = line_in_array[diagnostic_index]
			for element in line_in_array:
				if(index in index_to_keep):
					line_in_string += str(element)+","
				index += 1

			line_in_string = line_in_string[:-1]+","+str(diagnostic)
			line_in_string = line_in_string.replace(" ", "")
			output.write(line_in_string+"\n")
		cmpt += 1

	output.close()
	data.close()

