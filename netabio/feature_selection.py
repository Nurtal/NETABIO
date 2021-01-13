## Feature Selection functions
##

import os
import platform
import glob

from netabio import CORRELATIONMATRIX_SCRIPT
from netabio import ATTRIBUTEIMPORTANCE_SCRIPT
from netabio import RFE_SCRIPT
from netabio import BORUTA_SCRIPT



def run_boruta(input_data, output_folder):
    """
    This function run the Boruta algorithm on the input data
    and save results in the output_folder.
        - input_data is a string, the name (path) of the input data file
        - output_folder is a string, the name (path) of the output folder

    Three parameters can be modify to run the algorithm
        - max_depth, the max depth of trees used in the random forest by
          the Boruta algorithm
        - max_iteration : max iteration for the algorithm
        - verbose : display something (1 or 2) or nothing (0) in the terminal

    Generate 1 file
        - output_folder+"/Boruta_ranking.csv"
    """

    ## importation
    import numpy as np
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from boruta import BorutaPy

    ## parameters
    max_depth = 5
    max_iteration = 100
    verbose = 2

    ## set output file name
    ranking_file_name = output_folder+"/Boruta_ranking.csv"

    ## preprocess data
    df = pd.read_csv(input_data)
    df = df.dropna()
    y = df[['LABEL']]
    X = df.drop(columns=['LABEL'])

    ## extract features
    features = [f for f in X.columns]

    ## prepare dataset
    X = X.values
    Y = y.values.ravel()

    ## setup the RandomForrestClassifier as the estimator to use for Boruta
    rf = RandomForestClassifier(n_jobs=-1, class_weight='balanced', max_depth=max_depth)

    ## run Boruta
    boruta_feature_selector = BorutaPy(
        rf,
        n_estimators='auto',
        verbose=verbose,
        random_state=4242,
        max_iter = max_iteration,
        perc = 90
    )
    boruta_feature_selector.fit(X, Y)

    ## save extracted feature
    output_file = open(ranking_file_name, "w")
    output_file.write("VAR_NAME,SELECTED\n")
    for x in range(0,X.shape[1]):
        var_name = features[x]
        selected = boruta_feature_selector.support_[x]
        output_file.write(str(var_name)+","+str(selected)+"\n")
    output_file.close()



def run_rfe(input_data, output_folder):
    """
    This function run a Recursive feature elimination on the input data
    and save results in the output_folder.
        - input_data is a string, the name (path) of the input data file
        - output_folder is a string, the name (path) of the output folder

    First determine the optimal nb of features throught cross validation using
    a decision tree classifier.
    Then use this optimal nb of feature to run RFE and extract ranking info for
    each feature.

    Generate 3 files
        - output_folder+"/RFE_fig.png"
        - output_folder+"/RFE_ranking.csv"
        - output_folder+"/RFE_nb_features.csv"
    """

    ## importation
    from sklearn.feature_selection import RFE
    from sklearn.tree import DecisionTreeClassifier
    import pandas as pd
    from numpy import mean
    from numpy import std
    from sklearn.datasets import make_classification
    from sklearn.model_selection import cross_val_score
    from sklearn.model_selection import RepeatedStratifiedKFold
    from sklearn.feature_selection import RFECV
    from sklearn.pipeline import Pipeline
    from matplotlib import pyplot as plt

    ## set up fig name
    output_fig_name = output_folder+"/RFE_fig.png"
    ranking_file_name = output_folder+"/RFE_ranking.csv"
    nb_feature_file_name = output_folder+"/RFE_nb_features.csv"

    ## preprocess data
    df = pd.read_csv(input_data)
    df = df.dropna()
    y = df[['LABEL']]
    X = df.drop(columns=['LABEL'])

    ## parameters
    min_nb_feature = 5
    max_nb_feature = X.shape[1]
    results = []
    names = []
    best_score = 0.0
    best_nb_features = -1

    ## explore configurations
    for nb_feature in range(min_nb_feature, max_nb_feature):

        ## create the model
        rfe = RFE(estimator=DecisionTreeClassifier(), n_features_to_select=nb_feature)
        model = DecisionTreeClassifier()

        ## try cross validation
        cv = RepeatedStratifiedKFold(n_splits=3, n_repeats=3, random_state=1)
        scores = cross_val_score(model, X, y, scoring='accuracy', cv=cv, n_jobs=-1, error_score='raise')

        ## update log info
        results.append(scores)
        names.append(nb_feature)

        ## get optimal nb of feature
        if(scores.mean() > best_score):
            best_score = scores.mean()
            best_nb_features = nb_feature

    # plot model performance for comparison
    plt.boxplot(results, labels=names, showmeans=True)
    plt.xticks(rotation='vertical')
    plt.savefig(output_fig_name)
    plt.close()

    ## run RFE with optimal nb_feature
    rfe = RFE(estimator=DecisionTreeClassifier(), n_features_to_select=best_nb_features)
    rfe.fit(X, y)

    ## save ranking information
    output_file = open(ranking_file_name, "w")
    output_file.write("VAR_NAME,SELECTED,RANK\n")
    variable_name_list = list(X.keys())
    for i in range(X.shape[1]):
        var_name = variable_name_list[i]
        line_to_write = str(var_name)+","+str(rfe.support_[i])+","+str(rfe.ranking_[i])+"\n"
        output_file.write(line_to_write)
    output_file.close()

    ## save nb_feature search information
    output_file = open(nb_feature_file_name, "w")
    output_file.write("NB_VAR,MEAN_ACC\n")
    for i in range(0,len(names)):
        var_nb = names[i]
        mean_score = results[i].mean()
        line_to_write = str(var_nb)+","+str(mean_score)+"\n"
        output_file.write(line_to_write)
    output_file.close()


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
		- "Boruta"
		- "all" (perform all 4 analysis)

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

	## Run the R script
	if(valid_output and valid_input):
		if(analysis == "covarianceMatrix"):
			os.system("Rscript "+CORRELATIONMATRIX_SCRIPT+" "+str(input_data)+" "+str(output_folder))
		elif(analysis == "attributeImportance"):
			os.system("Rscript "+ATTRIBUTEIMPORTANCE_SCRIPT+" "+str(input_data)+" "+str(output_folder))
		elif(analysis == "RFE"):

			## call RFE function
			run_rfe(input_data, output_folder)

			# -> old stuff, call Rscript
			#os.system("Rscript "+RFE_SCRIPT+" "+str(input_data)+" "+str(output_folder))

		elif(analysis == "Boruta"):

			## call Boruta function
			run_boruta(input_data, output_folder)

			# -> old stuff, call Rscript
			#os.system("Rscript "+BORUTA_SCRIPT+" "+str(input_data)+" "+str(output_folder))

		elif(analysis == "all"):
			os.system("Rscript "+CORRELATIONMATRIX_SCRIPT+" "+str(input_data)+" "+str(output_folder))
			os.system("Rscript "+ATTRIBUTEIMPORTANCE_SCRIPT+" "+str(input_data)+" "+str(output_folder))
			os.system("Rscript "+RFE_SCRIPT+" "+str(input_data)+" "+str(output_folder))
			os.system("Rscript "+BORUTA_SCRIPT+" "+str(input_data)+" "+str(output_folder))


	elif(not valid_output):
		print("[ERROR] => Can't find the output folder "+str(output_folder))
	elif(not valid_input):
		print("[ERROR] => Can't find the input file "+str(input_data))



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

			Boruta_image_1 = result_folder+"boruta_results_1.png"
			Boruta_image_2 = result_folder+"boruta_results_2.png"
			Boruta_results_file = result_folder+"boruta_results.csv"


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

			Boruta_image_1 = result_folder+separator+"boruta_results_1.png"
			Boruta_image_2 = result_folder+separator+"boruta_results_2.png"
			Boruta_results_file = result_folder+separator+"boruta_results.csv"

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


		## Construct the summary data
		summary_data = {}
		data = open(Boruta_results_file, "r")
		cmpt = 0
		for line in data:
			line = line.replace("\n", "")
			line_in_array = line.split(",")
			if(cmpt > 0):
				key = line_in_array[0]
				summary_data[key] = {"Correlation" : "Pass",
				                     "Variance" : "Pass",
				                     "RFE" : "Flagged",
				                     "Boruta" : "UNDEF"}
			cmpt += 1
		data.close()

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
			summary_data[str(var)]["Correlation"] = "Flagged"
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
				summary_data[str(line_in_array[0])]["Variance"] = "Flagged"
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
		report.write("<center>\n")
		report.write("<table>\n")
		for line in data:
			line = line.replace("\n", "")
			line_in_array = line.split(",")
			report.write("<tr bgcolor=\"#F5F6CE\">\n")
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
		report.write("</center>\n")

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
				summary_data[str(line_in_array[1])]["RFE"] = "Pass"
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



		##----------------##
		## Work on Boruta ##
		##----------------##
		report.write("<h3>Boruta</h3>\n")

		## display the two graphic
		report.write("<img src="+Boruta_image_1+" style=\"width:600px;height:400px;\" align=\"left\">\n")
		report.write("<img src="+Boruta_image_2+" style=\"width:600px;height:400px;\" align=\"right\">\n")

		## write result table
		data = open(Boruta_results_file, "r")
		cmpt = 0
		report.write("<center>\n")
		report.write("<table>\n")
		for line in data:
			line = line.replace("\n", "")
			line_in_array = line.split(",")

			## deal with stupid format
			if(cmpt == 0):
				line_in_array = [" "] + line_in_array

			## define the bgcolor
			bgcolor = "#F5ECCE"
			if(line_in_array[-1] == "\"Rejected\""):
				bgcolor = "#DF0101"
				summary_data[str(line_in_array[0])]["Boruta"] = "Flagged"
			elif(line_in_array[-1] == "\"Confirmed\""):
				bgcolor = "#5FB404"
				summary_data[str(line_in_array[0])]["Boruta"] = "Pass"

			report.write("<tr bgcolor=\""+bgcolor+"\">\n")
			cmpt_elt = 0
			for elt in line_in_array:
				elt = elt.replace("\"", "")
				if(cmpt == 0):
					report.write("<th>"+str(elt)+"</th>\n")
				else:
					report.write("<td>"+str(elt)+"</td>\n")
				cmpt_elt += 1
			report.write("</tr>\n")
			cmpt += 1
		data.close()
		report.write("</table>\n")
		report.write("</center>\n")


		##----------------##
		## [TODO] Summary ##
		##----------------##
		report.write("<h3>Summary</h3>\n")

		## write table
		report.write("<center>\n")
		report.write("<table>\n")

		bgcolor = "#F5ECCE"

		##header
		report.write("<tr bgcolor=\""+bgcolor+"\">\n")
		report.write("<th>Features</th>\n")
		report.write("<th>Correlation</th>\n")
		report.write("<th>Variance</th>\n")
		report.write("<th>RFE</th>\n")
		report.write("<th>Boruta</th>\n")
		report.write("</tr>\n")

		## data
		for key in summary_data.keys():
			report.write("<tr bgcolor=\""+bgcolor+"\">\n")
			report.write("<td>"+str(key)+"</td>\n")
			if(summary_data[key]["Correlation"] == "Pass"):
				report.write("<td bgcolor=\"#5FB404\">"+summary_data[key]["Correlation"]+"</td>\n")
			else:
				report.write("<td bgcolor=\"#DF3A01\">"+summary_data[key]["Correlation"]+"</td>\n")

			if(summary_data[key]["Variance"] == "Pass"):
				report.write("<td bgcolor=\"#5FB404\">"+str(summary_data[key]["Variance"])+"</td>\n")
			else:
				report.write("<td bgcolor=\"#DF3A01\">"+str(summary_data[key]["Variance"])+"</td>\n")
			if(summary_data[key]["RFE"] == "Pass"):
				report.write("<td bgcolor=\"#5FB404\">"+str(summary_data[key]["RFE"])+"</td>\n")
			else:
				report.write("<td bgcolor=\"#DF3A01\">"+str(summary_data[key]["RFE"])+"</td>\n")
			if(summary_data[key]["Boruta"] == "Pass"):
				report.write("<td bgcolor=\"#5FB404\">"+str(summary_data[key]["Boruta"])+"</td>\n")
			else:
				report.write("<td bgcolor=\"#DF3A01\">"+str(summary_data[key]["Boruta"])+"</td>\n")
			report.write("</tr>\n")
		report.write("</table>\n")
		report.write("</center>\n")









		report.write("</html>\n")
		report.close()


	elif(not valid_result_folder):
		print("[ERROR] => Can't find the output folder "+str(result_folder))
	elif(not valid_data_file):
		print("[ERROR] => Can't find the input file "+str(data_file))
	elif(not all_results_file_present):
		print("[ERROR] => following files are missing in "+str(result_folder)+":")
		for f in missing_files:
			print("\t-> "+str(f))
