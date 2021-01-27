import csv
import os
from collections import defaultdict
# implementing algorithm from medium article
# data prep: aggregating stock data
stock_dir = 'stock_data/'
headers = ['Date'] + os.listdir(stock_dir)
with open('stock_data.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    row_data = defaultdict(list)
    for file in os.listdir(stock_dir):
        print(file)
        with open(os.path.join(stock_dir, file), newline='') as stock_data:
            reader = csv.DictReader(stock_data)
            for row in reader:
                # print('\t', row['0. date'], row['4. close']) # debug output
                row_data[row['0. date']].append((file, row['4. close']))
    for k, v in sorted(row_data.items(), key=lambda x: x[0][6:] + x[0][:6]):
        writer.writerow(dict([('Date',k)]+v))