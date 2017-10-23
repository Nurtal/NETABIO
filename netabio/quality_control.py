##
## Quality control
##


import biotoolbox




def basic_check(data_file):
	"""
	-> Check a few things
	->
	"""


	## Detect the best separator in file.
	## Detect problem of not enough lines & 
	## differences in lenght of lines
	separator = biotoolbox.detect_file_format(data_file)
	if(separator == "undef"):
		print "[WARNING]=>Very few lines in file (Less than 2)"
	elif(separator == "Difference in lenght of lines"):
		print "[ERROR]=>Difference in lenght of lines"

	


## TEST SPACE ##

basic_check("test.txt")