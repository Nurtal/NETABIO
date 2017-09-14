##------------------------------------------------##
## Use the Boruta algorithm to estimate           ##
## the contribution of each attribute in the data ##
## to a classification problem                    ##
##------------------------------------------------##

## Load the library
library(Boruta)

## Parse the arguments
args = commandArgs(trailingOnly=TRUE)

## Init file name [FIXEME]
data_file_name = args[1]
boruta_image_file_name_1 = paste(args[2], "boruta_results_1.png", sep ="")
boruta_image_file_name_2 = paste(args[2], "boruta_results_2.png", sep ="")
boruta_results_file_name = paste(args[2], "boruta_results.csv", sep ="")

## Load the data
## use only patient without NA
data <- read.csv(data_file_name, stringsAsFactors=TRUE)
data = data[complete.cases(data),]
data <- data.frame(lapply(data, as.factor))

## Run Boruta
panel_to_process <- data
boruta.train <- Boruta(Disease~., data = panel_to_process, doTrace = 2)

## Display results 1
png(boruta_image_file_name_1)
plot(boruta.train, xlab = "", xaxt = "n")
lz<-lapply(1:ncol(boruta.train$ImpHistory),function(i)
  boruta.train$ImpHistory[is.finite(boruta.train$ImpHistory[,i]),i])

names(lz) <- colnames(boruta.train$ImpHistory)
Labels <- sort(sapply(lz,median))
axis(side = 1,las=2,labels = names(Labels),
     at = 1:ncol(boruta.train$ImpHistory), cex.axis = 0.7)
dev.off()

## Supplemental Results
final.boruta <- TentativeRoughFix(boruta.train)

## Display results 2 (after tentative rough fix)
png(boruta_image_file_name_2)
plot(final.boruta, xlab = "", xaxt = "n")
lz<-lapply(1:ncol(boruta.train$ImpHistory),function(i)
  boruta.train$ImpHistory[is.finite(boruta.train$ImpHistory[,i]),i])

names(lz) <- colnames(boruta.train$ImpHistory)
Labels <- sort(sapply(lz,median))
axis(side = 1,las=2,labels = names(Labels),
     at = 1:ncol(boruta.train$ImpHistory), cex.axis = 0.7)
dev.off()

## Save analysis results in a csv file
getSelectedAttributes(final.boruta, withTentative = F)
boruta.df <- attStats(final.boruta)
write.table(boruta.df, boruta_results_file_name, sep=",")

