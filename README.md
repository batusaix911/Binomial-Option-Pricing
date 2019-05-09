# Binomial-Option-Pricing
Binomial option pricing model in Python for American Options.

Code generates the stock / option price lattice for american options based on an underlying instrument.

Parameters:<br>
mu = mean<br>
sigma = volatility<br>
T = total time to simulate option prices until<br>
t = optional parameter that can be used to pick specific time to display prices after simulation (e.g. as puts[len(puts)-t-1] or S[t])<br>
dt = time intervals to split T into<br>
r = risk free rate (used here as per dt)<br>
S = option underlying price at t=0 (instantiated here as a list of lists to use as the lattice variable)<br>
K = strike price of the option<br>

The option price is calculated as:

max(0, S[t]-K) if t=T<br>
max(max(0,S[t]-K), p\*exp(-r\*dt)\*c[t+1, i] + (1-p)\*exp(-r\*dt)\*c[t+1, i+1]) if t<T

There is also code to plot the lattice. This is not entirely useful since it plots 2^T paths for the entire lattice. This quickly blows up and if T/dt > 15, the pyplot object will quickly run out of memory.
