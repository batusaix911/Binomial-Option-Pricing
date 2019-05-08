import numpy
import matplotlib.pyplot as plt
import copy

mu=0.01
sigma=0.01
T=3
t=1
dt=0.5
r=0.005
S=[[10]]
K=10

u = numpy.exp(sigma * dt**0.5)
d = 1/u
p = (numpy.exp(r*dt)-d)/(u-d)

for i in range(int(T/dt)):
    St=[]
    for s in S[len(S)-1]:
        St.append(s * u)
        St.append(s * d)
    S.append(St)

puts=[list(map(max, numpy.zeros(len(S[len(S)-1])), [K-x for x in S[len(S)-1]]))]
calls=[list(map(max, numpy.zeros(len(S[len(S)-1])), [x-K for x in S[len(S)-1]]))]

for index in range(len(S)-2,-1,-1):
    puts.append(list(map(max, list(map(max, numpy.zeros(len(S[index])), [K-x for x in S[index]])),
                                        [p*numpy.exp(-r*dt)*puts[len(puts)-1][index1] +
                                         (1-p)*numpy.exp(-r*dt)*puts[len(puts)-1][index1+1]
                                         for index1 in range(len(S[index+1])-1)])))
    calls.append(list(map(max, list(map(max, numpy.zeros(len(S[index])), [x-K for x in S[index]])),
                         [p * numpy.exp(-r * dt) * calls[len(calls) - 1][index1] +
                          (1 - p) * numpy.exp(-r * dt) * calls[len(calls) - 1][index1 + 1]
                          for index1 in range(len(S[index + 1]) - 1)])))

paths = [[S[0][0]]]
for index in range(1,len(S)-1):
    paths = paths + copy.deepcopy(paths)
    for index1 in range(len(S[index])):
        paths[index1].append(S[index][index1])

for path in paths:
    print(paths.index(path))
    plt.plot(range(len(S)-1), path, label=paths.index(path))
plt.show()
