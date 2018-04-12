#!/usr/bin/env python
# # -*- coding: utf-8 -*-

""" This module contains all the functions for creating visualizations of the exploratory
    data analysis completed by other modules.
"""

import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns

def plot_dist_ave_return(df, column='ave_return'):
    ''' This takes in a dataframe and column name and then plots the distribution
        of the corresponding data.

        Args: df - dataframe of price and indicator information
              column - column of data to plot

        Return: None - plots the distribution
    '''
    # Create figure
    fig, ax = plt.subplots(figsize=(18,7))

    # Plot column data and label
    ax = sns.distplot(df[column], fit=norm)
    ax.set(title='Distribution of {}'.format(column), xlabel=column)

    plt.show()

def plot_ave_return_by_signal(df):
    ''' This function takes in a dataframe of price, indicator and return information
        and creates a strip plot of each ave_return by signal.

        Args: df - dataframe of return information

        Return: None - plots the returns by signal
    '''
    # Create figure
    fig, ax = plt.subplots(figsize=(18,7))

    # Plot data and label
    ax = sns.stripplot(x='signal', y='ave_return', data=df.sort_values(by='signal'), jitter=True)
    ax.set(title='Ave Return by Signal', xlabel='Signal', ylabel='Ave Return (%)')
    ax.tick_params(axis='x', rotation=90)

    plt.show()

def plot_heatmap(df):
    ''' This function takes in a dataframe of price, indicator and return information
        and creates a heatmap of ave_returns by product and signal.

        Args: df - dataframe of return information

        Return: None - plots the heatmap
    '''
    # Create figure
    fig, ax = plt.subplots(figsize=(18,7))

    # Manipulate dataframe to get ave_return by product and signal combination
    df1 = df.pivot_table(index='product', columns='signal', values='ave_return', aggfunc=np.mean)

    # Plot heatmap
    sns.heatmap(df1, annot=True, fmt=".2%", ax=ax)
    ax.set(title='Ave Return by Product/Signal Combination')
    ax.tick_params(axis='x', rotation=90)
    ax.tick_params(axis='y', rotation=45)

    plt.show()

def plot_heatmap_final(df):
    ''' This function takes in a dataframe of return information and creates a heatmap
        of ave_yearly_return by product and signal.

        Args: df - dataframe of return information

        Return: None - plots the heatmap
    '''
    # Create figure
    fig, ax = plt.subplots(figsize=(10,7))

    # Manipulate dataframe to get ave_yearly_return by produce and signal combination
    df1 = df.pivot_table(index='product', columns='signal', values='ave_yearly_return', aggfunc=np.mean)

    # Plot heatmap
    sns.heatmap(df1, annot=True, fmt=".2%", ax=ax, cbar_kws={'ticks': [0, 5, 10, 15]}, vmin=0, vmax=15)
    ax.set(title='Ave Yearly Return by Product/Signal Combination')

    plt.show()
