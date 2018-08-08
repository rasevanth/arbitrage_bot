#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 18:43:03 2018

@author: chennam
"""

from bitbns_pages.bitbns_market import Bitbns_market
from bitbns_pages.bitbns_withdrawal import Bitbns_withdrawal
from api.arbitrage import buy_amount_decider,sell_amount_decider
class Bitbns(Bitbns_market,Bitbns_withdrawal):
    def __init__(self):
        Bitbns_market.__init__(self)
        Bitbns_withdrawal.__init__(self)
        self.addresses_dict={'zrx': {'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98', 'tag': None},
 'act': {'address': 'T6KjD5iCCjkLUodyUnHYWz7BRR3s4ShAvr29520473828975214916175903834587',
  'tag': None},
 'cpx': {'address': 'AMjMKKCGp4bjRdMZjZeZSZJYnAB4t7qvcV', 'tag': None},
 'rep': {'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98', 'tag': None},
 'btc': {'address': '3AsFJQQ5VYvPr92domLnNed8jcWgLefDh6', 'tag': None},
 'bch': {'address': 'qqv4jvqfh9zqulaev9z95qr22gt5gu9phcrtqlf96w', 'tag': None},
 'blz': {'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98', 'tag': None},
 'ada': {'address': 'DdzFFzCqrhswF36WchKhZkCh2Vq8xzUAEoXHjQEdJH8qS5moyKd4eLeGVW5UrnfTgameimeFwdwNYKVxpK6BnYKXFoHBNJAMrcrxYpon',
  'tag': None},
 'dash': {'address': 'XbYeMUMkczGfYk5XdZcMz8kuxL947PzinU', 'tag': None},
 'dbc': {'address': 'AMjMKKCGp4bjRdMZjZeZSZJYnAB4t7qvcV', 'tag': None},
 'dgb': {'address': 'D9PwZUMuvmv7viHSjxMrog4tLTQzZ43csn', 'tag': None},
 'dgd': {'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98', 'tag': None},
 'doge': {'address': 'DESBii6REutJt3PqgTqhnLLBmrbmB6m8V7', 'tag': None},
 'efx': {'address': 'AMjMKKCGp4bjRdMZjZeZSZJYnAB4t7qvcV', 'tag': None},
 'etn': {'address': 'tnjzydNicf8qV4eigKm6wigAi3gGrfdvE6bz5tw7ktQBEUzDy2uay7KMY7F3qcxH2eNecPP3T8qcb5JYxrNVv1c2EdiCSsoBn',
  'tag': '626974626e73236fe66e447a2d27cdf31749fd2a132c56a054e6e4af3cfb7ee9'},
 'eos': {'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98', 'tag': None},
 'eth': {'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98', 'tag': None},
 'gas': {'address': 'AMjMKKCGp4bjRdMZjZeZSZJYnAB4t7qvcV', 'tag': None},
 'icx': {'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98', 'tag': None},
 'ltc': {'address': 'LLV5VeVsf4WmmdaqXU1BGFEsQx5kTHpbEM', 'tag': None},
 'loom': {'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98',
  'tag': None},
 'lrc': {'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98', 'tag': None},
 'xmr': {'address': '42bnMbYoGZr1xHgnrP25KC6bRMDZNLJtpVaN4yM3mwzC26KPkzibGLPTwvWNQzPVzejeZEAL7GGGkLQYPDgWWo4MUbo1eyg',
  'tag': '626974626e73236fe66e447a2d27cdf31749fd2a132c56a054e6e4af3cfb7ee9'},
 'xem': {'address': 'ND5NJ3J5J3VG7WCSIYIL3RRGEWNUCTRV52AOABBZ',
  'tag': '35014'},
 'neo': {'address': 'AMjMKKCGp4bjRdMZjZeZSZJYnAB4t7qvcV', 'tag': None},
 'nexo': {'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98',
  'tag': None},
 'ncash': {'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98',
  'tag': None},
 'omg': {'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98', 'tag': None},
 'ont': {'address': 'AMjMKKCGp4bjRdMZjZeZSZJYnAB4t7qvcV', 'tag': None},
 'poly': {'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98',
  'tag': None},
 'powr': {'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98',
  'tag': None},
 'qlc': {'address': 'AMjMKKCGp4bjRdMZjZeZSZJYnAB4t7qvcV', 'tag': None},
 'rpx': {'address': 'AMjMKKCGp4bjRdMZjZeZSZJYnAB4t7qvcV', 'tag': None},
 'req': {'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98', 'tag': None},
 'xrp': {'address': 'r4VaPEKo4XoU27bCREgsTdbfKrKwNxJ1Cm', 'tag': '35014'},
 'sia': {'address': '033eaeb145566b2757761bfc19bb53b65c7ff99734fe554d6a20984457de6d615114448a1c2',
  'tag': None},
 'xlm': {'address': 'GAVQNY45FBHSN5MEPLAF56U7VDCBDG54TQFGJSS2CRPZTWD3CSHP4YPU',
  'tag': 'BITBNS35014'},
 'sub': {'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98', 'tag': None},
 'trx': {'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98', 'tag': None},
 'ven': {'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98', 'tag': None},
 'xvg': {'address': 'DNPpgHNgDPPbCyVoyERGcAHHK38enkpAmx', 'tag': None},
 'wan': {'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98', 'tag': None},
 'waves': {'address': '3P8cjwVvFDZL6zitqDqdkUJ1NV527YJ8Pc', 'tag': None},
 'wpr': {'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98', 'tag': None},
 'zil': {'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98', 'tag': None},
 "eosd":{'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98', 'tag': None},
 "gnt":{'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98', 'tag': None},
 "qtum":{'address': 'QLdanGyyz1RqpaiWFYqEnR4DB4shjcmntU', 'tag': None},
 "qkc":{'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98', 'tag': None},
 "storm":{'address': '0xa74f03f4574ddc5795ddca1f19b900e21c146e98', 'tag': None},
 "usdt":{"address":"1Ava1e9XfqZqGzmdp226CazLp3esTJCvi","tag":None},
 }
    def signin(self):
        self.sign_in()
        self.update_balances()
    def signout(self):
        self.sign_out()
    def deposit_credentials(self,crypto):
        return self.addresses_dict[crypto.lower()]
    def balance(self,crypto):
        return self.wallets[crypto.lower()]
    def market_page(self,crypto):
        self.move_to_market_page(crypto)
    def withdraw(self,crypto,volume,address,tag=123456):
        self.withdraw_crypto(crypto,volume,address,tag=123456)
    def decide_buy_details(self,crypto,amount,quote_price):
        self.move_to_market_page(crypto.lower())
        sell_ob=self.sell_orderbook()
        return buy_amount_decider(quote_price,amount,sell_ob)
    
    def final_sell_details(self,crypto,amount,quote_price):
        self.move_to_market_page(crypto.lower())
        buy_ob=self.buy_orderbook()
        return sell_amount_decider(quote_price,amount,buy_ob)
    def sell_market_price(self,crypto):
        self.move_to_market_page(crypto.lower())
        return self.buy_orderbook()[-1][1]
    def feasible_buy(self,f_amnt,amount):
        if f_amnt<0.95*amount:
            return False
        else:
            return True

    def sell_limit_quote(self,crypto,vol):
        self.move_to_market_page(crypto.lower())
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
            