#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 22:09:18 2018

@author: chennam
"""
import time
from api.api import Koinex,Binance,Bitbns
from api.arbitrage import main
from orderbook import koinex,bitbns

orderbooks=[koinex.Koinex(),bitbns.Bitbns()]
def close_orderbooks(orderbooks=orderbooks):
    for each in orderbooks:
        each.close_driver()

balance_list={
        "koinex":000,
        "bitbns":27000,
        }
bitbns_exclusion_dict={
    "deposit":["eos","eosDac","icx","rep","ncash","usdt","req","etc","lsk","npxs","trx","let","sub","loom","storm","wpr","blz","gnt","cloak","dent","grs","kmd","lrc"],
    "withdraw":["eos","eosDac","icx","usdt","etc","lsk","npxs","trx","cloak","dent","grs","kmd","let","zrx"]#,"req","powr","nexo","lrc","loom","dgd","blz","poly","omg","zrx","gnt","eth","zil","poly","rep","ncash","qkc","wpr","wan","storm","ven","sub"]
}
binance_exclusion_dict={
    "deposit":Binance().get_deposit_disabled_list(),
    "withdraw":Binance().get_withdraw_disabled_list()
}
koinex_exclusion_dict={
    "deposit":["tusd","eos","trx","xzc","rep","ncash","cmt"],
    "withdraw":["tusd","eos","trx","xzc"]#"omg","req","omg","zrx","bat","gnt","eth","zil","zco","poly","elf","rep","ae","aion","iost","snt","ncash","qkc","cmt"]
}

indian_deposit_exclusion_names=[]
international_exclusion_names=[]
indian_withdrawal_exclusion_names=[]
def feed(balance_list=balance_list):
    indian_sites_list=[Koinex(),Bitbns()]
    international_sites_list=[Binance()]
    indian_exclusion_list=[koinex_exclusion_dict,bitbns_exclusion_dict]
    international_exclusion_list=[binance_exclusion_dict]
    return main(indian_sites_list,international_sites_list,
        indian_exclusion_list,international_exclusion_list,balance_list,orderbooks,
        indian_deposit_exclusion_names,international_exclusion_names,
         indian_withdrawal_exclusion_names)
