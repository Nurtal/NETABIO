## Test function from the netabio
## package


## importation
from netabio import na_manager
from netabio import biotoolbox 
from netabio import quality_control
from netabio import feature_selection

from netabio import TEST_DATA

def run():

	## general parameters
	data_file_name = TEST_DATA
	separator = ","
	test_value = "53,7%"
	input_vector = ["5","3","4","6","89","5","6"]
	col_number = 1
	header_detected = True
	output_folder = "output"
	analysis = "all"
	report_file = "report.html"

	## biotoolbox module
	print "[TEST] Testing biotoolbox module from netabio package"
	biotoolbox.detect_file_format(data_file_name)
	biotoolbox.change_file_format(data_file_name, separator)
	biotoolbox.fix_file_name(data_file_name)

	## na_manager module
	print "[TEST] Testing na_manager module from netabio package"
	na_manager.check_NA_proportion_in_file(data_file_name)
	na_manager.display_NA_proportions(data_file_name)
	na_manager.filter_NA_values(data_file_name)

	## quality_control module
	print "[TEST] Testing quality_control module from netabio package"
	quality_control.check_pourcentages(test_value)
	quality_control.looking_for_outliers(input_vector, col_number)
	quality_control.basic_check(data_file_name)
	quality_control.check_standard_deviation(data_file_name)
	quality_control.check_zscore(data_file_name, separator, header_detected)

	## feature_selection module
	print "[TEST] Testing feature_selection module from netabio package"
	feature_selection.run_analyser(data_file_name, output_folder, analysis)
	feature_selection.write_html_report(report_file, data_file_name, output_folder)

