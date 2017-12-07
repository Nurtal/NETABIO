##
## Quality control
##


import biotoolbox
import operator
import numpy as np
from scipy import stats


def check_pourcentages(value):
	"""
	-> Check if the value is a pourcentage
	-> Check if the pourcentage is credible
	-> Return true if it detect an invalid percentage, else False
		- Return False doesn't mean there all is good, just that
		  no alert was triggered.
	"""

	value_status = "undef"
	alert = False

	if(value != ""):
		if(value[-1] == "%"):
			value_to_test = value.replace("%", "")
			value_to_test = value_to_test.replace(",", ".")
			try:
				value_to_test = float(value_to_test)
				if(value_to_test >= 0 and value_to_test <= 100):
					value_status = "valid percentage"
				else:
					value_status = "invalid percentage"
					alert = True
			except:
				value_status = "not a numerical value"

		return alert



def looking_for_outliers(input_vector, col_number):
	"""
	-> Flag outlier in the input_vector, return list of patients
	   containing outliers
	TODO : deal with int vector (no replace attribute)
	"""

	## init structure de retour
	flag_patients= []
	number_of_tolerated_std = 5
	zscore_limit = 3

	## clean vector
	clean_vector = []
	index_in_clean_vector_to_patient = {}
	patient = 0
	index = 0
	for scalar in input_vector:
		scalar = scalar.replace("%", "")
		scalar = scalar.replace(" ", "")
		try:
			scalar = float(scalar)
			clean_vector.append(scalar)
			index_in_clean_vector_to_patient[index] = patient
			index += 1
		except:
			do_nothing = 1
		
		patient += 1

	## -> flag values distant from the median
	clean_vector = np.array(clean_vector)
	zscores = stats.zscore(clean_vector)

	index = 0
	for scalar in clean_vector:

		## -> compute the median
		## and standard deviation
		med = np.median(clean_vector)
		ecart_type = np.std(clean_vector)

		## Using Z-score
		if(float(abs(zscores[index])) >= zscore_limit):
			flag_patients.append(index_in_clean_vector_to_patient[index])

		## old method
		#if(float(abs(scalar)) >= float(med+(number_of_tolerated_std*ecart_type)) or float(abs(scalar)) <= float(med-(number_of_tolerated_std*ecart_type))):
		#	flag_patients.append(index_in_clean_vector_to_patient[index])

		index+= 1

	return flag_patients



def basic_check(data_file):
	"""
	-> Check a few things in data_file
		-> try to detect the best separator for the file
		-> make sure all lines are of the same lenght
		-> Looking for missing values (count and flag the concerning lines)
		-> Check percentages values, make sure there are between 0 and 100
		-> Try to detect a header
		-> Check column composition (containing digit or strings, flag mixt columns
		   and give the number of the concerning lines).
		-> Look for outliers, flag concerning lines.
	-> Display and write results in a log file (current directory)
	"""


	## Init variables
	number_of_lines = -1
	number_of_columns = -1
	separator = -1
	header_detected = -1

	## Init log file
	log_file = open("log.txt", "w")

	##---------------------------------------##
	## Detect the best separator in file.    ##
	## Detect problem of not enough lines &  ##
	## differences in lenght of lines        ##
	##---------------------------------------##
	separator = biotoolbox.detect_file_format(data_file)

	if(separator == "not_enough_line"):
		print "[WARNING] => Very few lines in file (Less than 2)"
		log_file.write("[WARNING] => Very few lines in file (Less than 2)\n")
	elif("Difference in lenght of lines" in separator):
		
		## get best separator
		separator = separator.split("<sep>") # not sure what is it about

		if(len(separator) > 1):
			separator = separator[1]
			print "[ERROR] => Difference in lenght of lines"
			log_file.write("[ERROR] => Difference in lenght of lines\n")
		else:
			separator = "undef"
			print "[ERROR] => Difference in lenght of lines"
			log_file.write("[ERROR] => Difference in lenght of lines\n")

		## check each lenght of line
		len_of_lines = {}
		number_of_lines_of_lenght = {}
		cmpt = 0
		input_data = open(data_file, "r")
		for line in input_data:
			line = line.replace("\n", "")
			line_in_array = line.split(separator)
			len_of_lines[cmpt] = len(line_in_array)
			if(len(line_in_array) in number_of_lines_of_lenght.keys()):
				number_of_lines_of_lenght[len(line_in_array)] += 1
			else:
				number_of_lines_of_lenght[len(line_in_array)] = 1
			cmpt += 1
		input_data.close()

		## write logs
		for key in len_of_lines.keys():
			log_file.write("[ERROR] => Line "+str(key)+" contain "+str(len_of_lines[key])+" values\n")
		for key in number_of_lines_of_lenght.keys():
			log_file.write("[ERROR] => "+str(number_of_lines_of_lenght[key])+" lines with "+str(key)+" values\n")

	else:
		##--------------------------------------------------------##
		## Find good separator,                                   ##
		## Pas de problemes apparent avec la taille des lignes    ##
		## Ecriture des logs                                      ##
		##--------------------------------------------------------##
		print "[PASS] => Same lenght for each lines"
		log_file.write("[PASS] => Same lenght for each lines\n")
		log_file.write("[PASS] => exact separator found : "+str(separator)+"\n")

		## Check numbers of lines & columns
		input_data = open(data_file, "r")
		cmpt = 0
		for line in input_data:
			line_in_array = line.split(separator)
			number_of_columns = len(line_in_array)
			cmpt += 1
		number_of_lines = cmpt
		input_data.close()

		## Ecriture des logs
		print "[PASS] => Found "+str(number_of_lines) +" lines"
		print "[PASS] => Found "+str(number_of_columns) +" columns"
		log_file.write("[PASS] => Found "+str(number_of_lines) +" lines\n")
		log_file.write("[PASS] => Found "+str(number_of_columns) +" columns\n")

		##----------------------------##
		## Looking for missing values ##
		##----------------------------##

		lines_containing_missing_values = []
		input_data = open(data_file, "r")
		cmpt = 0
		for line in input_data:
			line = line.replace("\n", "")
			line_in_array = line.split(separator)

			index = 0
			for scalar in line_in_array:
				if(scalar == "NA" or scalar == "" or scalar == " "):
					if(cmpt not in lines_containing_missing_values):
						lines_containing_missing_values.append(cmpt)
			cmpt += 1
		input_data.close()

		## Write the logs & display the information
		if(len(lines_containing_missing_values) > 0):
			print "[WARNING] => "+str(len(lines_containing_missing_values))+ " lines with missing values"
			log_file.write("[WARNING] => "+str(len(lines_containing_missing_values))+ " lines with missing values\n")
		for line in lines_containing_missing_values:
			print "[WARNING] => line "+str(line)+ " contains NA values"
			log_file.write("[WARNING] => line "+str(line)+ " contains NA values\n")


		##-------------------##
		## Check percentages ##
		##-------------------##

		input_data = open(data_file, "r")
		cmpt = 0
		for line in input_data:
			line = line.replace("\n", "")
			line_in_array = line.split(separator)
			
			index = 0
			for scalar in line_in_array:
				strange_percentage = check_pourcentages(scalar)
				if(strange_percentage):
					print "[WARNING] => line "+str(cmpt)+ ", column "+str(index)+" : invalid percentage"
					log_file.write("[WARNING] => line "+str(cmpt)+ ", column "+str(index)+" : invalid percentage\n")
				index += 1
			cmpt += 1
		input_data.close()


		##-----------------------------------##
		## Look for the presence of a header ##
		##-----------------------------------##


		missing_values_in_first_line = False

		input_data = open(data_file, "r")
		cmpt = 0
		data_profile = []
		for line in input_data:
			line = line.replace("\n", "")
			line_in_array = line.split(separator)
			if(cmpt == 0):
				
				header_profile = []
				index = 0
				for scalar in line_in_array:
					value_type = "undef"

					## Try to convert value to a digit
					scalar = scalar.replace(",", ".")
					scalar = scalar.replace("%", "")
					scalar = scalar.replace(" ", "")

					## The simple case
					if(scalar != "NA" and scalar != ""):
						try:
							float(scalar)
							value_type = "digit"
						except:
							value_type = "string"
						header_profile.append(value_type)

			else:
				line_profile = []
				index = 0
				for scalar in line_in_array:
					value_type = "undef"

					## Try to convert value to a digit
					scalar = scalar.replace(",", ".")
					scalar = scalar.replace("%", "")
					scalar = scalar.replace(" ", "")

					## The simple case
					if(scalar != "NA" and scalar != ""):
						try:
							float(scalar)
							value_type = "digit"
						except:
							value_type = "string"
						line_profile.append(value_type)
				data_profile.append(line_profile)
			cmpt += 1
		input_data.close()

		## loop over line profile
		## identify the "delault" profile
		## for a line
		profile_to_occurence = {}
		for profile in data_profile:
			profile_in_string = ""
			for elt in profile:
				profile_in_string += str(elt)+"_"
			profile_in_string = profile_in_string[:-1]
			if(profile_in_string not in profile_to_occurence.keys()):
				profile_to_occurence[profile_in_string] = 1
			else:
				profile_to_occurence[profile_in_string] += 1

		## delete all profile including NA values (len lower than the header len)
		## check if he header contain missing values (i.e a line as a profile greater than
		## the header ) -> flag it, probably not a header in this case
		list_of_key_to_delete = []
		for key in profile_to_occurence.keys():
			key_in_array = key.split("_")
			if(len(key_in_array) < len(header_profile)):
				list_of_key_to_delete.append(key)
			elif(len(key_in_array) > len(header_profile)):
				missing_values_in_first_line = True
		for key in list_of_key_to_delete:
			del profile_to_occurence[key]

		## select the profile that have the max occurence
		## check that profile_to_occurence is not empty
		if(bool(profile_to_occurence)):
			global_profile = max(profile_to_occurence.iteritems(), key=operator.itemgetter(1))[0]
			global_profile = global_profile.split("_")
		else:
			global_profile = "undef"

		## compare to the header profile
		if(global_profile == header_profile):
			## Does not seems to have any header in the file
			## check if there is only string in the global profile
			if("digit" in global_profile):
				## Almost positive there is no header
				print "[PASS] => No header detected"
				log_file.write("[PASS] => No header detected\n")
				header_detected = False
			else:
				## More tricky, means that we encounter only string
				## in most of lines, hard to discriminate between the first line
				## and the rest
				print "[WARNING] => No header detected, low confidence"
				log_file.write("[WARNING] => No header detected, low confidence\n")
		else:
			## Probably a header
			print "[PASS] => Header detected"
			log_file.write("[PASS] => Header detected\n")
			header_detected = True

		if(missing_values_in_first_line):
			## Probably no header
			print "[PASS] => No header detected"
			log_file.write("[PASS] => No header detected\n")
			header_detected = False


		##-------------------------------------------------##
		## Check column composition                        ##
		## Make sure all values has the same type for each ##
		## variables                                       ##
		##-------------------------------------------------##

		## init structure
		variable_to_values = {}
		variable_to_types = {}
		column_to_type = {}
		for x in xrange(0, number_of_columns):
			variable_to_values[x] = []

		## fill the structure
		input_data = open(data_file, "r")
		cmpt = 0
		for line in input_data:

			## deal with header
			if(not (header_detected and cmpt == 0)):
				line = line.replace("\n", "")
				line_in_array = line.split(separator)
				index = 0
				for scalar in line_in_array:
					variable_to_values[index].append(scalar)
					index += 1
			cmpt += 1
		input_data.close()

		## look for each value in each variable
		for key in variable_to_values.keys():
			values_type = []
			for value in variable_to_values[key]:
				value_type = "undef"

				## Try to convert value to a digit
				value = value.replace(",", ".")
				value = value.replace("%", "")
				value = value.replace(" ", "")

				## The simple case
				if(value != "NA" and value != ""):
					try:
						float(value)
						value_type = "digit"
					except:
						value_type = "string"
					values_type.append(value_type)
			
			digit_count = 0
			string_count = 0

			for value_type in values_type:
				if(value_type == "digit"):
					digit_count += 1
				elif(value_type == "string"):
					string_count += 1

			if(digit_count > string_count):
				if(string_count == 0):
					## nothing strange, it's a column full of digit
					## (minus evntually the NA variables)
					column_to_type[key] = "digit"
				else:
					## Problem, digit and strngs in the same column
					## but still more digit
					column_to_type[key] = "digit"
					print "[ERROR] => find string in a digit column : column "+str(key)
					log_file.write("[ERROR] => string found in a digit column : column "+str(key)+"\n")

			else:
				if(digit_count == 0):
					## nothing strange, it's a column full of strings
					## (minus evntually the NA variables)
					column_to_type[key] = "string"

				else:
					## Problem, digit and strngs in the same column
					## but still more or equal strings
					column_to_type[key] = "string"
					print "[ERROR] => find digit in a string column : column "+str(key)
					log_file.write("[ERROR] => digit found in a string column : column "+str(key)+"\n")
						

		##---------------------##
		## Looking for outlier ##
		##---------------------##

		flag_patients = []

		for key in variable_to_values.keys():
			vector = variable_to_values[key]
			if(column_to_type[key] == "digit"):
				flag_patient_in_vector = looking_for_outliers(vector, key)
				for patient in flag_patient_in_vector:
					print "[WARNINGS] => outlier detected, flag line "+str(patient)+" in column "+str(key)
					log_file.write("[WARNINGS] => outlier detected, flag line "+str(patient)+" in column "+str(key)+"\n")
		

		##---------------##
		## Check Z-score ##
		##---------------##

		flag_variables = []

		
		variable_to_zscore_mean = check_zscore(data_file, separator, header_detected)
		for var in variable_to_zscore_mean.keys():
			if(variable_to_zscore_mean[var] != "NA"):
				if(variable_to_zscore_mean[var] >= 2 or variable_to_zscore_mean[var] <= -2):
					print "[WARNINGS] => Strange distribution detected, flag variable: "+str(var)
					log_file.write("[WARNINGS] => Strange distribution detected, flag variable: "+str(var)+"\n")


		





	## Close log file
	log_file.close()







def consistency_check(data_file):
	"""
	[IN PROGRESS]
	"""

	print "choucroute"



def check_standard_deviation(data_file_name):
	##
	## -> Check the standard deviation for each variables
	## in data_file_name.
	## -> Return a dict variable to standard deviation
	##

	position_to_variable = {}
	variable_to_distribution = {}
	variable_to_standard_deviation = {}

	## add scalar to distribution for each variables
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
				variable_to_distribution[variable] = []
				variable_to_standard_deviation[variable] = "NA"
				index +=1
		else:
			index = 0
			for scalar in line_in_array:

				try:
					scalar = scalar.replace("\"", "")
					scalar_to_add = float(scalar)
					variable_to_distribution[position_to_variable[index]].append(scalar_to_add)
				except:
					scalar_to_add = "undef"				

				index+=1

		cmpt += 1
	input_data.close()


	## Compute the standard deviation
	for key in variable_to_distribution.keys():
		distribution = variable_to_distribution[key]
		distribution = np.array(distribution)
		if(len(distribution) > 1):
			variable_to_standard_deviation[key] = np.std(distribution)
		else:
			variable_to_standard_deviation[key] = "NA" 

	## return dict
	return variable_to_standard_deviation



def check_zscore(data_file_name, separator, header_detected):
	##
	## -> Compute the zscore mean for each variables in 
	## data_file_name.
	## -> Return mean of the zscore for each variable
	##

	position_to_variable = {}
	variable_to_distribution = {}
	variable_to_zscore_mean = {}

	## add scalar to distribution for each variables
	## in data file.
	cmpt = 0
	input_data = open(data_file_name, "r")
	for line in input_data:
		line = line.split("\n")
		line = line[0]
		line_in_array = line.split(separator)
		

		if(cmpt == 0):
			index = 0
			for variable in line_in_array:
				
				if(header_detected):
					position_to_variable[index] = variable
					variable_to_distribution[variable] = []
					variable_to_zscore_mean[variable] = "NA"
				else:
					position_to_variable[index] = index
					variable_to_distribution[index] = []
					variable_to_zscore_mean[index] = "NA"
				
				index +=1

		else:
			index = 0
			for scalar in line_in_array:

				try:
					scalar = scalar.replace("\"", "")
					scalar_to_add = float(scalar)
					variable_to_distribution[position_to_variable[index]].append(scalar_to_add)
				except:
					scalar_to_add = "undef"				

				index+=1

		cmpt += 1
	input_data.close()


	## Compute the standard deviation
	for key in variable_to_distribution.keys():
		distribution = variable_to_distribution[key]
		distribution = np.array(distribution)
		if(len(distribution) > 1):
			zscores = stats.zscore(distribution)
			variable_to_zscore_mean[key] = np.mean(zscores)
		else:
			variable_to_zscore_mean[key] = "NA" 

	## return dict
	return variable_to_zscore_mean







## TEST SPACE ##

#basic_check("test.txt")