# Price_Indicator_Analysis

Analysis of common technical analysis indicators on daily price data for different products.  This project is the second for the K2 Data Science program.  

# Project Organization
------------

    |-- README.md           <- The top-level README which serves as a run-through the project
    │
    ├── MVP                 <- Minimum Viable Product
    │   |__ images          <- Generated figures to be used in reporting
    |   |__ README.md       <- Run-through of the MVP
    |   |__ Price_Indicator_Analysis_MVP.ipynb
    |
    |-- figures             <- Collection of figures used in creating the walkthrough
    │
    ├── notebooks           <- Jupyter notebooks used to create scripts, perform data cleaning,
    |                         manipulation, visualizations, etc
    │
    └── src                 <- Source code for use in this project
        ├── __init__.py     <- Makes src a Python module
        │
        ├── data            <- Scripts to download or generate data
        │   |── db_setup.py
        |   |__ util.py
        │
        ├── manipulation    <- Scripts to manipulate data into desired form for analysis
        │   └── manipulation.py
        │
        ├── analysis        <- Scripts to summarize and analyze cleaned data
        |   |
        |   ├__ analysis.py
        |  
        |
        |__ visualization   <- Scripts to visualize the exploratory analysis
            |
            |__ visualization.py


--------

# Project Workflow


![Project Workflow](figures/price_indicator_workflow.png)


# Project Walkthrough

## Goals

This analysis is being done to explore whether or not certain technical analysis indicators can consistently predict future price movements in various actively traded products.  Three common trading strategies include trend-following, break-out, and mean-reversion.  This project will explore indicators in each category and determine their individual predictive value over different timeframes.

## Data Collection

In order to get data from more traditional products and newer assets, I will be extracting data from both Quandl and Cryptocompare.  Each has its own API that is freely available, Quandl even has a package to be used specifically with Python.  For this project I am going to focus on historical daily price data, including the basic open, high, low, and close price as well as volume.  The end goal for collection is to have a database schema setup with three tables, one for Data, one for Symbols, and one for Daily_Prices data.  These tables will be linked by keys and include the relevant price and volume information mentioned above.

For continuous futures data, [Quandl](https://www.quandl.com/collections/futures)

For cryptocurrency data, [Cryptocompare](https://www.cryptocompare.com/)

Here is a list of all products broken down by sector, with accompanying symbols used in analysis:

* **Grains**
     * Corn - C
     * Wheat - W
     * Soybeans - S
* **Energy**
     * Crude Oil - CL
     * Heating Oil - HO
     * Natural Gas - NG
* **Forex**
     * Australian Dollar - AD
     * Canadien Dollar - CD
     * Euro - EC
     * Japanese Yen - JY
     * British Pound - BP
* **Treasuries**
     * 30-yr Bond - US
* **Metals**
     * Gold - GC
     * Silver - SI
* **Index**
     * E-mini S&P 500 - ES
* **Cryptocurrencies**
     * Bitcoin - BTC
     * Ethereum - ETH
     * Ripple- XRP
     * BitcoinCash - BCH
     * Litecoin - LTC
     * Cardano - ADA
     * Neo - NEO
     * Stellar - XLM
     * EOS - EOS
     * Monero - XMR

**SQL Database Schema**

![SQL Database Schema](figures/sql_db_schema.png)

## Improvements

1. For all futures data, continuous contracts were used for simplicity.  This means that when the a contract expires,
there is a rolling period where an average of the old and new front month contract prices are used rather than the
actual price.  This is an issue with futures contracts in general and any real trading strategy back-testing would
need to account for this.  However, this analysis was done simply to find good candidates for indicators that predict
future prices.  Therefore, I do not think it would significantly affect this study, but would need to be kept in
mind when moving to the next level of implementation.

2. This data is all historical data.  When moving on to creating strategies and potentially trading them, there
would need to be functionality for updating data and making decisions based on what is happening right now. Also
this type of analysis would need to continue to run in order to determine if the best indicators are continuing to
work, or if there are new indicators that are working better given current situations.

1. **Different Timeframes**
2. **Futures contract consideration, rather than continuous**
3. **Better check for outliers, not just 3 stds from overall mean**
4. **Better testing and cleaning of data before deploying capital**
