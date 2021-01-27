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
from pypfopt import objective_functions
from pypfopt import expected_returns

# Read in price data
df = pd.read_csv("stock_data.csv", parse_dates=True, index_col="Date")

# Calculate expected returns and sample covariance
mu = mean_historical_return(df)
S = CovarianceShrinkage(df).ledoit_wolf()
# Must have no weight bounds to allow shorts
ef = EfficientFrontier(mu, S, weight_bounds=(0, 1))
ef.add_objective(objective_functions.L2_reg)
ef.efficient_return(target_return=0.05, market_neutral=False)
weights = ef.clean_weights()
print(weights)