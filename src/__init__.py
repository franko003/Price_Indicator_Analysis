#!/usr/bin/env python
# # -*- coding: utf-8 -*-

""" This is the starting point for the entire program.  Upon running this file, the
    entire workflow is completed, from acquiring, cleaning, and storing the data,
    creating the indicators and exploring the data.
"""

import os

from data.util import *
from data.db_setup import *
from manipulation.manipulation import *
from analysis.analysis import *
from visualization.visualization import *

from dotenv import load_dotenv, find_dotenv

# Load API_KEY from .env file
load_dotenv(find_dotenv())
API_KEY = os.getenv('API_KEY')

if __name__ == "__main__":
    print('')
    print('This program runs an analysis of common technical price indicators on high volume futures and cryptocurrencies')
    print('')

    # Dict of all products with maps to data_id, name, sector, and exchange
    products = {'CL': [2, 'Crude', 'Energy', 'CME'],
                'HO': [2, 'HeatOil', 'Energy', 'CME'],
                'NG': [2, 'NatGas', 'Energy', 'CME'],
                'GC': [2, 'Gold', 'Metals', 'CME'],
                'SI': [2, 'Silver', 'Metals', 'CME'],
                'AD': [2, 'Aussie', 'Forex', 'CME'],
                'CD': [2, 'Canadien', 'Forex', 'CME'],
                'EC': [2, 'Euro', 'Forex', 'CME'],
                'BP': [2, 'Pound', 'Forex', 'CME'],
                'JY': [2, 'Yen', 'Forex', 'CME'],
                'US': [2, '30-yr', 'Treasuries', 'CME'],
                'C': [2, 'Corn', 'Grains', 'CME'],
                'W': [2, 'Wheat', 'Grains', 'CME'],
                'S': [2, 'Soybeans', 'Grains', 'CME'],
                'ES': [2, 'E-mini', 'Indexes', 'CME'],
                'BTC': [1, 'Bitcoin', 'Cryptocurrency', 'CCAgg'],
                'ETH': [1, 'Ethereum', 'Cryptocurrency', 'CCAgg'],
                'XRP': [1, 'Ripple', 'Cryptocurrency', 'CCAgg'],
                'BCH': [1, 'BitcoinCash', 'Cryptocurrency', 'CCAgg'],
                'LTC': [1, 'Litecoin', 'Cryptocurrency', 'CCAgg'],
                'ADA': [1, 'Cardano', 'Cryptocurrency', 'CCAgg'],
                'NEO': [1, 'Neo', 'Cryptocurrency', 'CCAgg'],
                'XLM': [1, 'Stellar', 'Cryptocurrency', 'CCAgg'],
                'EOS': [1, 'EOS', 'Cryptocurrency', 'CCAgg'],
                'XMR': [1, 'Monero', 'Cryptocurrency', 'CCAgg'],}

    # List of all signals explored in the analysis
    signal_list = ['vol_bo_long', 'vol_bo_short',
                   'range_bo_long', 'range_bo_short',
                   'ma20_long', 'ma20_short',
                   'ma50_long', 'ma50_short',
                   'ma100_long', 'ma100_short',
                   'bb_long', 'bb_short']

    # Acquire data from Quandl and Cryptocompare APIs
    print('.....Acquiring and cleaning data from Quandl and Cryptocompare.....')
    df_dict = generate_df_dict(products, API_KEY)
    print('')

    # Create SQLite3 database to store price information
    sqlite_file = input('Provide a name for the database file (ex. my_new_db.sqlite): ')
    print('')
    print('.....Creating the SQLite3 database tables.....')
    db_setup(sqlite_file)
    print('')

    # Insert symbols and price data into Symbols and Daily_Prices tables
    print('.....Inserting data into Symbols table.....')
    insert_symbols_table(products, sqlite_file)
    print('')
    print('.....Inserting data into Daily_Prices table.....')
    insert_daily_prices_table(products, df_dict, sqlite_file)
    print('')

    # Allow user to use check_outlier function on specified product
    choice = input('Do you want to print a chart for a specific product to check for outliers? (Y or N)\n')
    print('')

    if choice == 'Y':
        product = input('Enter product symbol (ex. BTC, CL, C, ES): ')
        print('')
        check_outliers(df_dict[product])
        print('')

    # Transform data into the indicators and returns needed for analysis
    print('.....Transforming data.....')
    transform_all_products(df_dict)
    print('')

    # Allow user to plot the returns of a selected product, signal, timeframe combination
    choice = input('Do you want to plot a returns chart and see summary stats for a product/signal/timeframe combination? (Y or N)\n')
    print('')

    if choice == 'Y':
        product = input('Enter product symbol (ex. BTC, CL, C, ES): ')
        print('')
        signal = input('Enter trade signal (ex. range_bo_long, ma50_short, bb_long): ')
        print('')
        timeframe = int(input('Enter timeframe (ex. 1, 5, 10, 20): '))
        print('')
        plot_returns(df_dict[product], signal, timeframe)
        print('')
        stats = return_stats(product, df_dict[product], signal, timeframe)

        # Print summary
        print('Total number of signals: {}'.format(stats[3]))
        print('Number of signals per trading day: {0:.2f}'.format(stats[4]))
        print('Average return: {:.2%}'.format(stats[5]))
        print('Standard deviation of return: {:.2%}'.format(stats[6]))
        print('Minimum return: {:.2%}'.format(stats[7]))
        print('Maximum return: {:.2%}'.format(stats[8]))
        print('25th percentile return: {:.2%}'.format(stats[9]))
        print('75th percentile return: {:.2%}'.format(stats[10]))
        print('')

    # Final data transformation to create returns dataframe
    print('.....Final data transformation.....')
    returns_df = create_returns_df(df_dict, signal_list)
    print('')

    # Data exploration
    print('.....Distribution plot of all ave_returns.....')
    plot_dist_ave_return(returns_df)
    print('')

    print('.....Strip plot of ave_return by signal.....')
    plot_ave_return_by_signal(returns_df)
    print('')

    print('.....Heatmap of ave_return by product/signal combination.....')
    plot_heatmap(returns_df)
    print('')

    # Filter data and combine strategies
    print('.....Filtering trade strategies.....')
    df_final = filter_strategies(returns_df)
    print('')

    print('.....Combining trade strategies.....')
    df_combined = combine_strategies(df_final)
    print('')

    print('.....Calculating average yearly returns.....')
    years_map = generate_years_map(df_dict)
    df_yearly_return = add_yearly_return(df_combined, years_map)
    print(df_yearly_return.head())
