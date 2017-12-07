from netabio import data_extraction
from netabio import feature_selection
from netabio import quality_control
import argparse

def test():
	parser = argparse.ArgumentParser(prog='my_test_stuff')
	#data_extraction.generate_Luminex_data_file("C:\\Users\NaturalKiller01\\Desktop\\Nathan\\Spellcraft\\DATA\\PHASE_I_II_28_08_2017.tsv", group_pos="start", group_name="Disease", phase="I")
	parser.add_argument('-i', nargs='?', help='help for -i blah')
	args = parser.parse_args()
	collected_inputs = {'i': args.i}
	data_extraction.generate_Luminex_data_file(collected_inputs['i'], group_pos="start", group_name="Disease", phase="I")



def features_selection():
	"""
	-> Perform a features selection procedure:
		- get arguments from the command line
			- i : the input file (mandatory)
			- o : the output folder (mandatory)
			- r : the name of the report file (optionnal, default is report.html)
		- run analysis (analysis type set to "all")
		- write report 
	"""
	
	## Collect arguments
	parser = argparse.ArgumentParser(prog='netabio_stuff') # not sure what does the instanciation
	parser.add_argument('-i', nargs='?', help='the input data file')
	parser.add_argument('-o', nargs='?', help='the output directory')
	parser.add_argument('-r', nargs='?', help='the name of the report file')
	args = parser.parse_args()

	## Init optionnal arguments
	if(not args.r):
		args.r = "report.html"
	collected_inputs = {'i': args.i,
	                    'r': args.r,
					    'o': args.o}

	## Get the name of the prepared data file
	report_file = str(collected_inputs["o"])+"/"+str(collected_inputs["r"])
	data_file = str(collected_inputs["i"])
	result_folder = str(collected_inputs["o"])

	## Run analysis
	feature_selection.run_analyser(data_file, result_folder, "all")

	## write report
	feature_selection.write_html_report(report_file, data_file, result_folder)




def features_selection_workspace():
	"""
	[IN PROGRESS]

	-> Grand bazar, scavange stuff from this function
	-> TODO:
		- get a list of args
		- implement the feature selection procedure ...
		- include the fudction in entry point
	"""

	
	## Collect arguments
	parser = argparse.ArgumentParser(prog='netabio_stuff') # not sure what does the instanciation
	parser.add_argument('-i', nargs='?', help='the input data file')
	parser.add_argument('-gp', nargs='?', help='the group position (label) in the reformated file')
	parser.add_argument('-gn', nargs='?', help='the group name (colname of the label) in the reformated file')
	parser.add_argument('-ph', nargs='?', help='the phase we want in the reformated dile')
	parser.add_argument('-o', nargs='?', help='the output directory')

	args = parser.parse_args()

	## Init optionnal arguments
	if(not args.gp):
		args.gp = "start"
	if(not args.gn):
		args.gn = "Disease"
	if(not args.ph):
		args.ph = "all"

	collected_inputs = {'i': args.i,
	                    'gp': args.gp,
					    'gn': args.gn,
					    'ph': args.ph,
					    'o': args.o}

	## Prepare data file
	#data_extraction.generate_Luminex_data_file(collected_inputs['i'], group_pos=collected_inputs['gp'], group_name=collected_inputs['gn'], phase=collected_inputs['ph'])

	## Get the name of the prepared data file
	report_file = "C:\\Users\\NaturalKiller01\\Desktop\\Nathan\\Spellcraft\\TRASH\\report.html"
	data_file = "C:\\Users\\NaturalKiller01\\Desktop\\Nathan\\Spellcraft\\Luminex_data_NA_filtered.csv"
	result_folder = "C:\\Users\\NaturalKiller01\\Desktop\\Nathan\\Spellcraft\\TRASH"

	## Run analysis
	feature_selection.run_analyser(data_file, result_folder, "all")

	## write report
	feature_selection.write_html_report(report_file, data_file, result_folder)  


def quality_control_operation():
	"""
	-> Run the basic_check function from 
	   quality_control file, with the data file retrieve
	   as input.
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


	## Collect arguments
	parser = argparse.ArgumentParser(prog='netabio_stuff') # not sure what does the instanciation
	parser.add_argument('-i', nargs='?', help='the input data file')
	args = parser.parse_args()

	## Init optionnal arguments
	collected_inputs = {'i': args.i}

	## main operation
	quality_control.basic_check(collected_inputs['i'])



def consistency_control_operation():

	## Collect arguments
	parser = argparse.ArgumentParser(prog='netabio_stuff') # not sure what does the instanciation
	parser.add_argument('-i', nargs='?', help='the input data file')
	args = parser.parse_args()

	## Init optionnal arguments
	collected_inputs = {'i': args.i}

	## main operation
	quality_control.consistency_check(collected_inputs['i'])
