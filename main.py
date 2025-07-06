from helper import *
import os

if __name__ == "__main__":
    config = import_json('./config/', 'settings')
    #%% Portfolio composition analysis
    df = acquire_portfolio(config)
    plot_portfolio(df, config)

    #%% Investment analysis
    record = analyze_transactions(config)
    plot_transactions(record, config)

