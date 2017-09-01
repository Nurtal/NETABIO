"""
This file extract data from raw data file
and generate new data files
"""

import biotoolbox



def generate_HLA_data_file(input_data_file, **optional_args):
	"""
	=> Create a csv file with only the HLA Variables
	and the diagnostic from the file input_data_file

	- input_data_file is the name of the input data file
	- optional_args contains the optional parameters, such as:
		- "phase": The selected phase, could be:
			- "all" -> get all patients
			- "I" -> get only phase I patients
			- "II" -> get only phase II patients
		- "group": by defaut the selected group is disease,
		   but this parameter can accept:
		   - "medication" -> list of medication applied to the patient (sep by ";")
		   - "treatment" -> treated if patient have any medication, else control.
		- "group_pos": the position of the group in the generated file, defaut is the last column
		  of the new file. could be:
			-"start" -> first column
			-"end" -> last column
		- "group_name": the name of the group column
	"""
	## preprocessing input file
	biotoolbox.change_file_format(input_data_file, ",")
	data_reformated_file = input_data_file.split(".")
	data_reformated_file = data_reformated_file[0]+"_reformated.csv"

	## Looking for optional arguments
	specific_phase_selected = False
	specific_group_selected = False
	artificial_group_selected = False
	specific_group_position_selected = False
	specific_group_name_selected = False
	group_name = "Diagnostic" 
	if("phase" in optional_args):
		specific_phase_selected = True
		phase_selected = optional_args['phase']
	if("group" in optional_args):
		specific_group_selected = True
		group_selected = optional_args['group']
		if(group_selected == "medication" or group_selected == "treatment"):
			artificial_group_selected = True
			groupFeatures_to_positions = {}
	if("group_pos" in optional_args):
		specific_group_position_selected = True
		group_position = optional_args["group_pos"]
	if("group_name" in optional_args):
		specific_group_name_selected = True
		group_name = optional_args["group_name"]

	## Extract HLA Variables, add the Diagnostic
	index_to_keep = []
	group_index = -1
	phase_index = -1
	data = open(data_reformated_file, "r")
	output = open("HLA_data.csv", "w")
	cmpt = 0
	for line in data:
		line = line.split("\n")
		line = line[0]
		line_in_array = line.split(",")
		group = "poulet" # init the variable
		phase = "choucroute"

		if(cmpt == 0):
			index = 0
			header_in_string = ""

			if(specific_group_selected):
				for element in line_in_array:
					element_in_array = element.split("\\")
					if("HLA" in element_in_array):
						index_to_keep.append(index)
						header_in_string += str(element)+","
					elif("CSPHASE" in element_in_array):
						phase_index = index
					elif("DISEASE" in element_in_array and group_selected == "diagnostic"):
						group_index = index					
					elif("SEX" in element_in_array and group_selected == "sex"):
						group_index = index
					elif("Medication" in element_in_array and group_selected == "medication"):
						groupFeatures_to_positions[element_in_array[-2]] = index
					elif("Medication" in element_in_array and group_selected == "treatment"):
						groupFeatures_to_positions[element_in_array[-2]] = index					
					index += 1

			else:
				for element in line_in_array:
					element_in_array = element.split("\\")
					if("Luminex" in element_in_array):
						index_to_keep.append(index)
						header_in_string += str(element)+","
					elif("DISEASE" in element_in_array and not specific_group_selected):
						group_index = index
					elif("CSPHASE" in element_in_array):
						phase_index = index
					index += 1

			if(specific_group_position_selected):
				if(group_position == "start"):
					header_in_string = str(group_name)+","+header_in_string[:-1]
				else:
					header_in_string = header_in_string[:-1]+","+str(group_name)
			else:
				header_in_string = header_in_string[:-1]+","+str(group_name)

			header_in_string = header_in_string.replace(" ", "")
			output.write(header_in_string+"\n")

		else:
			index = 0
			line_in_string = ""
			phase = line_in_array[phase_index]
			if(specific_group_selected):
				if(artificial_group_selected):		
					if(group_selected == "medication"):
						group = ""
						for med in groupFeatures_to_positions.keys():
							if(line_in_array[groupFeatures_to_positions[med]] == "\"Yes\""):
								group += str(med)+";"
						group = group[:-1]
						if(group == ""):
							group = "control"
					elif(group_selected == "treatment"):
						group = "control"
						for med in groupFeatures_to_positions.keys():
							if(line_in_array[groupFeatures_to_positions[med]] == "\"Yes\""):
								group = "treated"
				else:
					group = line_in_array[group_index]
			else:
				group = line_in_array[group_index]
				if(group == ""):
					group = "control"
			
			for element in line_in_array:
				if(index in index_to_keep):
					line_in_string += str(element)+","
				index += 1

			if(specific_group_position_selected):
				if(group_position == "start"):
					line_in_string = str(group)+","+line_in_string[:-1]
				else:
					line_in_string = line_in_string[:-1]+","+str(group)
			else:
				line_in_string = line_in_string[:-1]+","+str(group)
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
		- "group": by defaut the selected group is disease,
		   but this parameter can accept:
		   - "medication" -> list of medication applied to the patient (sep by ";")
		   - "treatment" -> treated if patient have any medication, else control.
		- "group_pos": the position of the group in the generated file, defaut is the last column
		  of the new file. could be:
			-"start" -> first column
			-"end" -> last column
		- "group_name": the name of the group column
	"""
	## preprocessing input file
	biotoolbox.change_file_format(input_data_file, ",")
	data_reformated_file = input_data_file.split(".")
	data_reformated_file = data_reformated_file[0]+"_reformated.csv"

	## Looking for optional arguments
	specific_phase_selected = False
	specific_group_selected = False
	artificial_group_selected = False
	specific_group_position_selected = False
	specific_group_name_selected = False
	group_name = "Diagnostic" 
	if("phase" in optional_args):
		specific_phase_selected = True
		phase_selected = optional_args['phase']
	if("group" in optional_args):
		specific_group_selected = True
		group_selected = optional_args['group']
		if(group_selected == "medication" or group_selected == "treatment"):
			artificial_group_selected = True
			groupFeatures_to_positions = {}
	if("group_pos" in optional_args):
		specific_group_position_selected = True
		group_position = optional_args["group_pos"]
	if("group_name" in optional_args):
		specific_group_name_selected = True
		group_name = optional_args["group_name"]

	## Extract Luminex Variables, add the Diagnostic
	index_to_keep = []
	group_index = -1
	phase_index = -1
	data = open(data_reformated_file, "r")
	output = open("Luminex_data.csv", "w")
	cmpt = 0
	for line in data:
		line = line.split("\n")
		line = line[0]
		line_in_array = line.split(",")
		group = "poulet" # init the variable
		phase = "choucroute"

		if(cmpt == 0):
			index = 0
			header_in_string = ""

			if(specific_group_selected):
				for element in line_in_array:
					element_in_array = element.split("\\")
					if("Luminex" in element_in_array):
						index_to_keep.append(index)
						header_in_string += str(element)+","
					elif("CSPHASE" in element_in_array):
						phase_index = index
					elif("DISEASE" in element_in_array and group_selected == "diagnostic"):
						group_index = index					
					elif("SEX" in element_in_array and group_selected == "sex"):
						group_index = index
					elif("Medication" in element_in_array and group_selected == "medication"):
						groupFeatures_to_positions[element_in_array[-2]] = index
					elif("Medication" in element_in_array and group_selected == "treatment"):
						groupFeatures_to_positions[element_in_array[-2]] = index					
					index += 1
			else:
				for element in line_in_array:
					element_in_array = element.split("\\")
					if("Luminex" in element_in_array):
						index_to_keep.append(index)
						header_in_string += str(element)+","
					elif("DISEASE" in element_in_array and not specific_group_selected):
						group_index = index
					elif("CSPHASE" in element_in_array):
						phase_index = index
					index += 1

			if(specific_group_position_selected):
				if(group_position == "start"):
					header_in_string = str(group_name)+","+header_in_string[:-1]
				else:
					header_in_string = header_in_string[:-1]+","+str(group_name)
			else:
				header_in_string = header_in_string[:-1]+","+str(group_name)
			
			header_in_string = header_in_string.replace(" ", "")
			output.write(header_in_string+"\n")

		else:
			index = 0
			line_in_string = ""
			phase = line_in_array[phase_index]

			if(specific_group_selected):
				if(artificial_group_selected):		
					if(group_selected == "medication"):
						group = ""
						for med in groupFeatures_to_positions.keys():
							if(line_in_array[groupFeatures_to_positions[med]] == "\"Yes\""):
								group += str(med)+";"
						group = group[:-1]
						if(group == ""):
							group = "control"
					elif(group_selected == "treatment"):
						group = "control"
						for med in groupFeatures_to_positions.keys():
							if(line_in_array[groupFeatures_to_positions[med]] == "\"Yes\""):
								group = "treated"
				else:
					group = line_in_array[group_index]
			else:
				group = line_in_array[group_index]
				if(group == ""):
					group = "control"
			
			for element in line_in_array:
				if(index in index_to_keep):
					line_in_string += str(element)+","
				index += 1

			if(specific_group_position_selected):
				if(group_position == "start"):
					line_in_string = str(group)+","+line_in_string[:-1]
				else:
					line_in_string = line_in_string[:-1]+","+str(group)
			else:
				line_in_string = line_in_string[:-1]+","+str(group)
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



def generate_Flow_data_file(input_data_file, **optional_args):
	"""
	=> Create a csv file with only the Flow cytometry Variables
	and the diagnostic

	- input_data_file is the name of the input data file
	- optional_args contains the optional parameters, such as:
		- "phase": The selected phase, could be:
			- "all" -> get all patients
			- "I" -> get only phase I patients
			- "II" -> get only phase II patients
		- "group": by defaut the selected group is disease,
		   but this parameter can accept:
		   - "medication" -> list of medication applied to the patient (sep by ";")
		   - "treatment" -> treated if patient have any medication, else control.
		- "group_pos": the position of the group in the generated file, defaut is the last column
		  of the new file. could be:
			-"start" -> first column
			-"end" -> last column
		- "group_name": the name of the group column
	"""
	## preprocessing input file
	biotoolbox.change_file_format(input_data_file, ",")
	data_reformated_file = input_data_file.split(".")
	data_reformated_file = data_reformated_file[0]+"_reformated.csv"

	## Looking for optional arguments
	specific_phase_selected = False
	specific_group_selected = False
	artificial_group_selected = False
	specific_group_position_selected = False
	specific_group_name_selected = False
	group_name = "Diagnostic" 
	if("phase" in optional_args):
		specific_phase_selected = True
		phase_selected = optional_args['phase']
	if("group" in optional_args):
		specific_group_selected = True
		group_selected = optional_args['group']
		if(group_selected == "medication" or group_selected == "treatment"):
			artificial_group_selected = True
			groupFeatures_to_positions = {}
	if("group_pos" in optional_args):
		specific_group_position_selected = True
		group_position = optional_args["group_pos"]
	if("group_name" in optional_args):
		specific_group_name_selected = True
		group_name = optional_args["group_name"]

	## Extract Flow cytometry Variables, add the Diagnostic
	index_to_keep = []
	group_index = -1
	phase_index = -1
	data = open(data_reformated_file, "r")
	output = open("FlowCytometry_data.csv", "w")
	cmpt = 0
	for line in data:
		line = line.split("\n")
		line = line[0]
		line_in_array = line.split(",")
		group = "poulet" # init the variable
		phase = "choucroute"

		if(cmpt == 0):
			index = 0
			header_in_string = ""

			if(specific_group_selected):
				for element in line_in_array:
					element_in_array = element.split("\\")
					if("Flowcytometry" in element_in_array):
						index_to_keep.append(index)
						header_in_string += str(element)+","
					elif("CSPHASE" in element_in_array):
						phase_index = index
					elif("DISEASE" in element_in_array and group_selected == "diagnostic"):
						group_index = index					
					elif("SEX" in element_in_array and group_selected == "sex"):
						group_index = index
					elif("Medication" in element_in_array and group_selected == "medication"):
						groupFeatures_to_positions[element_in_array[-2]] = index
					elif("Medication" in element_in_array and group_selected == "treatment"):
						groupFeatures_to_positions[element_in_array[-2]] = index					
					index += 1

			else:
				for element in line_in_array:
					element_in_array = element.split("\\")
					if("Luminex" in element_in_array):
						index_to_keep.append(index)
						header_in_string += str(element)+","
					elif("DISEASE" in element_in_array and not specific_group_selected):
						group_index = index
					elif("CSPHASE" in element_in_array):
						phase_index = index
					index += 1

			if(specific_group_position_selected):
				if(group_position == "start"):
					header_in_string = str(group_name)+","+header_in_string[:-1]
				else:
					header_in_string = header_in_string[:-1]+","+str(group_name)
			else:
				header_in_string = header_in_string[:-1]+","+str(group_name)

			header_in_string = header_in_string.replace(" ", "")
			output.write(header_in_string+"\n")

		else:
			index = 0
			line_in_string = ""
			phase = line_in_array[phase_index]
			if(specific_group_selected):
				if(artificial_group_selected):		
					if(group_selected == "medication"):
						group = ""
						for med in groupFeatures_to_positions.keys():
							if(line_in_array[groupFeatures_to_positions[med]] == "\"Yes\""):
								group += str(med)+";"
						group = group[:-1]
						if(group == ""):
							group = "control"
					elif(group_selected == "treatment"):
						group = "control"
						for med in groupFeatures_to_positions.keys():
							if(line_in_array[groupFeatures_to_positions[med]] == "\"Yes\""):
								group = "treated"
				else:
					group = line_in_array[group_index]
			else:
				group = line_in_array[group_index]
				if(group == ""):
					group = "control"
			
			for element in line_in_array:
				if(index in index_to_keep):
					line_in_string += str(element)+","
				index += 1

			if(specific_group_position_selected):
				if(group_position == "start"):
					line_in_string = str(group)+","+line_in_string[:-1]
				else:
					line_in_string = line_in_string[:-1]+","+str(group)
			else:
				line_in_string = line_in_string[:-1]+","+str(group)
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

