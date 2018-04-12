#!/usr/bin/env python
# # -*- coding: utf-8 -*-

""" This module contains all the functions for exploratory analysis of the price
    and indicator dataframes.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import math
import datetime

def plot_returns(df, signal, timeframe):
    ''' This function takes in a dataframe of price and indicator information, as well as the
        signal and timeframe for desired analysis.  It then plots a line chart of the percent
        returns over the given timeframe, for each signal in the dataset.

        Args: df - dataframe of price and indicator information
              signal - string name of the desired indicator signal
              timeframe - int of number of days into the future to show returns for (1, 5, 10, 20)

        Return: None - plots the input information
    '''
    # Get the relevant data from the dataframe and set timeframe string
    df_signal = df[df[signal] == 1]
    returns = 'pct_change_{}day'.format(timeframe)

    # Find out if signal is long or short and calculate the mean
    is_long = re.search('long$', signal)
    is_short = re.search('short$', signal)

    if is_long:
        mean_pc = df_signal[returns].mean()
    elif is_short:
        mean_pc = -1.0 * df_signal[returns].mean()
    else:
        return 'No such trading strategy'

    # Plot the 1day returns
    plt.figure(figsize=(14,7))

    if is_long:
        plt.plot(df_signal.index, df_signal[returns], label='Daily Returns')
    else:
        plt.plot(df_signal.index, -1.0 * (df_signal[returns]), label='Daily Returns')

    plt.plot(df_signal.index, [mean_pc]*len(df_signal[returns]),
                color='r', linestyle='--', label='Average Return')

    plt.title('Returns\nStrategy: {}\nTimeframe: {}'.format(signal, returns))
    plt.xlabel('Date')
    plt.ylabel('{}'.format(returns))
    plt.legend(loc='best')

    plt.show()
    print('Average return: {}'.format(mean_pc))
    print('Number of trades: {}'.format(len(df_signal)))

def return_stats(product, df, signal, timeframe=1):
    ''' This function takes in a product, dataframe of price and indicator information, as well as a
        trading strategy signal and a timeframe, then returns important statistics about the
        percentage returns of the strategy over the total dataset, which is used for further analysis.

        Args: df - dataframe of price and indicator information
              signal - string name of the desired indicator signal
              timeframe - int of number of days into the future to show returns for (1, 5, 10, 20)

        Return: list [product, signal, timeframe, signals per day, mean return, std return, min, max, 25%, 75%]
    '''
    # Get the relevant data from the dataframe and set timeframe string
    df_signal = df[df[signal] == 1]
    returns = 'pct_change_{}day'.format(timeframe)

    # Find out if signal is long or short and calculate the mean
    is_long = re.search('long$', signal)
    is_short = re.search('short$', signal)

    if is_long:
        mean_pc = df_signal[returns].mean()
    elif is_short:
        mean_pc = -1.0 * df_signal[returns].mean()
    else:
        return 'No such trading strategy'

    # Calculate return statistics
    signal_count = len(df_signal)
    signals_per_day = len(df_signal) / len(df)
    std_pc = df_signal[returns].std()
    min_pc = df_signal[returns].min()
    max_pc = df_signal[returns].max()
    q25_pc = df_signal[returns].quantile(q=0.25)
    q75_pc = df_signal[returns].quantile(q=0.75)

    return [product, signal, timeframe, signal_count, signals_per_day, mean_pc, std_pc, min_pc, max_pc, q25_pc, q75_pc]

def price_volatility_summary(df):
    ''' This function takes in a dataframe of price and indicator info and returns a
        summary of average monthly price data vs average monthly volatility.

        Args: df - dataframe to summarize

        Return: None - prints summary of price vs volatility on monthly basis
    '''
    cpy = df.copy()

    # Add 20day historical volatility as a column to the dataframe
    cpy['20day_hist_vol'] = math.sqrt(252) * cpy['pct_change_1day'].rolling(window=20, center=False).std()

    # Get historical vol and price data grouped by year and month
    hist_vol_monthly = cpy['20day_hist_vol'].groupby([cpy.index.year, cpy.index.month]).mean()
    price_monthly = cpy['close'].groupby([cpy.index.year, cpy.index.month]).mean()

    # Scatter plot of the data
    plt.figure(figsize=(10,7))

    plt.scatter(hist_vol_monthly, price_monthly)

    plt.show()

def indicator_summary(df):
    ''' This function takes in a dataframe of price and indicator data and returns a
        summary of the number of trades over the time period for all indicators.

        Args: df - the dataframe to summarize indicator data on

        Return: None - prints summary and visualization of trade data
    '''
    # Modify dataframe to include only trade signal columns
    df_signals = df[['vol_bo_long', 'vol_bo_short', 'range_bo_long', 'range_bo_short',
                     'ma20_long', 'ma20_short', 'ma50_long', 'ma50_short' 'ma100_long',
                     'ma100_short', 'bb_long', 'bb_short']]

    # Get strategy names and counts in lists
    signal_names = [signal for signal in df_signals.columns]
    signal_counts = [df_signals[signal].value_counts()[1] for signal in df_signals.columns]

    # Plot histogram of number of trades for different signals
    plt.figure(figsize=(10,7))
    plt.bar(signal_names, signal_counts)
    plt.show()

def price_summary(df):
    ''' This function takes in a dataframe and returns a summary of the overall price
        data, including time period, descriptive statistics, and visualizations.

        Args: df - dataframe to show a summary for

        Return: None - prints summary and visualizations
    '''
    # Get the range, number of days, data points, start date and end date
    date_range = (df.index[-1] - df.index[0]).days
    start_date = df.index[0].strftime('%m-%d-%y')
    end_date = df.index[-1].strftime('%m-%d-%y')
    data_points = len(df.close)

    print('This dataset is comprised of {} calendar days'.format(date_range))
    print('from {} to {}'.format(start_date, end_date))
    print('with {} total daily data points.'.format(data_points))

    # Plot box and whisker of descpritive statistics
    df.boxplot(column='close', sym='o', whis='range', return_type='axes')

    # Calculate descriptive statistics and print summary
    mean = df['close'].mean()
    median = df['close'].median()
    std = df['close'].std()
    low = df['low'].min()
    high = df['high'].max()
    price_range = high - low

    print('The mean price over that timeframe was: {0:.2f}'.format(mean))
    print('The median price over that timeframe was: {}'.format(median))
    print('The standard deviation was: {0:.2f}'.format(std))
    print('The overall price range was: {0:.2f}, from a low of {l} to a high of {h}'\
        .format(price_range, l=low, h=high))
