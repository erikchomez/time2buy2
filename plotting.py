import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sn
import glob


stock_dir = 'stock_data/'
headers = os.listdir(stock_dir)
df = pd.read_csv('stock_data.csv')

""" VOLATILITY PLOTTING """
# volatility_list = []
#
# for stock in headers:
#     symbol_pct_change = df[stock].pct_change().apply(lambda x: np.log(1 + x))
#     variance = symbol_pct_change.var()
#     volatility = np.sqrt(variance * 250)
#
#     volatility_list.append(volatility)
#
# x_pos = [i for i, _ in enumerate(headers)]
#
# plt.bar(x_pos, volatility_list)
# plt.xlabel('Stocks')
# plt.ylabel('Volatility')
# plt.title('Volatility of Each Stock')
# plt.xticks(x_pos, headers)
# plt.show()

""" CORRELATION PLOTTING """
# corr_matrix = df.corr()
# sn.heatmap(corr_matrix, annot=True)
# plt.show()

""" EFFICIENT FRONTIER PLOTTING """
df = pd.read_csv('asset_returns.csv')
NUM_STOCKS = 18
np.random.seed(42)
num_portfolios = 2000
all_weights = np.zeros((num_portfolios, NUM_STOCKS))
ret_arr = np.zeros(num_portfolios)
vol_arr = np.zeros(num_portfolios)
sharpe_arr = np.zeros(num_portfolios)


# CALCULATE USING WEIGHTS FROM GA (algorithm2_max_sharpeRATIO)
GA_obtained_weights_2 = [0.0, 0.0, 0.0, 0.3515022046135446, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                         0.5197106934990161, 0.1287871018874393, 0.0, 0.0, 0.0, 0.0]

GA_obtained_weights_2 = GA_obtained_weights_2 / np.sum(GA_obtained_weights_2)

GA_RET_2 = np.sum((df.mean() * GA_obtained_weights_2 * 252))
GA_VOL_2 = np.sqrt(np.dot(GA_obtained_weights_2.T, np.dot(df.cov() * 252, GA_obtained_weights_2)))


# CALCULATE USING WEIGHTS FROM GA (algorithm3_CONSTRAINED)
GA_obtained_weights_constrained = [0.04979, 0.05622, 0.04508, 0.06191, 0.06075, 0.05818,
                                   0.0488, 0.05815, 0.04945, 0.05812, 0.07005, 0.06061,
                                   0.05012, 0.04885, 0.06278, 0.0407, 0.05943, 0.06103]

GA_obtained_weights_constrained = GA_obtained_weights_constrained / np.sum(GA_obtained_weights_constrained)

GA_RET_constrained = np.sum((df.mean() * GA_obtained_weights_constrained * 252))
GA_VOL_constrained = np.sqrt(np.dot(GA_obtained_weights_constrained.T, np.dot(df.cov() * 252, GA_obtained_weights_constrained)))


# CALCULATE USING WEIGHTS FROM GA (algorithmMaxSharpeRatio)
GA_obtained_weights = [0.08078193, 0.0028061,  0.07370276, 0.06090447, 0.01068368, 0.09862788,
                       0.04883693, 0.05098003, 0.04426998, 0.10034251, 0.07571499, 0.0145882,
                       0.04209858, 0.06844555, 0.00358775, 0.05629702, 0.07125316, 0.09572853]

GA_obtained_weights = GA_obtained_weights / np.sum(GA_obtained_weights)

GA_RET = np.sum((df.mean() * GA_obtained_weights * 252))
GA_VOL = np.sqrt(np.dot(GA_obtained_weights.T, np.dot(df.cov() * 252, GA_obtained_weights)))


# CALCULATE USING WEIGHTS FROM GA (algorithmConstrainedCovariance)
GA_obtained_weights_c = [0.02536624, 0.09666754, 0.05066589, 0.01843563, 0.07613159, 0.05599079,
                         0.24047874, 0.11075257, 0.0190171,  0.0714222, 0.09741402, 0.16461281,
                         0.03270675, 0.08903868, 0.06575599, 0.02605843, 0.02221008, 0.0312724]

GA_obtained_weights_c = GA_obtained_weights_c / np.sum(GA_obtained_weights_c)

GA_RET_c = np.sum((df.mean() * GA_obtained_weights_c * 252))
GA_VOL_c = np.sqrt(np.dot(GA_obtained_weights_c.T, np.dot(df.cov() * 252, GA_obtained_weights_c)))
# GA_SHARPE_c = GA_RET_c / GA_VOL_c

for i in range(num_portfolios):
    # Weights
    weights = np.array(np.random.random(18))
    weights = weights / np.sum(weights)

    # Save weights
    all_weights[i, :] = weights

    # Expected return
    ret_arr[i] = np.sum((df.mean() * weights * 252))

    # Expected volatility
    vol_arr[i] = np.sqrt(np.dot(weights.T, np.dot(df.cov() * 252, weights)))

    # Sharpe ratio
    sharpe_arr[i] = ret_arr[i] / vol_arr[i]

# print('Max sharpe ratio: {}'.format(sharpe_arr.max()))
# print('Location in array: {}'.format(sharpe_arr.argmax()))

# Weights at this location
# print(all_weights[sharpe_arr.argmax(), :])

max_sr_ret = ret_arr[sharpe_arr.argmax()]
max_sr_vol = vol_arr[sharpe_arr.argmax()]

plt.figure(figsize=(12, 8))
plt.scatter(vol_arr, ret_arr, c=sharpe_arr, cmap='viridis')
plt.colorbar(label='Sharpe Ratio')
plt.xlabel('Volatility')
plt.ylabel('Return')
plt.scatter(max_sr_vol, max_sr_ret, c='red', s=50)
plt.scatter(GA_VOL, GA_RET, c='black', s=50)  # (algorithmMaxSharpeRatio)
plt.scatter(GA_VOL_c, GA_RET_c, c='blue', s=50)  # (algorithmConstrainedCovariance)
plt.scatter(GA_VOL_constrained, GA_RET_constrained, c='orange', s=50)  # (algorithm3_CONSTRAINED)
plt.scatter(GA_VOL_2, GA_RET_2, c='green', s=50)  # (algorithm2_max_sharpeRATIO)
plt.show()
