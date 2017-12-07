##--------------------------------------##
## Recursive Feature Elimination (RFE)  ##
## args[1] -> path to the input data    ##
## args[2] -> path to the output folder ##  
##--------------------------------------##

## Load the library
library(mlbench)
library(caret)

## Parse the arguments
args = commandArgs(trailingOnly=TRUE)

## Init file name
data_file_name = args[1]
rfe_analysis_results_file = paste(args[2], "RFE_results.csv", sep ="")
predictors_file_name = paste(args[2], "RFE_selected_attributes.csv", sep ="")
accuracy_image_file_name = paste(args[2], "RFE_accuracy.png", sep ="")

## Load the data
data <- read.csv(data_file_name, stringsAsFactors=TRUE)
data <- data[complete.cases(data), ]

## Prepare training scheme
control <- rfeControl(functions=rfFuncs, method="cv", number=10)

## Run the RFE algorithm
results <- rfe(data[,2:ncol(data)], data[,1], sizes=c(2:ncol(data)), rfeControl=control)

## Get and save the results for the RFE
output <- results$results
write.csv(output, rfe_analysis_results_file)

## List the chosen features
write.csv(predictors(results), predictors_file_name)

## Plot the results
png(filename = accuracy_image_file_name)
plot(results, type=c("g", "o"))
dev.off()
