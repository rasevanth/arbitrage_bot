#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 15:47:40 2018

@author: chennam
"""

from koinex_pages.koinex_market import Koinex_market
from koinex_pages.koinex_withdrawal import Koinex_withdrawal
from api.arbitrage import buy_amount_decider,sell_amount_decider
class Koinex(Koinex_market,Koinex_withdrawal):
    def __init__(self):
        Koinex_market.__init__(self)
        Koinex_withdrawal.__init__(self)
        
        self.addresses_dict={'xrp': {'address': 'rLdinLq5CJood9wdjY9ZCdgycK8KGevkUj', 'tag': '5955376'},
 'eth': {'address': '0x7a7f8c04017698256bb81f33efd3ff1e9c40a9de', 'tag': None},
 'btc': {'address': '39F7LvL5PYMMft7fk4VswpKTGTx7rtULrM', 'tag': None},
 'act': {'address': 'ACTNZ6vctmoSbgj7frsF2wRFdfq7GRdBu7vX99F14D21DEA4206494594443B68E74AD',
  'tag': None},
 'cmt': {'address': '0x7a7f8c04017698256bb81f33efd3ff1e9c40a9de', 'tag': None},
 'elf': {'address': '0x7a7f8c04017698256bb81f33efd3ff1e9c40a9de', 'tag': None},
 'poly': {'address': '0x7a7f8c04017698256bb81f33efd3ff1e9c40a9de',
  'tag': None},
 'zco': {'address': '0x7a7f8c04017698256bb81f33efd3ff1e9c40a9de', 'tag': None},
 'iost': {'address': '0x7a7f8c04017698256bb81f33efd3ff1e9c40a9de',
  'tag': None},
 'zil': {'address': '0x7a7f8c04017698256bb81f33efd3ff1e9c40a9de', 'tag': None},
 'ont': {'address': 'ARFJETwmUZFtEozAwCLP1byddaeZgR7o5c', 'tag': None},
 'xrb': {'address': 'xrb_1atdbxaku45b3r9pmhupsk747yt5od48u5g578riqazkoerk3omgzhudrxkf',
  'tag': None},
 'ncash': {'address': '0x7a7f8c04017698256bb81f33efd3ff1e9c40a9de',
  'tag': None},
 'aion': {'address': '0x7a7f8c04017698256bb81f33efd3ff1e9c40a9de',
  'tag': None},
 'gas': {'address': 'ARFJETwmUZFtEozAwCLP1byddaeZgR7o5c', 'tag': None},
 'neo': {'address': 'ARFJETwmUZFtEozAwCLP1byddaeZgR7o5c', 'tag': None},
 'xlm': {'address': 'GBTBVILDGCOIK26EPEHYCMKM7J5MTQ4FD5DO37GVTTBP45TVGRAROQHP',
  'tag': '1548940405'},
 'trx': {'address': '0x7a7f8c04017698256bb81f33efd3ff1e9c40a9de', 'tag': None},
 'gnt': {'address': '0x7a7f8c04017698256bb81f33efd3ff1e9c40a9de', 'tag': None},
 'ae': {'address': '0x7a7f8c04017698256bb81f33efd3ff1e9c40a9de', 'tag': None},
 'bat': {'address': '0x7a7f8c04017698256bb81f33efd3ff1e9c40a9de', 'tag': None},
 'zrx': {'address': '0x7a7f8c04017698256bb81f33efd3ff1e9c40a9de', 'tag': None},
 'omg': {'address': '0x7a7f8c04017698256bb81f33efd3ff1e9c40a9de', 'tag': None},
 'req': {'address': '0x7a7f8c04017698256bb81f33efd3ff1e9c40a9de', 'tag': None},
 'bch': {'address': '1P2y3VDYvBVSxiXK2XRgXrHMj9H9Ko1yRB', 'tag': None},
 'ltc': {'address': 'LXpELfQA6sa4EjL8xirgKC7DWpEejAh34q', 'tag': None},
 'snt': {'address': '0x7a7f8c04017698256bb81f33efd3ff1e9c40a9de', 'tag': None},
 "rep":{'address': '0x7a7f8c04017698256bb81f33efd3ff1e9c40a9de', 'tag': None},
 "qkc":{'address': '0x7a7f8c04017698256bb81f33efd3ff1e9c40a9de', 'tag': None},
 "xzc":{'address': 'aJCtrx9D8bm7xVFj8e9Rn42ntnwAhkVVfN', 'tag': None},
 "tusd":{'address': '0x7a7f8c04017698256bb81f33efd3ff1e9c40a9de', 'tag': None},
 }
    def signin(self):
        self.sign_in()
        self.update_balances()
    def signout(self):
        self.sign_out()
    def deposit_credentials(self,crypto):
        return self.addresses_dict[crypto.lower()]
    def crypto_fullforms(self,crypto):
        return self._fullforms[crypto.lower()]
    def market_page(self,crypto):
        self.navigate_to_market_page(crypto)

    def balance(self,crypto):
        return self.wallets[crypto.lower()]
    def withdraw(self,crypto,volume,address,tag=123456):
        self.withdraw_crypto(crypto,volume,address,tag=123456)
    def decide_buy_details(self,crypto,amount,quote_price):
        self.navigate_to_market_page(crypto.lower())
        sell_ob=self.sell_orderbook()
        return buy_amount_decider(quote_price,amount,sell_ob)
    
    def final_sell_details(self,crypto,amount,quote_price):
        self.navigate_to_market_page(crypto.lower())
        buy_ob=self.buy_orderbook()
        return sell_amount_decider(quote_price,amount,buy_ob)
    def sell_market_price(self,crypto):
        self.navigate_to_market_page(crypto.lower())
        return self.buy_orderbook()[-1][1]
    def feasible_buy(self,f_amnt,amount):
        if f_amnt<0.95*amount:
            return False
        else:
            return True
    def sell_limit_quote(self,crypto,vol):
        self.navigate_to_market_page(crypto.lower())
        buy_ob=self.buy_orderbook()
        cum_amnt=0
        cum_vol=0
        lob=len(buy_ob)
        for order_row in buy_ob:
            cum_vol+=order_row[0]
            cum_amnt+=order_row[0]*order_row[1]
            if cum_vol>vol:
                
                prev_vol=cum_vol-order_row[0]
                prev_amnt=cum_amnt-order_row[0]*order_row[1]
                amnt=prev_amnt+(vol-prev_vol)*order_row[1]
                avg_price=amnt/vol
                quote_price=order_row[1]
                return round(avg_price,2),quote_price
        avg_price=cum_amnt/cum_vol
        quote_price=buy_ob[lob-1][1]
        return round(avg_price,2),quote_price
    
    def feasible_sell(self,f_avg,avg_price):
        if f_avg<0.99*avg_price:
            return False
        else:
            return True
        
    