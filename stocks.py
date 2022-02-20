import yfinance as yf
import pandas as pd
import json
import dataChecker as dc

stocks_file = open("./data/stock_list.json")
stocks_dict = json.load(stocks_file)

def get_daily_data(ticker = 'Airtel', start_date = "2003-01-01", end_date = '2021-12-31'):
    file_name = ticker+".csv"
    if file_name in dc.csv_files:
        stock_data = pd.read_csv("./data/"+file_name)
        stock_data.set_index(['Date'], inplace = True)
    else:
        stock_data = yf.download(stocks_dict[ticker], start = start_date, end= end_date )
        stock_data.to_csv("./data/"+ticker+".csv")
        dc.csv_files.append(ticker+".csv")
    return stock_data

stocks_file.close()
