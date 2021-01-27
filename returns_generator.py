import csv
import os

""" Obtain the lines from our aggregated stock data """
with open('stock_data.csv', 'r') as f:
    lines = f.readlines()

data = []

""" We don't care for the headers so skip the first line """
for line in lines[1:]:
    line = line.strip('\n')

    # we don't care for the data so do not include it
    data.append(line.split(',')[1:])

asset_returns = []

""" Returns is calculated as: (price - prev_price) / prev_price """
for index, element in enumerate(data[1:], 1):
    row_returns = []

    # since each row contains a closing price for each stock
    # we must loop through the row and calculate the return
    # for each stock
    for element_index, _ in enumerate(element):

        price = float(element[element_index])
        prev_price = float(data[index - 1][element_index])

        returns = float((price - prev_price) / prev_price)
        row_returns.append(returns)

    asset_returns.append(row_returns)

stock_dir = 'stock_data/'
headers = os.listdir(stock_dir)

with open('asset_returns.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(os.listdir(stock_dir))
    for i in asset_returns:
        writer.writerow(i)


