# Price_Indicator_Analysis (MVP)

Analysis of common technical analysis indicators on daily price data for different products.

## Goals

This analysis is being done to explore whether or not certain technical analysis indicators can consistently predict future price movements in various actively traded products.  Three common trading strategies include trend-following, break-out, and mean-reversion.  This project will explore indicators in each category and determine their individual predictive value over different timeframes.

## Data Collection

In order to get data from more traditional products and newer assets, I will be extracting data from both Quandl and Cryptocompare.  Each has its own API that is freely available, Quandl even has a package to be used specifically with Python.  For this project I am going to focus on historical daily price data, including the basis open, high, low, and close price as well as volume.  The end goal for collection is to have a database schema setup with three tables, one for Data source, one for Product names, and one for Price Data.  These tables will be linked by keys and include the relevant price and volume information mentioned above.

From Quandl, I want to look at data from highly traded products across different asset classes.  My breakdown follows...

  * **Grains**
   * Corn
   * Wheat
   * Soybeans
  * **Energy**
   * Crude Oil
   * Heating Oil
   * Natural Gas
  * **Forex**
   * Australian Dollar
   * Canadien Dollar
   * Euro
   * Japanese Yen
   * British Pound
  * **Treasuries**
   * 30-yr Bond
  * **Metals**
   * Gold
   * Silver
  * **Index**
   * E-mini S&P 500

Then in order to incorporate a newer asset class like cryptocurrencies I will use the Cryptocompare API.  I will look at the following 10 for this project, based on them being the current top 10 as far as market cap.

  * **Cryptocurrencies**
   * Bitcoin
   * Ethereum
   * Ripple
   * BitcoinCash
   * Litecoin
   * Cardano
   * Neo
   * Stellar
   * EOS
   * Monero

## Data Cleaning

After examining the initial data I found there are a few different key areas of focus as far as cleaning the data.  Some specific to 






## Further research

1. **Different Timeframes**
2. **Futures contract consideration, rather than continuous**
