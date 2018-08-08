# arbitrage_bot
###dependencies:python 3,jupyter-notebook,pyotp,selenium
trianguar arbitrage from koinex and bitbns through binance
#api folder 
consists of api.py and arbitrage.py
api.py consists of apis of all the exchanges
arbitrage.py calculates the trianguar arbitrages among the exchanges
#koinex folder,koinex.py
abstracts the market and withdrawal functionalities of koinex exchange
#bitbns folder,bitbns.py
abstracts the market and withdrawal functionalities of bitbns exchange and confirming the withdrawal mail
#binance.py
abstracts the market and withdrawal functionalities of binance exchange

#orderbooks folder
scrapes the orderbooks of the indian cryptocurrency exchanges
#feeder.py
gets the best possible arbitrage
#main.ipynb
does the arbitrage
