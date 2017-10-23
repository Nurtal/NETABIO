##
## Quality control
##


import biotoolbox




def basic_check(data_file):
	"""
	-> Check a few things
	"""


	## Detect the best separator in file
	separator = biotoolbox.detect_file_format(data_file)
	print separator

	## Look for errors in the numbers of entry per line
	len_of_lines = []
	input_data = open(data_file, "r")
	for line in input_data:
		line = line.replace("\n", "")
		line_in_array = line.split(separator)
		len_of_lines.append(len(line_in_array)) 
	input_data.close()

	header_size = len_of_lines[0]
	cmpt = 0
	for size in len_of_lines:
		print header_size
		print size
		if(size != header_size):
			print "flag line "+str(cmpt)

		cmpt += 1