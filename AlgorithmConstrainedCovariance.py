import csv
import os
import numpy as np
from pandas import *
import statistics as stats
from scipy.optimize import minimize
from geneticalgorithm import geneticalgorithm as ga
import numpy as np
import math
#Return computation
original = 0
with open('stock_data.csv', 'r', newline='') as csvfile:
    original = list(csv.reader(csvfile))
    for row in original[1:]:
        for column in range(1,len(row)):
            row[column] = float(row[column])
date_order = [ r[0] for r in original[1:] ]
returns = [ r[1:] for r in original[1:] ]

for i in range(len(returns)-1,0, -1):
    for j in range(len(returns[i])):
        returns[i][j] = (returns[i][j]  - returns[i-1][j])/returns[i-1][j]

del returns[0]

#############Precompute######################
#Returns
st_means = []
st_variances = []
for i in range(len(returns[0])):
    to_evaluate =  [j[i] for j in returns ]
    st_means.append(stats.mean(to_evaluate))
    st_variances.append(stats.variance(to_evaluate))
#Covariance
from copy import deepcopy
return_copy = deepcopy(returns)

data_entries = len(return_copy) -1
for i in range(len(return_copy)):
    for j in range(len(return_copy[0])):
        return_copy[i][j] -= st_means[j]
        return_copy[i][j] /= data_entries
covariance = np.dot(np.matrix(return_copy).T,np.matrix(return_copy))
#############EEEEEEEENNNNNNNNNDDDDDDDDDDDDD######################


def sharpe(weight: list):
    return sum(np.multiply(weight, st_means))/ math.sqrt(sum(np.multiply(weight, st_variances)))

def algorithm(weight: list) ->float:
    return  np.array(weight)@np.array(covariance)@np.array(weight) + penaltyCount(weight)

#Only penalty since 2 types of constraints

#Need to have 100% of total
def con1(x:list) -> float:
    return abs(1 - sum(x))

#each should be [0,1]  Each adds extra terms
def con2(x:list) -> int:
    return sum([0 if i > 0 and 1 <= i else 1 for i in x]) 

desired_expectancy_ratio = 0.05#realistic
#each should be [0,1]  Each adds extra terms
def con3(x:list) -> int:
    return abs(desired_expectancy_ratio - sum(np.multiply(x,st_means)) )

def penaltyCount(x):
    return (100*con1(x))**2 + 100*(con2(x)**2) + (100*con3(x))**2

itermax = 360

varbound=np.array([[0,1]]*len(returns[0]))
algorithm_param = {'max_num_iteration': itermax ,\
                   'population_size':1000,\
                   'mutation_probability':0.3,\
                   'elit_ratio': 0.01,\
                   'crossover_probability': 0.5,\
                   'parents_portion': 0.3,\
                   'crossover_type':'uniform',\
                   'max_iteration_without_improv':100}

model=ga(function=algorithm,\
            dimension=len(returns[0]),\
            variable_type='real',\
            variable_boundaries=varbound,\
            algorithm_parameters=algorithm_param)

model.run()

convergence=model.report
solution = model.output_dict
print(sum(solution['variable']))
print(sorted(list(zip(solution['variable'],original[0][1:])), key = lambda x: x[0]))
