#!/usr/bin/env python
# # -*- coding: utf-8 -*-

""" This module contains all the functions for exploratory analysis of the price
    and indicator dataframes.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re


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

''' quick script to create the last dataframe.  Need to put into a function '''
# Set variable to keep track of index in dataframe
i = 0

# Iterate through each product, for each signal, for each timeframe
for prod, df in prod_dict.items():
    for signal in signal_list:
        for timeframe in timeframe_list:
            # Insert row of data into dataframe
            returns_df.loc[i] = return_stats(prod, df, signal, timeframe)
            i += 1
