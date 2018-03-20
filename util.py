import requests
import pandas as pd
import numpy as np
import json
import datetime
import quandl

# All functions used in creating and populating master database

def connect(sqlite_file):
    ''' This function takes in a sqlite db files, returns a connection
        and a cursor.

        Args: sqlite_file - a sqlite db file name

        Return: conn - connection to the sqlite file
                c - cursor in the connection
    '''
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    return conn, c

def close(conn):
    ''' This function takes in a connection to a sqlite db file, then
        commits changes and closes the connection.

        Args: conn - connection to a sqlite db

        Return: None - commits changes and closes the connection
    '''
    conn.commit()
    conn.close()

def create_df_crypto(symbol, curr='USD', limit=2500):
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

def generate_df_dict(product_dict, api_key):
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
        if info[0] == 2:
            df = create_df_quandl(product, api_key)

        df_dict[product] = df

    return df_dict

################################################################################

# Insert all symbols for Quandl data into Symbols table
def insert_symbols_table(sector_map, name_map, sqlite_file):
    ''' This function takes in two dicts, one mapping sectors to specific futres contracts,
        the other mapping symbols to full names.  It also takes in a sqlite file and then
        uses the info to insert all rows into the Symbols table of the database

        Args: sector_map - dict that maps breaks all futures into sectors
              name_map - dict that maps symbols to full names of the products
              sqlite_file - file for the database to write to

        Return: None - nothing explicit but inserts info into the database
    '''
    # Since this is specifc Quandl data all from CME exchange we can set these two params
    data_id = 2
    exchange = 'CME'

    # Create the column name list for database insertion
    table_name = 'Symbols'
    cols = ['data_id', 'symbol', 'name', 'sector', 'exchange']

    # Open a connection to the database
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    # Iterate through all symbols to get sector and name
    for sector, s_list in sectors.items():
        for symbol in s_list:
            # Set params and insert row into database
            params = (data_id, symbol, name_map[symbol], sector, exchange)
            c.execute("INSERT INTO {tn} ({c0}, {c1}, {c2}, {c3}, {c4}) VALUES (?, ?, ?, ?, ?)"\
                      .format(tn=table_name, c0=cols[0], c1=cols[1], c2=cols[2],\
                             c3=cols[3], c4=cols[4]), params)

    # Close connection to database
    conn.commit()
    conn.close()

# Insert all price data into Daily_Prices database
def insert_daily_prices_table(df_dict, sqlite_file):
    ''' This function takes in a dict of dataframes, with each key being a different futures
        contract, and the value is the price data.  It also takes in a sqlite file and then
        uses the info to insert all rows into the Daily_Prices table of the database

        Args: df_dict - dict of dataframes with futures symbols and price data
              sqlite_file - file for the database to write to

        Return: None - nothing explicit but inserts info into the database
    '''
    # Since this is specifc Quandl data we can set data_id param
    data_id = 2

    # Create the column name list for database insertion
    table_name = 'Daily_Prices'
    cols = ['data_id', 'symbol', 'date', 'open', 'high', 'low', 'close', 'volume']

    # Open a connection to the database
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    # Iterate through all symbols and then the dataframe to get all price data
    for symbol, df in df_dict.items():
        for i, row in df.iterrows():
            date = i.strftime('%Y-%m-%d')
            # Set params and insert row into database
            params = (data_id, symbol, date, row.open, row.high, row.low, row.close, row.volume)
            c.execute("INSERT INTO {tn} ({c0}, {c1}, {c2}, {c3}, {c4}, {c5}, {c6}, {c7}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)".format(tn=table_name, c0=cols[0], c1=cols[1], c2=cols[2], c3=cols[3], c4=cols[4], c5=cols[5], c6=cols[6], c7=cols[7]), params)

    # Close connection to database
    conn.commit()
    conn.close()
