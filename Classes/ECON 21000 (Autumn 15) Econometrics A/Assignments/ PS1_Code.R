#===========================
# Econ 210                 
# Problem Set 1            
# Problem 5 (c)            
# evanliao@uchicago.edu
#===========================



# set random seed
set.seed(210)

# Generate U,V, and W
U <- rnorm(40,0,1)
V <- rnorm(40,0,1)
W <- rnorm(40,0,1)

# Construct X,Y
X <- (2*U + V + 1)
Y <- (-U + 3*W + 3)

# Draw a scatterplot
# install.packages("car")
library(car)
scatterplot(X~Y)

# Compute all of our desired moments

#################
#### part vi ####
#################

mean(X)
mean(Y)

##################
#### part vii ####
##################
var(X)
var(Y)

##################
#### part viii ###
##################
cov(X,Y)
cor(X,Y)

#################
#### part ix ####
#################
mean(X+Y)
var(X+Y)

#################
##### part x ####
#################
cov(X+Y,Y)
cor(X+Y,Y)