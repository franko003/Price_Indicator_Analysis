#!/usr/bin/env python
# # -*- coding: utf-8 -*-

""" This module contains all the functions for creating indicators and making them
    individual columns in the cleaned dataframe for further summary, visualization,
    and analysis
"""

import pandas as pd
import numpy as np

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
    df['ma50_long'] = df.apply(lambda row: ma_signal(row, ma=50, direction='short'), axis=1)
    df['ma100_long'] = df.apply(lambda row: ma_signal(row, ma=100, direction='long'), axis=1)
    df['ma100_long'] = df.apply(lambda row: ma_signal(row, ma=100, direction='short'), axis=1)

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
