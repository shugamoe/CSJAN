#===========================
# Econ 210                 
# Problem Set 3            
# Problem 4             
# evanliao@uchicago.edu
#===========================

##################
#### part (a) ####
##################

# set random seed
set.seed(210)

# generate a random sample
X <- runif(10,-0.3,0.7)
mu_tilde <- mean(X)


##################
#### part (b) ####
##################

# create placeholder for simulation results
mu_hat <- rep(0,500)

# simulation
for (i in 1:500) {
  mu_hat[i] = mean(runif(10,-0.5,0.5))
}

# plot a histogram for mu_hat
hist(mu_hat)

# find the 95th percentile of mu_hat
quantile(mu_hat,0.95)

# compare mu_tilde with the 95th percentile
mu_tilde > quantile(mu_hat,0.95)

# create the empirical cdf function from mu_hat
Fn = ecdf(mu_hat)

# compute the probability that we would reject the null
1 - Fn(mu_tilde)

##################
#### part (c) ####
##################

# create placeholder for simulation results
mu_hat_2 <- rep(0,500)

# simulation
for (i in 1:500) {
  mu_hat_2[i] = mean(runif(10,-0.3,0.7))
}

# plot a histogram for mu_hat_2
hist(mu_hat_2)

# calculate the proportion of mu_hat_2 falling above 
# the 95th percentile obtained in part (b)
sum(mu_hat_2 > quantile(mu_hat,0.95))/length(mu_hat_2)
