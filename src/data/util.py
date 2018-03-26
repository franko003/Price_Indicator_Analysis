#!/usr/bin/env python
# # -*- coding: utf-8 -*-

""" This module contains all the functions used in the main.py file.  It takes in a
    list of products and creates dataframes of each, with the name as the key and daily
    price information as the value.  These functions also put the data into clean
    format in order to then insert both the product symbols and the price data into
    a SQLite3 database.
"""

import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import datetime
import quandl
import sqlite3

def create_df_crypto(symbol, curr='USD', limit=2000):
    ''' This function takes in a symbol of a cryptocurrency to be
        used with the Cryptocompare API, and returns a formatted dataframe
        for later processing.

        Args: symbol - cryptocurrency symbol
              curr - currency to report in (default USD)
              limit - max number of data points (default 2500)

        Return: df - dataframe of daily price info for symbol
    '''
    # Set url and params for the call to Cryptocompare API
    url = 'https://min-api.cryptocompare.com/data/histoday'
    params = {'fsym': symbol, 'tsym': curr, 'limit': limit}

    # Call API for symbol and put data into pandas dataframe
    response = requests.get(url, params=params)
    data = response.json()['Data']
    df = pd.DataFrame(data)

    # Add date column and set to index
    df['Date'] =[datetime.date.fromtimestamp(d) for d in df.time]
    df = df[['open', 'high', 'low', 'close', 'volumeto', 'Date']]
    df.set_index('Date', inplace=True)

    # Rename volumeto column
    df.rename(columns={'volumeto': 'volume'}, inplace=True)

    return df

def create_df_quandl(symbol, api_key):
    ''' This function takes in a symbol of a futures contract to be used
        with the Quandl API as well as the API key, and returns a formatted
        dataframe for processing.

        Args: symbol - a symbol for a continuous futures contract
              api_key - Quandl API key

        Return: df - dataframe for daily price info for symbol
    '''
    # Quandl API call which puts price data into dataframe
    df = quandl.get('SCF/CME_{s}1_FW'.format(s=symbol), authtoken=api_key)

    # Drop open interest column and rename Settle column
    df.drop(['Prev. Day Open Interest'], axis=1, inplace=True)
    df.rename(columns={'Open': 'open',
                      'High': 'high',
                      'Low': 'low',
                      'Settle': 'close',
                      'Volume': 'volume'}, inplace=True)
    return df

def clean_df_crypto(df, volume_thresh=1000000):
    ''' This function takes in a dataframe and a volume threshold and returns a filtered
        dataframe from the first data point that achieves the threshold.  This is written
        to be used specifically with the cryptocurrency dataframes.

        Args: df - dataframe to be filtered on volume
              volume_thresh - min volume to reach before using data in the dataframe

        Return df - the filtered dataframe with only points after the volume threshold is hit
    '''
    # Find start_date and filter df
    start_date = df.index[df.volume > volume_thresh].tolist()[0]
    df = df[start_date:]

    return df

def replace_df_zeros(df):
    ''' This function takes in a dataframe of price information, finds all zero values
        for the 'volume' column and replaces them with the mean volume of the dataset.

        Args: df - dataframe of price information

        Return: df - cleaned dataframe with no zero volume entries
    '''
    df['volume'].replace(0.0, df['volume'].mean(), inplace=True)

    return df

def check_outliers(df):
    ''' This function finds all closing price points that are more than 3 stds away from
        the mean and plots them on a line graph of all the data.  This can be used to see
        if these points are truly outliers.

        Args: df - dataframe to be checked for outliers

        Return: None - shows a graph of the price data series with annotations for outliers
    '''
    # Use a copy of the dataframe
    cpy = df.copy()
    # Create range of values that are more than 3 stds away from mean
    cpy['stds_from_mean'] = ((cpy['close'] - cpy['close'].mean()).apply(abs)) / cpy['close'].std()
    locs_gt_3std = [cpy.index.get_loc(x) for x in cpy.index[cpy['stds_from_mean'] > 3.0]]

    # Plot the price data, highlighting the outliers
    plt.figure(figsize=(15,10))
    plt.plot(cpy.index, cpy.close, linestyle='solid', markevery=locs_gt_3std,
                marker='o', markerfacecolor='r', label='Outliers')

    # Apply title, legend and labels
    plt.title('Closing Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()

    plt.show()

    # Print out description
    print('Number of data points: {}'.format(len(cpy.index)))
    print('Number of outliers: {}'.format(len(locs_gt_3std)))

def generate_df_dict(product_dict, api_key=None):
    ''' This function takes in a dict of product symbols mapped to
        information about the product  and a Quandl API key and returns
        a dict object with the symbols as keys and a dataframe of price
        info as values.

        Args: product_dict - a dict of symbols for products with maps to
                             a list of info
              api_key - Quandl API key

        Return: df_dict - a dictionary of symbols mapped to dataframes
                          of price info
    '''
    df_dict = {}

    # Iterate through list
    for product, info in product_dict.items():
        # Determine what dataframe creator to use
        if info[0] == 1:
            df = create_df_crypto(product)
            df = clean_df_crypto(df)
            df = replace_df_zeros(df)
        if info[0] == 2:
            df = create_df_quandl(product, api_key)
            df = replace_df_zeros(df)

        df_dict[product] = df

    return df_dict

def insert_symbols_table(product_dict, sqlite_file, table_name='Symbols'):
    ''' This function takes in a dict of product symbols mapped to
        information about the product.  It also takes in a sqlite file and then
        uses the info to insert all symbols in the dict into the Symbols
        table of the database.

        Args: product_dict - a dict of symbols for products with maps to
                             a list of info
              sqlite_file - file for the database to write to
              table_name - default to 'Symbols' for this function

        Return: None - nothing explicit but inserts info into the database
    '''
    # Create the column name list for database insertion
    cols = ['data_id', 'symbol', 'name', 'sector', 'exchange']

    # Open a connection to the database
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    # Iterate through all symbols of product_dict
    for symbol, s_info in product_dict.items():
        # Set params and insert row into database
        params = (s_info[0], symbol, s_info[1], s_info[2], s_info[3])
        c.execute("INSERT INTO {tn} ({c0}, {c1}, {c2}, {c3}, {c4}) VALUES (?, ?, ?, ?, ?)"\
            .format(tn=table_name, c0=cols[0], c1=cols[1], c2=cols[2],\
            c3=cols[3], c4=cols[4]), params)

    # Close connection to database
    conn.commit()
    conn.close()

def insert_daily_prices_table(product_dict, df_dict, sqlite_file, table_name='Daily_Prices'):
    ''' This function takes in a 2 dicts, one with product keys mapping
        to info about the product and the other with product keys mapping
        to a dataframe a daily price information.  It also takes in a sqlite
        file and then uses the info to insert all rows into the Daily_Prices
        table of the database.

        Args: product_dict - a dict of symbols for products with maps to
                             a list of info
              df_dict - dict of dataframes with futures symbols and price data
              sqlite_file - file for the database to write to
              table_name - default to 'Daily_Prices' for this function

        Return: None - nothing explicit but inserts info into the database
    '''
    # Create the column name list for database insertion
    cols = ['data_id', 'symbol', 'date', 'open', 'high', 'low', 'close', 'volume']

    # Open a connection to the database
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    # Iterate through all symbols and then the dataframe to get all price data
    for symbol, df in df_dict.items():
        data_id = product_dict[symbol][0]
        for i, row in df.iterrows():
            date = i.strftime('%Y-%m-%d')
            # Set params and insert row into database
            params = (data_id, symbol, date, row.open, row.high, row.low, row.close, row.volume)
            c.execute("INSERT INTO {tn} ({c0}, {c1}, {c2}, {c3}, {c4}, {c5}, {c6}, {c7}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"\
                .format(tn=table_name, c0=cols[0], c1=cols[1], c2=cols[2], c3=cols[3], c4=cols[4],\
                c5=cols[5], c6=cols[6], c7=cols[7]), params)

    # Close connection to database
    conn.commit()
    conn.close()
