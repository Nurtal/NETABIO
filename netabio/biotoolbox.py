"""
A few functions to manage
data files in biology
"""

import shutil
import subprocess
import os.path
import platform
import os
import glob
from difflib import SequenceMatcher


def detect_file_format(data_file_name):
	"""
	Because in biology, you always need to check
	if a csv file is a real csv file ...
	
	-> Should return the separator used in
	data file.
	"""

	## A few parameters
	can_analyse_file = False
	separator_list = [",", ";", "\t"]
	separator_to_count = {}
	best_separator = "undef"

	## Count the Number of line in the file
	data_file = open(str(data_file_name), "r")
	cmpt_line = 0
	for line in data_file:
		line = line.split("\n")
		line = line[0]
		cmpt_line += 1
	data_file.close()

	## Test if we can do something with it
	if(cmpt_line > 1):
		can_analyse_file = True
	else:
		best_separator = "not_enough_line"

	## Run the analysis if we can
	if(can_analyse_file):


		## Initialize the separator_to_count variable:
		for separator in separator_list:
			separator_to_count[separator] = []

		## Re-open the file and parse the lines
		data_file = open(str(data_file_name), "r")
		for line in data_file:
			line = line.split("\n")
			line = line[0]

			## Split line with a few separator
			for separator in separator_list:
				line_in_array = line.split(separator)
				separator_to_count[separator].append(len(line_in_array))


		data_file.close()


		## Perform the analysis
		perfect_separator_found = False
		for separator in separator_to_count.keys():

			## Separate data and header size
			## Because biologists ... well, you know why.
			header_size = separator_to_count[separator][0]
			data_size = separator_to_count[separator][1:]

			max_size = max(data_size)
			min_size = min(data_size)

			## Perform the test
			if(max_size != 1 and max_size == min_size):
				 best_separator = separator
				 perfect_separator_found = True

			elif(max_size != 1 and max_size != min_size and not perfect_separator_found):
				best_separator = "Difference in lenght of lines"

		## return the best separator found
		return best_separator


	## Exit The programm with a warning message
	else:
		print "[!] Can't run an analysis\n"
		return best_separator





def change_file_format(data_file_name, separator):
	"""
	-> Change the separator used in data_file_name, to separator
	-> Delete spaces in lines if space is not the separator 
	"""

	## Define the extension
	extension = "_reformated.tmp"
	if(separator == ","):
		extension = "_reformated.csv"
	elif(separator == "\t"):
		extension = "_reformated.tsv"

	## Get current separator
	current_separator = detect_file_format(data_file_name)
	if(current_separator != "undef"):
		
		## Re-write file with new separator
		output_file_name = data_file_name.split(".")
		output_file_name = output_file_name[0]
		output_file_name = str(output_file_name)+extension
		input_data_file = open(data_file_name, "r")
		output_data_file = open(output_file_name, "w")
		for line in input_data_file:
			line_to_write = line.replace(current_separator, separator)
			if(separator != " "):
				line_to_write = line_to_write.replace(" ", "")
			output_data_file.write(line_to_write)
		output_data_file.close()
		input_data_file.close()

		# Exit The programm with a validation message
		print "[*] File "+str(data_file_name)+" have been formated, from "+str(current_separator)+ " To "+str(separator)+" separator"

	## Exit The programm with a warning message
	else:
		print "[!] Can't determine the separator used in "+str(data_file_name)+", can't reformat file"




def fix_file_name(input_file):
	"""
	-> for all the spaces and dots in
	   the wild biology file name ...
	-> Deal with path on Windows and Linux, treat onlu the file name
	-> convert dots and spaces in file
	-> copy the input_file with to a file with a valid file name
	"""

	## Make sure the file exist
	if(os.path.exists(input_file)):

		## Separate file name from file path
		input_file_path = ""
		folder_separator = "/"
		if(platform.system() == "Windows"):
			folder_separator = "\\"
		elif(platform.system == "Linux"):
			folder_separator = "/"
		
		input_file_name_path_in_array = input_file.split(folder_separator)
		input_file_name = input_file_name_path_in_array[-1]

		if(len(input_file_name_path_in_array) > 1):
			for folder in input_file_name_path_in_array[:-1]:
				input_file_path += str(folder) + folder_separator

		## Scan for multiple dots in file name
		input_file_name_in_array = input_file_name.split(".")
		output_file_name = ""
		if(len(input_file_name_in_array) > 2):
			
			## Deal with multiple dots in file name
			for element in input_file_name_in_array[:-1]:
				output_file_name += str(element)+"_"
			output_file_name = output_file_name[:-1]

			## get file extension
			file_extension = input_file_name_in_array[-1]

			## replace spaces and dots by underscores
			output_file_name = output_file_name.replace(" ", "_")
			output_file_name = output_file_name.replace(".", "_")

			## init output filename
			output_file_name += "."+str(file_extension)

		elif(len(input_file_name_in_array) == 2):

			## get file extension
			file_extension = input_file_name_in_array[-1]
			
			## init output filename
			output_file_name = input_file_name_in_array[0]
			output_file_name += "."+str(file_extension)

			## replace spaces and dots by underscores
			output_file_name = output_file_name.replace(" ", "_")

		else:
			print "[!] It appears that the input file have no extensions ... "

		## Finalise output file name
		output_file_name = str(input_file_path) + str(output_file_name)
		
		## Check if input file is a valid file name
		## if not copy make a copy of the file with a valid file name.
		if(str(output_file_name) == str(input_file)):
			print "[*] "+str(input_file) +" appears to be a valid file name"
		else:
			print "[*] Create a copy of "+str(input_file) +" \n[~] with the name: "+str(output_file_name)
			shutil.copy(input_file, output_file_name)
	else:
		print "[!] Can't find file "+str(input_file)







def reformat_variables_names(input_file):
	##
	## [IN PROGRESS]
	## 
	## => Check the name of the variables in
	## input files, delete identical part
	## 	- Useful for specific project, use
	##    with caution
	## => Assume the file has a header and separator is a ","
	##

	## parameters
	separator = ","

	## get the variables names
	original_variables = []
	data = open(input_file, "r")
	cmpt = 0
	for line in data:
		line = line.replace("\n", "")
		if(cmpt == 0):
			line_in_array = line.split(separator)
			for variable in line_in_array:
				original_variables.append(variable)
		cmpt += 1
	data.close()

	##----------------##
	## THE SMART PART ##
	##----------------##
	## [WARNING] => not functionnal for now
	## [TODO] => deal with the bugs
	## check for each variable if it share a commun prefix
	## wich another variables
	"""
	new_variables = []
	for variable in original_variables:

		for variable_to_compare in original_variables:
			if(variable != variable_to_compare):
				match = SequenceMatcher(None, variable, variable_to_compare).find_longest_match(0, len(variable), 0, len(variable_to_compare))
				new_variable = variable.replace(str(variable[match.a: match.a + match.size]), "")
		
				if(new_variable not in new_variables):
					new_variables.append(new_variable)
	
	print new_variables
	"""
	##----------------##
	## THE STUPID WAY ##
	##----------------##
	new_variables = []
	new_header = ""
	for variable in original_variables:
		new_var = variable.replace("\\CrossSectional\\LowDimensionalData\\Luminex\\", "")
		new_var = new_var.replace("\\", "")
		new_variables.append(new_var)
		new_header += str(new_var)+","
	new_header = new_header[:-1]+"\n"

	## Rewrite the file
	output_file = open(input_file+".tmp", "w")
	input_data = open(input_file, "r")
	cmpt = 0
	for line in input_data:
		if(cmpt == 0):
			output_file.write(new_header)
		else:
			output_file.write(line)
		cmpt += 1
	input_data.close()
	output_file.close()

	## clean files
	os.remove(input_file)
	shutil.copy(input_file+".tmp", input_file)
	os.remove(input_file+".tmp")




