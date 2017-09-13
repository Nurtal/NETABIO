## Feature Selection functions
##

import os
import platform
import glob

from netabio import CORRELATIONMATRIX_SCRIPT
from netabio import ATTRIBUTEIMPORTANCE_SCRIPT
from netabio import RFE_SCRIPT 

def run_analyser(input_data, output_folder, analysis):
	"""
	-> Run a R script wich perform a few analysis for feature selection
	-> input_data is the absolute path to the data file, must be a csv file
	   where the label attribute is at the first column under the
	   term "Disease" (something to fix)
	-> output_folder is the absolute path of the output folder
	-> analysis is a string, the type of analysis to perform, could be:
		- "covarianceMatrix"
		- "attributeImportance"
		- "RFE"
		- "all" (perform all 3 analysis)

	-> exemple of use:
		run_analyser("/home/foulquier/Bureau/SpellCraft/WorkSpace/TRASH/data3.csv", "/home/foulquier/Bureau/SpellCraft/WorkSpace/TRASH/", "RFE")
	"""

	## Check & adapat path to the os
	if(platform.system() == "Linux"):
		output_folder = output_folder.replace("\\", "/")
		input_data = input_data.replace("\\", "/")
		if(output_folder[-1] != "/"):
			output_folder += "/"
	elif(platform.system() == "Windows"):
		output_folder = output_folder.replace("/", "\\")
		input_data = input_data.replace("/", "\\")
		if(output_folder[-1] != "\\"):
			output_folder += "\\"

	## Check if the output folder exist
	valid_output = False
	if(os.path.isdir(output_folder)):
		valid_output = True	

	## Check if the input file exist
	valid_input = False
	if(os.path.isfile(input_data)):
		valid_input = True

	## Get path to R script
	#correlationMatrix_script = get_script_path('fs_correlation_matrix_analysis.R')
	#attributeImportance_script = get_script_path('fs_attribute_importance_evaluation.R')
	#RFE_script = get_script_path('fs_RFE_analysis.R')

	## Run the R script
	if(valid_output and valid_input):
		if(analysis == "covarianceMatrix"):
			#os.system("Rscript scripts/fs_correlation_matrix_analysis.R "+str(input_data)+" "+str(output_folder))
			os.system("Rscript "+CORRELATIONMATRIX_SCRIPT+" "+str(input_data)+" "+str(output_folder))
		elif(analysis == "attributeImportance"):
			#os.system("Rscript scripts/fs_attribute_importance_evaluation.R "+str(input_data)+" "+str(output_folder))
			os.system("Rscript "+ATTRIBUTEIMPORTANCE_SCRIPT+" "+str(input_data)+" "+str(output_folder))
		elif(analysis == "RFE"):
			#os.system("Rscript scripts/fs_RFE_analysis.R "+str(input_data)+" "+str(output_folder))
			os.system("Rscript "+RFE_SCRIPT+" "+str(input_data)+" "+str(output_folder))
		elif(analysis == "all"):
			#os.system("Rscript scripts/fs_correlation_matrix_analysis.R "+str(input_data)+" "+str(output_folder))
			#os.system("Rscript scripts/fs_attribute_importance_evaluation.R "+str(input_data)+" "+str(output_folder))
			#os.system("Rscript scripts/fs_RFE_analysis.R "+str(input_data)+" "+str(output_folder))

			os.system("Rscript "+CORRELATIONMATRIX_SCRIPT+" "+str(input_data)+" "+str(output_folder))
			os.system("Rscript "+ATTRIBUTEIMPORTANCE_SCRIPT+" "+str(input_data)+" "+str(output_folder))
			os.system("Rscript "+RFE_SCRIPT+" "+str(input_data)+" "+str(output_folder))


	elif(not valid_output):
		print "[ERROR] => Can't find the output folder "+str(output_folder)
	elif(not valid_input):
		print "[ERROR] => Can't find the input file "+str(input_data)



def write_html_report(report_file, data_file, result_folder):
	"""
	-> Write a html report for the features selection
	-> report_file is the name of the html file generate by the function
	-> data_file is the input data file used for feature selection
	-> result_folder is the folder where reults file from feature selection
	   procedure are stored.
	-> This function need the following files in the result_folder:
		- attribute_importance.csv
		- attribute_importance.png"
		- correlationMatrix.csv"
		- high_correlation.txt"
		- RFE_results.csv"
		- RFE_selected_attributes.csv"
		- variance_analysis.csv"
		- RFE_accuracy.png"
		All results files are generated by the run_analyser() function
	"""

	## Check if data_file exist
	valid_data_file = False
	if(os.path.isfile(data_file)):
		valid_data_file = True

	## Check if result_folder exist
	valid_result_folder = False
	if(os.path.isdir(result_folder)):
		valid_result_folder = True

	## Check if all results file are present to write the report
	## and init the file name variable
	all_results_file_present = True
	missing_files = []
	separator = "/"
	if(platform.system() == "Windows"):
		separator = "\\"
	list_of_results_file = ["attribute_importance.csv", "attribute_importance.png", "correlationMatrix.csv", "high_correlation.txt", "RFE_results.csv", "RFE_selected_attributes.csv", "variance_analysis.csv", "RFE_accuracy.png"]
	if(valid_result_folder):
		if(result_folder[-1] == str(separator)):
			files_in_results_directory = glob.glob(result_folder+"*")

			## init the file name variable
			correlationMatrix_file = result_folder+"correlationMatrix.csv"
			high_correlation_file = result_folder+"high_correlation.txt"
			variance_analysis_file = result_folder+"variance_analysis.csv"
			attribute_importance_file = result_folder+"attribute_importance.csv"
			attribute_importance_image = result_folder+"attribute_importance.png"
			RFE_results_file = result_folder+"RFE_results.csv"
			RFE_selected_attributes = result_folder+"RFE_selected_attributes.csv"
			RFE_image = result_folder+"RFE_accuracy.png"

		else:
			files_in_results_directory = glob.glob(result_folder+separator+"*")

			## init the file name variable
			correlationMatrix_file = result_folder+separator+"correlationMatrix.csv"
			high_correlation_file = result_folder+separator+"high_correlation.txt"
			variance_analysis_file = result_folder+separator+"variance_analysis.csv"
			attribute_importance_file = result_folder+separator+"attribute_importance.csv"
			attribute_importance_image = result_folder+separator+"attribute_importance.png"
			RFE_results_file = result_folder+separator+"RFE_results.csv"
			RFE_selected_attributes = result_folder+separator+"RFE_selected_attributes.csv"
			RFE_image = result_folder+separator+"RFE_accuracy.png"

		for f in list_of_results_file:
			if(result_folder[-1] == separator):
				file_to_test = result_folder+f
			else:
				file_to_test = result_folder+separator+f
			if(file_to_test not in files_in_results_directory):
				all_results_file_present = False
				missing_files.append(f)

	## Write the Report
	if(valid_result_folder and valid_data_file and all_results_file_present):

		report = open(report_file, "w")

		report.write("<html>\n")
		report.write("<title>NETABIO</title>\n")
		report.write("<h2>Features Selection Report</h2>\n")

		##----------------------------##
		## Work on correlation matrix ##
		##----------------------------##
		report.write("<h3>Correlation Matrix</h3>\n")
		index_to_label = {}
		data = open(correlationMatrix_file, "r")
		cmpt = 0
		for line in data:
			line = line.replace("\n", "")
			line_in_array = line.split(",")
			if(cmpt == 0 and line_in_array[0] == "\"\""):
				line_in_array = line_in_array[1:] # Remove stupid R stuff
			index_to_label[cmpt] = line_in_array[0]
			cmpt += 1
		data.close()

		variable_to_remove = []
		data = open(high_correlation_file, "r")
		for line in data:
			line = line.replace("\n", "")
			line_in_array = line.split(" ")

			if(line_in_array[0] == "Compare"):
				line_in_array[2] = str(line_in_array[2])+" ("+str(index_to_label[int(line_in_array[2])])+") "
				line_in_array[7] = str(line_in_array[7])+" ("+str(index_to_label[int(line_in_array[7])])+") "
				line_in_string = ""
				for elt in line_in_array:
					line_in_string += str(elt) + " "
				line_in_string = line_in_string[:-1]
				report.write(line_in_string+"<br>\n")
			elif("flagging" in line_in_array):
				variable_to_remove.append(index_to_label[int(line_in_array[-2])])
				line_in_array[-2] = str(line_in_array[-2])+" ("+str(index_to_label[int(line_in_array[-2])])+") "
				line_in_string = "<dd>"
				for elt in line_in_array:
					line_in_string += str(elt) + " "
				line_in_string = line_in_string[:-1]
				report.write(line_in_string+"<br>\n")
		data.close()

		report.write("<p> Recommand to remove the following (redundant) variables:<p>\n")
		report.write("<ul>\n")
		for var in variable_to_remove:
			report.write("<li>"+str(var)+"</li>\n")
		report.write("</ul>\n")

		##------------------##
		## Work on Variance ##
		##------------------##
		report.write("<h3>Variance and features</h3>\n")
		variable_to_remove = []
		data = open(variance_analysis_file, "r")
		cmpt = 0
		for line in data:
			line = line.replace("\n", "")
			line_in_array = line.split(",")
			if("TRUE" in line_in_array and cmpt > 0):
				variable_to_remove.append(line_in_array[0])
			cmpt += 1
		data.close()

		if(len(variable_to_remove) > 0):
			report.write("<p> Recommand to remove the following (variance near zero) variables:<p>\n")
			report.write("<ul>\n")
			for var in variable_to_remove:
				report.write("<li>"+str(var)+"</li>\n")
			report.write("</ul>\n")
		else:
			report.write("<p>No variable found with variance near zero<p>\n")

		##------------------------------##
		## Work on attribute importance ##
		##------------------------------##
		## table with the 10 most important attributes
		report.write("<h3>Attribute importance</h3>\n")
		data = open(attribute_importance_file, "r")
		cmpt = 0
		report.write("<table>\n")
		for line in data:
			line = line.replace("\n", "")
			line_in_array = line.split(",")
			report.write("<tr>\n")
			for elt in line_in_array:
				elt = elt.replace("\"", "")
				if(cmpt == 0):
					report.write("<th>"+str(elt)+"</th>\n")
				elif(cmpt <= 10):
					report.write("<td>"+str(elt)+"</td>\n")
			report.write("</tr>\n")
			cmpt += 1
		data.close()
		report.write("</table>\n")

		## Display graphic
		report.write("<img src="+attribute_importance_image+" style=\"width:600px;height:400px;\">\n")

		##-------------##
		## Work on RFE ##
		##-------------##
		report.write("<h3>Recursive Feature Elimination (RFE)</h3>\n")

		## display graphic
		report.write("<img src="+RFE_image+" style=\"width:600px;height:400px;\">\n")
		
		## Selected features
		selected_features = []
		data = open(RFE_selected_attributes, "r")
		cmpt = 0
		for line in data:
			line = line.replace("\n", "")
			line_in_array = line.split(",")
			if(cmpt > 0):
				feature = line_in_array[1].replace("\"", "")
				selected_features.append(feature)
			cmpt += 1
		data.close()

		if(len(selected_features) > 0):
			report.write("<p> Selected features:</p>\n")
			report.write("<ul>\n")
			for var in selected_features:
				report.write("<li>"+str(var)+"</li>\n")
			report.write("</ul>\n")
		else:
			report.write("<p> No features selected</p>\n")


		report.write("</html>\n")
		report.close()
	elif(not valid_result_folder):
		print "[ERROR] => Can't find the output folder "+str(result_folder)
	elif(not valid_data_file):
		print "[ERROR] => Can't find the input file "+str(data_file)
	elif(not all_results_file_present):
		print "[ERROR] => following files are missing in "+str(result_folder)+":"
		for f in missing_files:
			print "\t-> "+str(f)





## TEST SPACE
"""
report_file = "/home/foulquier/Bureau/SpellCraft/WorkSpace/TRASH/test.html"
data_file = "/home/foulquier/Bureau/SpellCraft/WorkSpace/TRASH/data3.csv"
result_folder = "/home/foulquier/Bureau/SpellCraft/WorkSpace/TRASH"
"""
"""
report_file = "C:\\Users\\NaturalKiller01\\Desktop\\Nathan\\Spellcraft\\TRASH\\report.html"
#data_file = "C:\\Users\\NaturalKiller01\\Desktop\\Nathan\\Spellcraft\\Luminex_data_NA_filtered.csv"
data_file = "C:\\Users\\NaturalKiller01\\Desktop\\Nathan\\Spellcraft\\SideQuest\\Bene\\newCytoData.csv"
result_folder = "C:\\Users\\NaturalKiller01\\Desktop\\Nathan\\Spellcraft\\TRASH"


run_analyser(data_file, result_folder, "all")
write_html_report(report_file, data_file, result_folder)
"""