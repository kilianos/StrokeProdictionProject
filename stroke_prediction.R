# Stroke Prediction Project

# Load Required Libraries
library(car)
library(readxl)
library(dplR)
library(tidyverse)
library(ggplot2)
library(moments)
library(neuralnet)
library(arulesViz)
library(kernlab)
library(e1071)
library(gridExtra)
library(caret)
library(arules)
library(cowplot)

# reading in original excel file
strokedesc <- read_excel("/Users/thomasmarianos/OneDrive - Syracuse University/Grad School/IST 687/Project/healthcare-dataset-stroke-data.xls")
str(stroke)
stroke <- strokedesc

#omit all N/A's from Dataset
stroke <- na.omit(stroke)

#subsetting the age column
stroke <- subset(stroke, age>10)

#convert bmi to numeric
stroke <- stroke[- grep("N/A", stroke$bmi),]
stroke$bmi <- as.numeric(stroke$bmi)

#removing unknowns from smoking column
stroke <- stroke[- grep("Unknown", stroke$smoking_status),]

#subsetting the dataset in order to generate a random sample 
hadstroke <- subset(stroke, stroke == 1)
nostroke <- subset(stroke, stroke == 0)

#pulling random samples from nostroke in order to make comparable to hadstroke to run machine learning models
SampleNoStroke <- nostroke[sample(nrow(nostroke), 350),]

#combining the two dataframes
Stroke <- rbind(SampleNoStroke, hadstroke)
Stroke <- Stroke[,-1]

#randomizing the Stroke dataframe
set.seed(45)
rows <- sample(nrow(Stroke))
Stroke <- Stroke[rows,]

#Getting Ready for Regression
#Changing Categorical to Factors w/ levels
Stroke$gender <- factor(Stroke$gender)
Stroke$ever_married <- factor(Stroke$ever_married)
Stroke$work_type <- factor(Stroke$work_type)
Stroke$Residence_type <- factor(Stroke$Residence_type)
Stroke$smoking_status <- factor(Stroke$smoking_status)
Stroke$hypertension <- factor(Stroke$hypertension)
Stroke$heart_disease <- factor(Stroke$heart_disease)

#Changing all quantitative variables to numeric
Stroke$age <- as.numeric(Stroke$age)
Stroke$avg_glucose_level <- as.numeric(Stroke$avg_glucose_level)
Stroke$bmi <- as.numeric(Stroke$bmi)

#Train/Test Split
##75% of the sample size
sample_size <- floor(0.75 * nrow(Stroke))

#setting seed to reproduce partition
set.seed(123)

#subsetting training data
training_index <- sample(seq_len(nrow(Stroke)), size = sample_size)
trainingdata <- Stroke[training_index,]
train_x <- trainingdata[,(1:10)]
train_x <- as.matrix(train_x[,-1])
train_y <- trainingdata[,-(1:10)]

#subsetting testing data
testingdata <- Stroke[-training_index,]
test_x <- testingdata[,(1:10)]
test_y <- testingdata[,-(1:10)]

#LinearModel
Stroke.Linear <- lm(stroke ~ work_type + smoking_status + Residence_type + 
                    hypertension + heart_disease + gender + ever_married + bmi + 
                    avg_glucose_level + age, data=trainingdata)
summary(Stroke.Linear)

Pred.Linear <- predict(Stroke.Linear,testingdata)
Pred.Linear
str(Pred.Linear)

compTable.Linear <- data.frame(testingdata[,11],Pred.Linear)
colnames(compTable.Linear) <- c("test","Pred")
compTable.Linear$Pred <- ifelse(compTable.Linear$Pred<.6, 0, 1)

sqrt(mean((compTable.Linear$test-compTable.Linear$Pred)^2))

results <- table(original = compTable.Linear$test, pred = compTable.Linear$Pred)
print(results)

perc.Linear <- length(which(compTable.Linear$test == compTable.Linear$Pred))/dim(compTable.Linear)[1]
perc.Linear

#Probit Regression
Stroke.Probit <- glm(stroke ~ work_type + smoking_status + Residence_type + 
                      hypertension + heart_disease + gender + ever_married + bmi + 
                       avg_glucose_level + age, family=binomial(probit), data=Stroke)
summary(Stroke.Probit)

#Logit Regression - Less sensitive than probit to outliers
Stroke.Logit <- glm(stroke ~ work_type + smoking_status + Residence_type + 
                      hypertension + heart_disease + gender + ever_married + bmi + 
                      avg_glucose_level + age, family=binomial(logit), data=Stroke)
summary(Stroke.Logit)
exp(coef(Stroke.Logit)) # Exponentiated coefficients ("odds ratios")

summary(Stroke)

Stroke.Logit <- glm(stroke ~ age + hypertension + avg_glucose_level, family=binomial(logit), data=Stroke)
summary(Stroke.Logit)

#Variance Inflation Factor Shows no multi-collinearity between variables we kept
vif <- vif(Stroke.Logit)    
vif

#ksvm
Strokeksvm <- ksvm(stroke~., data = trainingdata, kernel = "rbfdot", kpar="automatic", C=10,cross=10, prob.model=TRUE)
Strokeksvm
ksvm.pred <- predict(Strokeksvm, testingdata)
head(ksvm.pred)


#building a dataframe to compare prediction vs. actual
compare_ksvm <- data.frame(test_y, ksvm.pred)
head(compare_ksvm)
colnames(compare_ksvm) <- c("test", "pred")
compare_ksvm$pred <- ifelse(compare_ksvm$pred<.6, 0, 1)
tail(compare_ksvm)
percent_ksvm <- length(which(compare_ksvm$test==compare_ksvm$pred))/dim(compare_ksvm)[1]
percent_ksvm

results <- table(original = compare_ksvm$test, pred = compare_ksvm$pred)
print(results)

# Plot the results
compare_ksvm$correct <- ifelse(compare_ksvm$test == compare_ksvm$pred, "correct", "wrong")

df.ksvm <- data.frame(compare_ksvm$correct, testingdata$age, testingdata$avg_glucose_level, testingdata$stroke, compare_ksvm$pred)
colnames(df.ksvm) <- c("correct", "age", "glucose", "stroke", "pred")

plot.ksvm <- ggplot(df.ksvm, aes(x = age,y = glucose)) + 
  geom_point(aes(size = correct, color = stroke)) + 
  scale_shape_identity() +
  ggtitle("KSVM Plot")
plot.ksvm

