#!/usr/bin/env python
# # -*- coding: utf-8 -*-

""" This module is the main function for inserting symbol and price data into a
    SQLite3 database.  The user manually enters the symbols that they want to see
    in a dictionary, mapping the symbol to some general information.  The user also
    enters the sqlite3 file which they want to create the database in, and if necessary
    the api key from Quandl.
"""

import requests
import pandas as pd
import numpy as np
import json
import datetime
import quandl
import sqlite3
from util import *
from db_setup import *

def main():
    # Sqlite3 db info and Quandl key
    sqlite_file = 'securities_master_db.sqlite'
    api_key = 'Hv95pPh1xQWzt5DFhxS7'

    # Create the sqlite database tables
    db_setup(sqlite_file)

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

    # Insert symbols into the Symbols table
    insert_symbols_table(products, sqlite_file)

    # Generate df_dict and insert price info into Daily_Prices table
    df_dict = generate_df_dict(products, api_key)
    insert_daily_prices_table(products, df_dict, sqlite_file)

if __name__ == '__main__':
    main()
