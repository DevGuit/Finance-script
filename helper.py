import resources
import pandas as pd
import matplotlib.pyplot as plt
import os
import yfinance as yf
import numpy as np
import json
import datetime
"""
Insert all the functions used in main
"""
#%% Functions

def acquire_portfolio(config):
    """
    Acquire the portfolio from the specified path.
    """
    portfolio_path = os.path.join('.\\',config['input_dir'],config['sel_dir'], 'portfolio.csv')
    print(f'Acquiring portfolio from {portfolio_path}')

    df = pd.read_csv(portfolio_path, delimiter=',', decimal=',')
    df = df.rename({'Aantal': 'Quantity', 'Slotkoers': 'Actual Price', 'Lokale waarde': 'Price in USD/EUR', 'Waarde in EUR': "Price in EUR"}, axis='columns')
    df = df.sort_values(by='Price in EUR', ascending=False)

    print(df)
    print('Portfolio acquired')
    return df

def plot_portfolio(df, config):
    """
    Plot the portfolio composition.
    """
    output_dir = os.path.join('.\\',config['output_dir'],config['sel_dir'])
    save_path = os.path.join(output_dir, 'piechart.png')
    os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(20, 8))
    labels = [f'{prod} (€{val:,.2f})' for prod, val in zip(df['Product'], df['Price in EUR'])]
    wedges, texts, autotexts = ax.pie(df['Price in EUR'], autopct='%1.1f%%', startangle=90, counterclock=False)
    ax.legend(wedges, labels, title="Products", loc="center left", bbox_to_anchor=(0.8, 0, 0.5, 1))
    plt.title('Portfolio assets')
    plt.axis('equal')  
    plt.savefig(save_path)

def analyze_transactions(config):
    """
    Analyze the transactions from the JSON file.
    """
    json_path = os.path.join('.\\',config['input_dir'],config['sel_dir'], 'record.json')
    print(f'Acquiring transactions from {json_path}')
    
    f = open(json_path)
    rec = json.load(f)
    
    print('Transactions acquired')
    return rec

def plot_transactions(rec, config):
    """
    Plot the transactions from the record.
    """
    output_dir = os.path.join('.\\', config['output_dir'], config['sel_dir'], 'charts')
    os.makedirs(output_dir, exist_ok=True)

    for sel_stock_name in rec.keys():
        print(sel_stock_name)
        name_stock = rec[sel_stock_name]['Name']
        entry_value = np.round(np.float64(rec[sel_stock_name]['Entry_val']),3)
        entry_date = rec[sel_stock_name]['Entry_date']
        entry_date = datetime.datetime.strptime(entry_date, "%d/%m/%Y").strftime("%Y-%m-%d") # Convert the format
        quantities_en = np.int64(rec[sel_stock_name]['Quantities_en'])
        currency = rec[sel_stock_name]['Currency']

        period = "16mo"
        df = yf.download(sel_stock_name, period=period)
        print(df)

        actual_value = np.round(df[('Close')].iloc[-1],3)
        win_loss = np.round(quantities_en*actual_value - quantities_en*entry_value,3)

        fig = plt.figure()
        plt.plot(df.index, df[('Close')], label=sel_stock_name, marker='s', color = 'midnightblue',  ms = 4)

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

        save_path = os.path.join(output_dir, f'{name_stock}.png')
        fig.savefig(save_path)
        # plt.show()

def import_json(dir_target, json_name):
    inp_out = resources.json_dict.InputOutput(dir_target, json_name)
    print(f'Importing {json_name}.json from {dir_target}')
    var_dict = inp_out.json_to_dict()
    
    return var_dict

def export_json(dir_target, dict_name, var_dict):
    inp_out = resources.json_dict.InputOutput(dir_target, dict_name, var_dict)
    print(f'Exporting {dict_name}.json in {dir_target}')
    inp_out.dict_to_json()