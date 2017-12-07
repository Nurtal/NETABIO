##----------------------------------------------------------------------------##
## Estimate the importance of each attributes.                                ##
## The absolute value of the t–statistic for each model parameter is used.    ##
## glmboost and glmnet : the absolute value of the coefficients corresponding ##
## the the tuned model are used                                               ##
## args[1] -> path to the input data 	                    				  ##
## args[2] -> path to the output folder                                       ##
##----------------------------------------------------------------------------##

## Load the library
library(mlbench)
library(caret)

## Parse the arguments
args = commandArgs(trailingOnly=TRUE)

## Init file name
data_file_name = args[1]
attribute_importance_file_name = paste(args[2], "attribute_importance.csv", sep ="")
attribute_importance_plot_name = paste(args[2], "attribute_importance.png", sep ="")

## Load the data
data <- read.csv(data_file_name, stringsAsFactors=TRUE)
data <- data[complete.cases(data), ]

## Prepare training scheme
control <- trainControl(method="repeatedcv", number=10, repeats=3)

## Train the model
model <- train(Disease~., data=data, method="lvq", preProcess="scale", trControl=control)

## estimate variable importance and save it in file
importance <- varImp(model, scale=FALSE)
write.csv(importance$importance, attribute_importance_file_name)

## Plot importance
png(filename = attribute_importance_plot_name)
plot(importance)
dev.off()
