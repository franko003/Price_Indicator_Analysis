#!/usr/bin/env python
# # -*- coding: utf-8 -*-

"""" This module contains all the code for initial setup of the sqlite3 database to
    keep all data vendor, product, and price information.  It creates three separate
    tables and links them using table specific ids.
"""

import sqlite3

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

def db_setup(filename):
    # DATA TABLE
    # Initialize variables for file name, table, columns, data types
    sqlite_file = filename
    table_name = 'Data'
    id_col = 'id'
    name_col = 'name'
    url_col = 'url'
    dtype_int = 'INTEGER'
    dtype_text = 'TEXT'

    # Connect to the database file
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    # Create a new table with 3 columns
    c.execute('CREATE TABLE {tn} ({ic} {dti} PRIMARY KEY, {nc} {dtt}, {uc} {dtt})'\
         .format(tn=table_name, ic=id_col, dti=dtype_int, nc=name_col, dtt=dtype_text, uc=url_col))

    # Commit changes and close
    conn.commit()
    conn.close()

    # Add value for Cryptocompare to Data table
    conn, c = connect(sqlite_file)

    c.execute("INSERT INTO {tn} ({ic}, {nc}, {uc}) VALUES (1, 'Cryptocompare', 'https://min-api.cryptocompare.com')"\
          .format(tn=table_name, ic=id_col, nc=name_col, uc=url_col))

    close(conn)

    # Add value for Quandl to Data table
    conn, c = connect(sqlite_file)

    c.execute("INSERT INTO {tn} ({ic}, {nc}, {uc}) VALUES (2, 'Quandl', 'https://docs.quandl.com')"\
          .format(tn=table_name, ic=id_col, nc=name_col, uc=url_col))

    close(conn)

    # Add value for Quantopian to Data table
    conn, c = connect(sqlite_file)

    c.execute("INSERT INTO {tn} ({ic}, {nc}, {uc}) VALUES (3, 'Quantopian', 'https://www.quantopian.com/data')"\
          .format(tn=table_name, ic=id_col, nc=name_col, uc=url_col))

    close(conn)

    # SYMBOLS TABLE
    # Create table for symbol
    # Initialize variables for file name, table, columns, data types
    table_name = 'Symbols'

    data_table = 'Data'
    data_id = 'id'

    id_col = 'id'
    data_id_col = 'data_id'
    symbol_col = 'symbol'
    name_col = 'name'
    sector_col = 'sector'
    exchange_col = 'exchange'
    dtype_int = 'INTEGER'
    dtype_text = 'TEXT'

    # Connect to the database file
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    # Create a new table with 3 columns
    c.execute('CREATE TABLE {tn} ({ic} {dti} PRIMARY KEY,\
                              {dc} {dti},\
                              {sc} {dtt},\
                              {nc} {dtt},\
                              {sec} {dtt},\
                              {ec} {dtt},\
                              FOREIGN KEY ({dc}) REFERENCES {dt} ({dic}))'\
         .format(tn=table_name, ic=id_col, dti=dtype_int, dc=data_id_col, sc=symbol_col,\
                 dtt=dtype_text, nc=name_col, sec=sector_col, ec=exchange_col,\
                 dt=data_table, dic=data_id))

    # Commit changes and close
    conn.commit()
    conn.close()

    # DAILY_PRICES TABLE
    # Create table for daily_price
    # Initialize variables for file name, table, columns, data types
    table_name = 'Daily_Prices'
    symbols_table = 'Symbols'

    id_col = 'id'
    data_id_col = 'data_id'
    symbol_col = 'symbol'
    date_col = 'date'
    open_col = 'open'
    high_col = 'high'
    low_col = 'low'
    close_col = 'close'
    volume_col = 'volume'

    dtype_int = 'INTEGER'
    dtype_text = 'TEXT'
    dtype_real = 'REAL'

    # Connect to the database file
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    # Create a new table with 3 columns
    c.execute('CREATE TABLE {tn} ({ic} {dti} PRIMARY KEY,\
                              {dc} {dti},\
                              {sc} {dtt},\
                              {dtc} {dtt},\
                              {oc} {dtr},\
                              {hc} {dtr},\
                              {lc} {dtr},\
                              {cc} {dtr},\
                              {vc} {dti},\
                              FOREIGN KEY ({sc}) REFERENCES {st} ({sc}))'\
         .format(tn=table_name, ic=id_col, dti=dtype_int, dc=data_id_col, sc=symbol_col,\
                 dtt=dtype_text, dtc=date_col, oc=open_col, dtr=dtype_real, hc=high_col,\
                 lc=low_col, cc=close_col, vc=volume_col, st=symbols_table))

    # Commit changes and close
    conn.commit()
    conn.close()
