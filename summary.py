#!/usr/bin/env python
# # -*- coding: utf-8 -*-

""" This module contains functions for summarizing and visualizing the complete dataframes
    including all price data as well as indicators.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import math

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

def indicator_summary(df):
    ''' This function takes in a dataframe of price and indicator data and returns a
        summary of the number of trades over the time period for all indicators.

        Args: df - the dataframe to summarize indicator data on

        Return: None - prints summary and visualization of trade data
    '''
    # Modify dataframe to include only trade signal columns
    df_signals = df[['vol_bo_long', 'vol_bo_short', 'range_bo_long', 'range_bo_short',
                       'ma20_long', 'ma20_short', 'ma50_long', 'ma50_short', 'ma100_long',
                       'ma100_short', 'bb_long', 'bb_short']]

   # Get strategy names and counts in lists
   signal_names = [signal for signal in df_signals.columns]
   signal_counts = [df_signals[signal].value_counts()[1] for signal in df.signals.columns]

   # Plot histogram of number of trades for different signals
   plt.figure(figsize=(10,7))
   plt.bar(signal_names, signal_counts)
   plt.show()

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
