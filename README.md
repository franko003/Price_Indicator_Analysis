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

## Data Cleaning

After examining the initial data I found there are a few different key areas of focus as far as cleaning the data.  

First of all, regarding the cryptocurrency data, due to the fact that each asset began trading at a different time, but we collected 2,000 data points for each, there are a lot of **zero** values.  

To clean this up and also take a look at data from times where there was enough liquidity to actually trade, I decided to pick a start date for each set of cryptocurrency to be the first day that trading volume reached **$1,000,000 USD**.

The next thing I noticed that needed to be addressed was a high amount of days with zero or less than 5,000 volume values.  The reason that I picked these specific products was due to their high liquidity so these values seemed off.  

This is likely due to poor data or something to do with the way they create the continuous contract, by taking weighting of the two current front months.  For this project **volume** is only going to be used in the case of a break-out strategy where we need to find days that are **200% of the rolling average volume**.  Thus, for our purposes taking these likely incorrect data and simply replacing them with the mean will suffice.

The last thing to do as far as cleaning the data before entering it into the database was to write a function that could check for outliers in price.  The fact is that these 3+ std moves do happen in commodity markets so my thought was to create a price chart and highlight the big outliers.

By looking at the entire price chart it should be easy to tell if the outlier was because of faulty data or simply because the market had made a big move so price was seriously deviating from the overall long-term mean.

Here is an example of the Crude Oil outliers

![Crude Oil Outliers Chart](figures/crude_oil_outliers.png)

And this is the Bitcoin outliers chart

![Bitcoin Outliers Chart](figures/bitcoin_outliers.png)

Each market has its outliers but they were due to the market itself making a strong move away from the mean value for the entire time series.  This is not uncommon for commodities and cryptocurrencies.  

In looking at the chart and having experience with these products I am comfortable saying that none of the points are far off due to inaccurate data.

## Data Manipulation

The next step in the analysis is to add columns to each product's dataframe to represent the specific indicators that we are interested in observing.  These can all be calculated from the current, **open, high, low, close, volume** data that we have.  

We also want to add columns that track future price changes.  I am choosing to look at a few different time frames, next day, 5 days out, 10 days out, and 20 days out.  Once we have columns for each indicator as a binary (0 if no signal, 1 if signal) and columns for the future returns from that point we can analyze which (if any) of the indicators shows promise for consistently predicting future returns.

Here is a list of the trade signal columns, price change columns, and descriptions

##### Break-out Strategies
* **Volume Break-out** - identifies days that are at least 200% of the 20day moving average volume.  Then gives a long signal if the closing price is greater than the previous day's high, or a short signal if the close is less than the previous day's low.

* **Range Break-out** - identifies days that trade higher than the high of the previous 20 days (long signal) or lower than the low of that range (short signal).

##### Trend-following Strategy
* **20day Moving Aveage** - identifies if price is above or below the 20day moving average and gives a long or short signal depending on the side.

* **50day Moving Aveage** - identifies if price is above or below the 50day moving average and gives a long or short signal depending on the side.

* **100day Moving Aveage** - identifies if price is above or below the 100day moving average and gives a long or short signal depending on the side.

##### Mean-reversion Strategy
* **Bollinger Band** - identifies when price trades higher than 2 standard deviations above or lower than 2 standard deviations below the 20day moving average.  If above it gives a short signal, if below a long.

##### Future Price Movement
* **Percent Change after 1 day** - gives the percentage change in price from close of this day to close of 1 day into the future.

* **Percent Change after 5 days** - gives the percentage change in price from close of this day to close of 5 days into the future.

* **Percent Change after 10 days** - gives the percentage change in price from close of this day to close of 10 days into the future.

* **Percent Change after 20 days** - gives the percentage change in price from close of this day to close of 20 days into the future.

With these columns now appended to our dataframes we can take a look at the number of signals produced for each product.  Here is the breakdown for **Crude Oil**

![Crude Oil Signal Count](figures/crude_trade_counts.png)

And this is the breakdown for **Bitcoin**

![Bitcoin Signal Count](figures/bitcoin_trade_counts.png)

## Initial Exploration

Now that we have all the data and indicators that we need, it is time to explore the real question at hand, do any of these indicators do a good job of predicting future prices.

In order to do this we will create a plot of the future returns of a product after each signal is triggered and see if the distribution is consistently around zero (no predictive value), above (positive predictive value), or below (negative predictive value).  Keep in mind that if we find an indicator that consistently predicts negative returns all we have to do is change the entry direction in order to create a winning strategy.

Here is an example with **Crude Oil** using the **50day Moving Average Long** strategy,looking at the **1day returns**.

![Crude Oil 50day MA Long 1day Returns](figures/crude_50ma_long_1day_returns.png)

And here looking at the **50day Moving Average Short** strategy, with **1day returns**.

![Crude Oil 50day MA Short 1day Returns](figures/crude_50ma_short_1day_returns.png)

So this looks like a good start.  With any trading strategy it is good to see positive results in each direction of trade.  It is a very simple way to show this is possibly a robust strategy, not one that finds winners in one direction but would just give back those gains on signals in the other direction.  

From here we will create a function to analyze this **signal-return** relationship for each signal, and for each timeframe of returns.  Then we will take a look at all the relationships to form hypotheses to test about what strategies are showing good predictive value.

In order to look at all the relationships I wrote a function to take in symbol, signal, and timeframe data and return the relevant statistics on percent returns.  Then I iterated over all products, for each signal, for each time period and added the data to a new dataframe.  It is this dataframe that I will use to show results of the initial exploration in the next section.

## Initial Research Findings

 * The distribution of **ave_return** for all combinations of strategies is not normal, but does have a positive mean and is skewed to the right, indicating that we may have found strategies with good predictive value.

![Distplot Ave Return](figures/distplot_ave_return.png)

 * **Cryptocurrencies** were clearly much more volatile than other products, taking up all of the top 100 strategies based on return, and most of the bottom 100.

![Countplot Top100](figures/countplot_top100.png)

![Countplot Bottom100](figures/countplot_bottom100.png)

 * The **Bollinger Band Signal** performed the worst by far, and it was the only **mean-reversion** strategy tested.

![Stripplot Signal](figures/stripplot_signal.png)

 * As far as **Break-out Strategies**, the **Range-Breakout** outperformed the **Volume-Breakout**, based on the fact that it showed positive results in both trade directions.

![Heatmap](figures/heatmap.png)

 * **Trend-following Strategies** using simple moving averages consistently performed well across the board, no matter what timeframe we were looking at.

## Final Steps

Now that the initial exploration is done, I want to refine the analysis down in order to make a recommendation for a robust trading strategy across all products.  To do so I will follow these final steps:

1. Filter out **Bollinger Band** strategy as it is clearly poor across all products.

2. Filter strategies down to those with a large number of data points. **(use 150)**

3. Search for the combinations (long and short combined) that create high average yearly returns based on product, signal, and timeframe.

4. Make a recommendation for an individual strategy to begin with on the road to creating a trading system.

Filtering the dataframe was accomplished with simple manipulation functions.  Then I created different functions to normalize the returns to an average yearly return (ave_yearly_return) rather than looking at ave_return.  Since these datasets all had a different number of points and covered a distinct periods of time.  

The last step was to combine the long/short trade directions for each strategy.  In the beginning analysis we were interested if we were seeing a difference between long and short returns of the same signal type.  For recommendation purposes, however, we want to suggest using a robust strategy that generates revenue for signals in either direction.

This last visualization shows the **Ave Yearly Return** based on each product/signal combination left after filtering.  

![Final Heatmap](figures/heatmap_final.png)

## Conclusions

1.  Trading strategies that go with the trend perform much better than mean-reversion strategies for the products, signals, and timeframes that were explored in this analysis.

2.  The longer the timeframe for holding the trade the better the ave return was.  While it is clear that given longer time, there should be bother greater winners and losers, it was interesting to me that the ave returns were all higher as timeframe increased.  This is a point to take into account when developing a trading system, longer holding periods can decrease transactional costs and time commitments to trading.  So if they increase returns as well there is strong evidence for moving away from intraday trading and shifting to a longer timeframe.

3.  For a recommendation of a signal/timeframe combination it is clear that the **Moving-Average 50day** strategy with a **20day** timeframe is the best.  In 17 of the 20 products it was the top combination.  Looking at the heatmap above we see that the **Moving-Average 20day** strategy is actually a little better across the board with averaging the returns of each timeframe.  Either way, in starting to create a trading system I would recommend using a moving average trend following signal to generate my first strategy for the portfolio.

## Improvements and Future Projects

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

1. A real trading strategy needs to take into account much more than closing prices and a fixed number of days to enter/exit positions on.  Introducing capital considerations, risk appetite, and profit targets would be three easy topics to add to this analysis.

2. This study was done looking at percentage gains and losses for each signal for the sake of simplicity and normalization across a number of different assets.  In reality, percentage changes are not as important as real money made and lost.  Further manipulation would have to be done to account for the tick size, tick amount, underlying currency, and other factors to determine exactly how much real money was being made and lost on each trade.  

3. There would need to be much better data cleaning and validation done before employing capital.  This was free historical data that was cleaned based on some simple observations from looking at price charts and volume information.  In reality more in depth work would need to be done and likely would need to bring in one or more other data sets to validate the results.
