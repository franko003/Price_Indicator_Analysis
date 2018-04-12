#!/usr/bin/env python
# # -*- coding: utf-8 -*-

""" This module contains all the functions for creating indicators and making them
    individual columns in the cleaned dataframe for further summary, visualization,
    and analysis
"""

import pandas as pd
import numpy as np
from analysis.analysis import *

def vol_bo(row, direction):
    ''' This is a helper function to use in volume breakout column creation.  It takes
        in a row of a dataframe and a direction of trade, and returns 1 if a breakout
        has occured, 0 if not.

        Args: row - row of a dataframe
              direction - 'long' or 'short'

        Return: 1 if volume breakout occured, 0 if not
    '''
    if row['volume'] > (2 * row['20day_ave_vol']):
        if (direction == 'long') and (row['close_gt_prev_h'] > 0.0):
            return 1
        elif (direction == 'short') and (row['close_lt_prev_l'] < 0.0):
            return 1
        else:
            return 0

def range_bo(row, direction):
    ''' This is a helper function to use in range breakout column creation.  It takes
        in a row of a dataframe and a direction of trade, and returns 1 if a breakout
        has occured, 0 if not.

        Args: row - row of a dataframe
              direction - 'long' or 'short'

        Return: 1 if volume breakout occured, 0 if not
    '''
    if direction == 'long':
        if row['high'] > row['20day_high']:
            return 1
        else:
            return 0
    if direction == 'short':
        if row['low'] < row['20day_low']:
            return 1
        else:
            return 0

def ma_signal(row, ma, direction):
    ''' This is a helper function to use in all moving average columns creation.  It takes
        in a row of a dataframe, a length of time and a direction of trade, and returns
        1 if a breakout has occured, 0 if not.

        Args: row - row of a dataframe
              ma - length of time for moving average
              direction - 'long' or 'short'

        Return: 1 if volume breakout occured, 0 if not
    '''
    if direction == 'long':
        if row['close'] > row['ma{}'.format(ma)]:
            return 1
        else:
            return 0
    if direction == 'short':
        if row['close'] < row['ma{}'.format(ma)]:
            return 1
        else:
            return 0

def bb_signal(row, direction):
    ''' This is a helper function to use in all bollinger band column creation.  It takes
        in a row of a dataframe and a direction of trade, and returns 1 if a breakout
        has occured, 0 if not.

        Args: row - row of a dataframe
              direction - 'long' or 'short'

        Return: 1 if volume breakout occured, 0 if not
    '''
    if direction == 'long':
        if row['low'] < row['bb_low']:
            return 1
        else:
            return 0
    if direction == 'short':
        if row['high'] > row['bb_high']:
            return 1
        else:
            return 0

def add_all_indicators(df):
    ''' This function takes in a cleaned dataframe of price information and uses
        the helper functions to add all relevant indicators as columns
        to the dataframe.

        Args: df - cleaned dataframe of price information

        Return: df - cleaned dataframe with added columns for all indicators
    '''
    # All columns for 20day volume breakout indicator
    df['20day_ave_vol'] = df.volume.rolling(window=20, center=False).mean().shift(1)
    df['close_gt_prev_h'] = df['close'] - df['high'].shift(1)
    df['close_lt_prev_l'] = df['close'] - df['low'].shift(1)
    df['vol_bo_long'] = df.apply(lambda row: vol_bo(row, direction='long'), axis=1)
    df['vol_bo_short'] = df.apply(lambda row: vol_bo(row, direction='short'), axis=1)
    df['vol_bo_long'].fillna(value=0, inplace=True)
    df['vol_bo_short'].fillna(value=0, inplace=True)

    # All columns for 20day range breakout indicator
    df['20day_high'] = df.high.rolling(window=20, center=False).max().shift(1)
    df['20day_low'] = df.low.rolling(window=20, center=False).min().shift(1)
    df['range_bo_long'] = df.apply(lambda row: range_bo(row, direction='long'), axis=1)
    df['range_bo_short'] = df.apply(lambda row: range_bo(row, direction='short'), axis=1)

    # All columns for moving average indicators
    df['ma20'] = df['close'].rolling(window=20, center=False).mean()
    df['ma50'] = df['close'].rolling(window=50, center=False).mean()
    df['ma100'] = df['close'].rolling(window=100, center=False).mean()
    df['ma20_long'] = df.apply(lambda row: ma_signal(row, ma=20, direction='long'), axis=1)
    df['ma20_short'] = df.apply(lambda row: ma_signal(row, ma=20, direction='short'), axis=1)
    df['ma50_long'] = df.apply(lambda row: ma_signal(row, ma=50, direction='long'), axis=1)
    df['ma50_short'] = df.apply(lambda row: ma_signal(row, ma=50, direction='short'), axis=1)
    df['ma100_long'] = df.apply(lambda row: ma_signal(row, ma=100, direction='long'), axis=1)
    df['ma100_short'] = df.apply(lambda row: ma_signal(row, ma=100, direction='short'), axis=1)

    # All columns for bollinger band indicators
    df['bb_high'] = df['ma20'] + (2 * df['close'].rolling(window=20, center=False).std())
    df['bb_low'] = df['ma20'] - (2 * df['close'].rolling(window=20, center=False).std())
    df['bb_long'] = df.apply(lambda row: bb_signal(row, direction='long'), axis=1)
    df['bb_short'] = df.apply(lambda row: bb_signal(row, direction='short'), axis=1)

    # All columns for percentage change for timeframe into the future
    df['pct_change_1day'] = df['close'].pct_change()
    df['pct_change_5day'] = df['close'].pct_change(periods=5)
    df['pct_change_10day'] = df['close'].pct_change(periods=10)
    df['pct_change_20day'] = df['close'].pct_change(periods=20)

    return df

def transform_all_products(prod_dict):
    ''' This function takes in the dictionary of all product dataframes and applies
        the add_all_indicators function to each.

        Args: prod_dict - dictionary of name:dataframe key:value pairs for all products

        Return: None - transforms each dataframe with indicators and returns
    '''
    # Iterate through all products in the dict and update
    for prod, df in prod_dict.items():
        add_all_indicators(df)

def create_returns_df(prod_dict, signal_list, timeframe_list=[1, 5, 10, 20]):
    ''' This function takes in a dict of product symbols mapped to dataframes of price and
        indicator information, a list of signals, and a list of timeframes.  It generates
        a new dataframe of products, signals, timeframes, and return statistics.

        Args: prod_dict - dict of product symbols mapped to dataframes of price info
              signal_list - list of strings of signal names
              timeframe_list - list of ints that represent timeframes for returns

        Return: returns_df - dataframe of products, signals, timeframes and return stats
    '''
    # Create empty dataframe in order to insert data
    returns_df = pd.DataFrame(columns=['product', 'signal', 'timeframe',
                              'signal_count', 'signals_per_day', 'ave_return', 'std_return',
                              'min_return', 'max_return', 'q25_return', 'q75_return'])

    # Set variable to keep track of index in dataframe
    i = 0

    # Iterate through each product, for each signal, for each timeframe
    for prod, df in prod_dict.items():
        for signal in signal_list:
            for timeframe in timeframe_list:
                # Insert row of data into dataframe
                returns_df.loc[i] = return_stats(prod, df, signal, timeframe)
                i += 1

    # Drop null values
    returns_df.dropna(inplace=True)

    return returns_df

def filter_strategies(df, thresh=150):
    ''' This function takes in a dataframe of returns and a min trade count and returns
        a filtered dataframe without the bb strategy and only strategies that reach the
        threshold for trade count.

        Args: df - dataframe to filter
              thresh - min number of trades needed to remain in dataframe

        Return: df_final - filtered dataframe
    '''
    # Remove all bb strats
    df_final = df[(df['signal'] != 'bb_long') & (df['signal'] != 'bb_short')]

    # Filter out strategies with trade count below the threshold
    df_final = df_final[df_final['signal_count'] > 150]

    # Create list of strategies to drop based on not having the other direction reach thresh
    drops = [('BTC', 'range_bo_long'), ('XLM', 'ma50_short'), ('XLM', 'ma20_short'),
             ('XMR', 'ma100_long'), ('XMR', 'ma50_long')]

    # Iterate through list and drop rows with those combinations
    for combo in drops:
        df_final.drop(df_final[(df_final['product'] == combo[0]) & (df_final['signal'] == combo[1])].index, inplace=True)

    return df_final

def calculate_combined(df, prod, sig, tf, sig_map):
    ''' This function takes in a dataframe, product, signal, timeframe and signal_map and returns
        both the combined average return and total signal count for each strategy long/short combination.

        Args: df - the cleaned dataframe of price and return information
              prod - product name
              sig - signal name
              tf - timeframe
              sig_map - a dict that maps the long strategy to the short strategy

        Return: combined ave return, total signal count
    '''
    # Get the individual counts, returns for long and short trades
    long_count, long_ave_return = df[(df['product'] == prod) & (df['signal'] == sig) &\
                                     (df['timeframe'] == tf)].iloc[0][['signal_count', 'ave_return']]
    short_count, short_ave_return = df[(df['product'] == prod) & (df['signal'] == sig_map[sig]) &\
                                       (df['timeframe'] == tf)].iloc[0][['signal_count', 'ave_return']]

    # Get total number of trades
    total_count = long_count + short_count

    # Calculate combined ave return
    combined_ave_return = ((long_count / total_count) * long_ave_return) +\
                            ((short_count / total_count) * short_ave_return)

    return combined_ave_return, total_count

def combine_strategies(df):
    ''' This function takes in a dataframe and combines each long/short side of a strategy
        then returns a dataframe of the resulting information.

        Args: df - dataframe to combine strategies for

        Return: df_combined - dataframe of combined strategies
    '''
    # Create a signal map for each strategy pair, list of timeframes and empty list to hold data
    signal_map = {'range_bo_long': 'range_bo_short',
                  'ma20_long': 'ma20_short',
                  'ma50_long': 'ma50_short',
                  'ma100_long': 'ma100_short'}

    timeframes = [1, 5, 10, 20]
    combined = []

    # Iterate through each combination and append the information
    for product in df['product'].unique():
        for timeframe in timeframes:
            for signal in signal_map:
                if signal in list(df[df['product'] == product].signal):
                    combined_return, combined_count = calculate_combined(df, product, signal, timeframe, signal_map)
                    combined.append([product, signal[:-5], timeframe, combined_return, combined_count])

    # Put data into a dataframe and name columns appropriately
    df_combined = pd.DataFrame(combined)
    df_combined.columns = ['product', 'signal', 'timeframe', 'ave_return', 'signal_count']

    return df_combined

def generate_years_map(df_dict):
    ''' This function takes in a dictionary of products:dataframes and finds the number of years
        for each.  It then returns a map of product names to number of years in dataframe.

        Args: df_dict - dict of product names and dataframes

        Return: years_map - dict of product names to number of years in original dataset
    '''
    # Initialize years_map
    years_map = {}

    # Iterate through all products and caluculate number of years (260 trading days), create dict entry
    for prod in df_dict.keys():
        years_map[prod] = df_dict[prod].shape[0] / 260

    return years_map

def year_return(row, years_map):
    ''' This is a helper function that takes in a row of a dataframe as well as a map of product to total
        number of years in the original dataset.  It will be used to calculate an ave_yearly_return
        column of the dataframe.

        Args: row - row of dataframe
              years_map - dict with product:total number of data points, as key:value pair
              trade_days - total number of trading days per year

        Return: ave_yearly_return - ave_yearly_return of the specfic strategy given total data points
    '''
    # Get return per year
    return_per_dp = row['total_return'] / years_map[row['product']]

    return return_per_dp

def add_yearly_return(df, years_map):
    ''' This function takes in a dataframe of return information and a map of products to
        number of years in the dataset, and then adds columns for total_return and ave_yearly_return
        to the dataframe.

        Args: df - dataframe to modify
              years_map - dict of product names to number of years in dataset

        Return: df - adds columns to given dataframe
    '''
    # Add total_return column to dataframe
    df['total_return'] = df['ave_return'] * df['signal_count']

    # Add ave_yearly_return column
    df['ave_yearly_return'] = df.apply(lambda row: year_return(row, years_map), axis=1)

    return df
