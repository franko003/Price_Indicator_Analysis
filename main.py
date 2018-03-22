# Main function to pick what products you want to see and put them into the database

# Sqlite3 db info
sqlite_file = 'securities_master_db.sqlite'
table1_name = 'Data'
table2_name = 'Symbols'
table3_name = 'Daily_Prices'

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

# Individual lists of products from Cryptocompare and Quandl
cc_products = [p for p in products.keys() if (products[p][0] == 1)]
quandl_products = [p for p in products.keys() if (products[p][0] == 2)]
