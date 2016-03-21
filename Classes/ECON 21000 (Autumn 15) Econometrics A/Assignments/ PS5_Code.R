#===========================
# Econ 210                 
# Problem Set 5                         
# evanliao@uchicago.edu
#===========================


#The code for this problem is from Mohsen (with some modifications by Evan)!
#make sure to put the CSV data file in the working directory for R

rm(list=ls())
# setwd

#################################
########### Problem 1 ########### 
#################################

#declare library for multivariate normal
library(MASS)

#Part (a)
n = 100

#(a) i.
#draw data
epsilon<-rnorm(n,0,1)
x1<-rnorm(n,2,sqrt(1.5))
x2<-rnorm(n,1,sqrt(1.5))
x3<-rnorm(n,1,sqrt(1.5))

#create y
y<- 1 + (1.5)*x1 + 2*x2 + x3 + epsilon

#run regression
summary(lm(y~x1 + x2))


#(a) ii.
#draw data when x2 x3 correlated
epsilon<-rnorm(n,0,1)
x1<-rnorm(n,2,sqrt(1.5))
x23<-mvrnorm(n,c(1,1), matrix(c(1.5,1,1,1.5),byrow = T,nrow=2))

#create y
y<- 1 + (1.5)*x1 + 2*x23[,1] + x23[,2] + epsilon

summary(lm(y~x1 + x23[,1]))


#(a) iii.
#We can rerun the above for beta3 = 0, beta3 = 2

#beta3 = 2
y<- 1 + (1.5)*x1 + 2*x23[,1] + 2*x23[,2] + epsilon
summary(lm(y~x1 + x23[,1]))

#beta3 = 0
y<- 1 + (1.5)*x1 + 2*x23[,1] + 0*x23[,2] + epsilon
summary(lm(y~x1 + x23[,1]))



#part (b) just copy paste with new n
n<-1000

#(b) i.
#draw data
epsilon<-rnorm(n,0,1)
x1<-rnorm(n,2,sqrt(1.5))
x2<-rnorm(n,1,sqrt(1.5))
x3<-rnorm(n,1,sqrt(1.5))

#create y
y<- 1 + (1.5)*x1 + 2*x2 + x3 + epsilon

#run regression
summary(lm(y~x1 + x2))


#(b) ii.

#draw data when x2 x3 correlated
epsilon<-rnorm(n,0,1)
x1<-rnorm(n,2,sqrt(1.5))
x23<-mvrnorm(n,c(1,1), matrix(c(1.5,1,1,1.5),byrow = T,nrow=2))

#create y
y<- 1 + (1.5)*x1 + 2*x23[,1] + x23[,2] + epsilon

summary(lm(y~x1 + x23[,1]))




#part (c) put it in a loop to repeat 500 times.
simus<-500
n<-1000

#create vector to store results.
betas<-mat.or.vec(simus,3)
betas2<-mat.or.vec(simus,3)

for(i in 1:simus)
{
  #draw data
  epsilon<-rnorm(n,0,1)
  x1<-rnorm(n,2,sqrt(1.5))
  x2<-rnorm(n,1,sqrt(1.5))
  x3<-rnorm(n,1,sqrt(1.5))
  
  #create y
  y<- 1 + (1.5)*x1 + 2*x2 + x3 + epsilon
  
  #run regression and store values
  betas[i,]<-summary(lm(y~x1 + x2))$coefficients[,1]
  
  
  #draw data when x2 x3 correlated
  epsilon<-rnorm(n,0,1)
  x1<-rnorm(n,2,sqrt(1.5))
  x23<-mvrnorm(n,c(1,1), matrix(c(1.5,1,1,1.5),byrow = T,nrow=2))
  
  #create y
  y<- 1 + (1.5)*x1 + 2*x23[,1] + x23[,2] + epsilon
  
  #run regression and store values
  betas2[i,]<-summary(lm(y~x1 + x23[,1]))$coefficients[,1]
  
}


#plot histograms
hist(betas[,3],main="Beta_2 for i.")
hist(betas2[,3],main="Beta_2 for ii.")



#################################
########### Problem 3 ########### 
#################################

#read in data
library(foreign)
ceosal<- read.dta("ceosal2.dta")

#part (a)

summary(lm(log(salary)~log(sales)+log(mktval),ceosal))


#part (b)

#run the level
summary(lm(log(salary) ~ log(sales) + log(mktval) + profits,ceosal))


#remove the NAs in other words negative values have no log so remove
datatemp <- ceosal[!(ceosal$profits <= 0),]

#run the log reg
summary(lm(log(salary) ~ log(sales) + log(mktval) + log(profits),datatemp))


#part (c)

cor(ceosal)


#part (d)

#add a column for ceotenure squared
datatemp2<-cbind(datatemp,datatemp[,6]^2)

#run the level
summary(lm(log(salary) ~ log(sales) + log(mktval) + log(profits) + ceoten + datatemp2[,11],datatemp2))



#################################
########### Problem 4 ########### 
#################################


cps <- read.csv("cps08.csv")

#part (a)
summary(lm(ahe ~ age + female + bachelor,cps))


#part (b)

#generate interaction
cps<-cbind(cps,cps[,4]*cps[,5])
colnames(cps)[7]<-"femxbach"

#run regression
summary(lm(ahe ~ age + female + bachelor + femxbach,cps))


#part (d)

#generate interaction

cps<-cbind(cps,cps[,6]*cps[,4])
colnames(cps)[8]<-"agexbach"

#run regression
summary(lm(ahe ~ female + bachelor + femxbach + age + agexbach,cps))



#part (e)

reg.cps <- summary(lm(ahe ~ female + bachelor + femxbach + age + agexbach,cps))

# obtain the covariance matrix for coefficients
cov <- vcov(reg.cps)


# define the linear restriction
c <- matrix(c(0,0,0,0,1,-1),6,1)

# compute the test statistic
T_n <- (reg.cps$coefficients[5,1]-reg.cps$coefficients[6,1])/sqrt(t(c)%*%cov%*%c)


# This is an alternative method for tesing the hypothsis
#run reduced regression
reduced<-cps[,6] + cps[,8]

summary(lm(ahe ~ female + bachelor + femxbach + reduced,cps))

#get SSR for reduced
summary(aov(ahe ~ female + bachelor + femxbach + reduced,cps))

#get SSR for full
summary(aov(ahe ~ female + bachelor + femxbach + age+ agexbach,cps))


