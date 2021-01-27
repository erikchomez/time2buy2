import csv
import os
import numpy as np
from pandas import *
import statistics as stats
from scipy.optimize import minimize
from geneticalgorithm import geneticalgorithm as ga
import numpy as np
import math
import pandas as pd
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import matplotlib.pyplot as plt
from pypfopt import CLA, plotting
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
# Read in price data
df = pd.read_csv("stock_data.csv", parse_dates=True, index_col="Date")

# Calculate expected returns and sample covariance
mu = mean_historical_return(df)
S = CovarianceShrinkage(df).ledoit_wolf()

# Optimise for maximal Sharpe ratio
ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()
ef.portfolio_performance(verbose=True)
print(weights)

cla = CLA(mu, S)
cla.max_sharpe()
ax = plotting.plot_efficient_frontier(cla, showfig=True)


plt.show()