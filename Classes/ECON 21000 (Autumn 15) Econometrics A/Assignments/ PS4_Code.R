#===========================
# Econ 210                 
# Problem Set 4            
# Question 6             
# evanliao@uchicago.edu
#===========================


#The code for this problem is from Mohsen!
#make sure to put the CSV data file in the working directory for R

rm(list=ls())

data<-read.csv("traffic_fatalities.csv")

# Part A
deaths_yearly = c(1043,911,927,918,957)
deaths_weekly = as.vector(t(matrix(rep(deaths_yearly/52,52),5,52)))
y = c(deaths_weekly, rep(322/17,17) )
d = c(rep(0,260),rep(1,17))
summary(lm(y~d))

# Part C
y = c(deaths_yearly,322*(52)/17)
d = c(rep(0,5),1)
summary(lm(y~d))

# Part D
data = read.csv("traffic_fatalities.csv")
yearly = aggregate(data$deaths, by = list(data$year), FUN=sum)

# Part E
summary(lm(data$deaths~data$signs))

# Part F
summary(lm(data$deaths~data$signs+data$tourists+data$icy_days))

# Part G
plot(data$week,data$icy_days)

mean(data$icy_days)
