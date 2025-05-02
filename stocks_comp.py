#%% 
import yfinance as yf
import numpy as np
import matplotlib.pylab as plt
import pandas as pd
from helper import *
import json
import datetime

#%% Import stock record

json_path = "./transactions/record.json"
f = open(json_path)
rec = json.load(f)

#%% Plot and read the json

for sel_stock_name in rec.keys():
    print(sel_stock_name)
    name_stock = rec[sel_stock_name]['Name']
    entry_value = np.round(np.float64(rec[sel_stock_name]['Entry_val']),3)
    entry_date = rec[sel_stock_name]['Entry_date']
    entry_date = datetime.datetime.strptime(entry_date, "%d/%m/%Y").strftime("%Y-%m-%d") # Convert the format
    quantities_en = np.int64(rec[sel_stock_name]['Quantities_en'])
    currency = rec[sel_stock_name]['Currency']

    

    period = "6mo"
    df = yf.download(sel_stock_name, period=period)
    print(df)

    actual_value = np.round(df[('Adj Close')].iloc[-1],3)
    win_loss = np.round(quantities_en*actual_value - quantities_en*entry_value,3)

    fig = plt.figure()
    plt.plot(df.index, df[('Adj Close')], label=sel_stock_name, marker='s', color = 'midnightblue',  ms = 4)

    # entry_value = np.round(df.loc[df.index == entry_date, ('Adj Close')].iloc[0],2)
    plt.axhline(entry_value, color='r', linestyle='--')
    plt.axvline(pd.to_datetime(entry_date), color='r', linestyle='--')
    plt.plot(pd.to_datetime(entry_date), entry_value, label=sel_stock_name, marker='x')

    # Add labels and title
    plt.grid(axis='y')
    plt.xlabel('Date')
    plt.ylabel(f'Price {currency}')
    plt.title(f'Historical price {name_stock} \n Win / Loss {win_loss} {currency}')
    plt.legend([sel_stock_name, f'Entry value {entry_value} {currency}'])

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Show plot
    plt.tight_layout()

    fig.savefig('./charts/'+ name_stock +'.png')
    # plt.show()

