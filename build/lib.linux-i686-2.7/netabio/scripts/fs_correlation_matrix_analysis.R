##--------------------------------------------------------##
## Work on the variance and covariance of the attributes, ##
## look for redundant and near zero variance attributes   ##
## save all results in csv and text files                 ##
## args[1] -> path to the input data 			  ##
## args[2] -> path to the output folder                   ##
##--------------------------------------------------------##

## Load the library
library(mlbench)
library(caret)

## Parse the arguments
args = commandArgs(trailingOnly=TRUE)

## Init file name
data_file_name = args[1]
correlationMatrix_file_name = paste(args[2], "correlationMatrix.csv", sep ="")
correlation_log_file_name = paste(args[2], "high_correlation.txt", sep ="")
variance_analysis_file_name = paste(args[2], "variance_analysis.csv", sep ="")

## Load the data
data <- read.csv(data_file_name, stringsAsFactors=TRUE)
data <- data[complete.cases(data), ]

## Calculate and save correlation matrix
correlationMatrix <- cor(data[,2:ncol(data)])
write.csv(correlationMatrix, correlationMatrix_file_name)
## Find attributes that are highly corrected (ideally >0.75) and save the console output in a log file
sink(file = correlation_log_file_name)
highlyCorrelated <- findCorrelation(correlationMatrix, cutoff=0.75, verbose = TRUE, names = TRUE)
sink()

## Chek if any attributes have a near Zero variance ans save the results in a csv file
variance_analysis <- nearZeroVar(data, freqCut = 95/5, saveMetrics = TRUE)
write.csv(variance_analysis, variance_analysis_file_name)
