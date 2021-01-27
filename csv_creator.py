from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
import numpy as np
import csv

csv_columns = ["0. date", "1. open", "2. high", "3. low", "4. close", "5. volume"]
stock_names = ['UNH']

for i, name in enumerate(stock_names, start=1):
    csv_file = "stock_data/" + name.lower() + ".csv"
    try:
        # Set up list of API keys
        with open("Keys APHAVANTAGE.txt", newline='') as keyfile:
            keys = [i.split("\t")[0] for i in keyfile.readlines()]

        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()

            ts = TimeSeries(key=keys[i//4])
            data, meta_data = ts.get_daily(name, outputsize='full')

            """
            We can adjust the time frame here
            """
            start_date = datetime.strptime("2018-01-01", '%Y-%m-%d').date()
            end_date = datetime.strptime("2019-12-31", '%Y-%m-%d').date()

            for k, v in sorted(data.items()):
                date_to_check = datetime.strptime(k, '%Y-%m-%d').date()

                # check if the date falls in between the time frame we are looking for
                if start_date <= date_to_check <= end_date:
                    # add date to dict
                    v["0. date"] = date_to_check.strftime("%m/%d/%y")
                    # write to csv file
                    writer.writerow(v)


    except IOError:
        print('IO Error')