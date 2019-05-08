# Binomial-Option-Pricing
Binomial option pricing model in Python for American Options.

Code generates the stock / option price lattice for american options based on an underlying instrument.

Parameters:<br>
mu = mean
sigma = volatility
T = total time to simulate option prices until
t = optional parameter that can be used to pick specific time to display prices after simulation (e.g. as puts[len(puts)-t-1] or S[t])
dt = time intervals to split T into
r = risk free rate (used here as per dt)
S = option underlying price at t=0 (instantiated here as a list of lists to use as the lattice variable)
K = strike price of the option

The option price is calculated as

max(0, S[t]-K) if t=T
max(max(0,S[t]-K), p*exp(-r*dt)*c[t+1, i] + (1-p)*exp(-r*dt)*c[t+1, i+1]) if t<T
