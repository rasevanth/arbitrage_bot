#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 21:53:31 2018

@author: chennam
"""

import time
import json
import requests
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,StaleElementReferenceException

def api(url):
    resp=requests.get(url)
    json_format=json.loads(resp.text)
    return json_format
def exclusion_list(volume_dict):
    exclusion_list=[]
    for each in volume_dict:
        if each[1][0]<2000000 or each[1][1] <1:
            exclusion_list.append(each[0])
    return exclusion_list    

class Koinex:
    _COINS_DICT={
        "bitcoin":"btc",
        "ethereum":"eth",
        "ripple":"xrp",
        "bitcoin cash":"bcc",
        "0x protocol":"zrx",
        "aelf":"elf",
        "aeternity":"ae",
        "aion":"aion",
        "basic attention token":"bat",
        "eos":"eos",
        "gas":"gas",
        "golem":"gnt",
        "ios token":"iost",
        "litecoin":"ltc",
        "nano":"xrb",
        "neo":"neo",
        "nucleus vision":"ncash",
        "omisego":"omg",
        "ontology":"ont",
        "polymath":"poly",
        "request network":"req",
        "stellar":"xlm",
        "tron":"trx",
        "zebi":"zco",
        "zilliqa":"zil",
        "tusd":"true_usd",
    }
    def __init__(self):
        self.__url="https://koinex.in/api/ticker"
        self.__api=api(self.__url)
    def crypto_rates(self,crypto,base="inr"):
        rates=self.__api
        crypto_rates=rates["stats"][base][crypto.upper()]
        market_buy=float(crypto_rates["lowest_ask"])
        market_sell=float(crypto_rates["highest_bid"])
        return market_buy,market_sell
    def cryptos_list_ratio(self,base="inr"):
        all_rates=dict()
        base_buy,base_sell=float(self.__api["stats"]["inr"]["BTC"]["lowest_ask"]),\
                                    float(self.__api["stats"]["inr"]["BTC"]["highest_bid"])
        coin_list=self.__api["prices"][base].keys()
        for each in coin_list:
            all_rates[each.lower()]=(
                self.crypto_rates(each,base)[0]/base_buy,self.crypto_rates(each,base)[1]/base_sell)
        return all_rates
    
    def cryptos_list_price(self,base="inr"):
        all_rates=dict()
        coin_list=self.__api["prices"][base].keys()
        for each in coin_list:
            all_rates[each.lower()]=(self.crypto_rates(each,base)[0],self.crypto_rates(each,base)[1])
        return all_rates
    def get_volume(self):
        vol_dict=dict()
        try:
            driver=webdriver.Firefox()
            driver.get("https://koinex.in/")
            rows=driver.find_elements_by_xpath("//tbody/tr")
        
            for row in rows[1:]:
                try:
                    columns=row.find_elements_by_xpath("td")
                    vol_dict[columns[0].text]=\
                    (float(columns[5].text.replace(",",""))*float(columns[1].text.replace(",","")),\
                     float(columns[1].text.replace(",","")))
                except StaleElementReferenceException:
                    columns=row.find_elements_by_xpath("td")
                    vol_dict[columns[0].text]=\
                (float(columns[5].text.replace(",",""))*float(columns[1].text.replace(",","")),\
                 float(columns[1].text.replace(",","")))
            driver.close()
        except StaleElementReferenceException:
            driver.close()
            self.get_volume()
        
        vol_dict=sorted(vol_dict.items(),key=lambda t:t[1][0],reverse=True)
        return vol_dict
    def get_exclusion_list_on_vol(self):
        exclusion_list_names=exclusion_list(self.get_volume())
        short_forms=lambda x:self._COINS_DICT[x.lower()]
        return list(map(short_forms,exclusion_list_names))
class Bitbns:
    _COINS_DICT={
        "bitcoin":"btc",
        "ethereum":"eth",
        "bitcoin cash":"bch",
        "ripple":"xrp",
        "litecoin":"ltc",
        "stellar":"xlm",
        "0x":"zrx",
        "apex":"cpx",
        "augur":"rep",
        "effect.ai":"efx",
        "loom network":"loom",
        "bluzelle":"blz",
        "substratum":"sub",
        "loopring":"lrc",
        "nexo":"nexo",
        "verge":"xvg",
        "electroneum":"etn",
        "neo":"neo",
        "achain":"act",
        "cardano":"ada",
        "dash":"dash",
        "deepbrain chain":"dbc",
        "digibyte":"dgb",
        "digixdao":"dgd",
        "doge":"doge",
        "eos":"eos",
        "gas":"gas",
        "icon":"icx",
        "monero":"xmr",
        "nem":"xem",
        "nucleus vision":"ncash",
        "omisego":"omg",
        "ontology":"ont",
        "polymath":"poly",
        "request":"req",
        "power ledger":"powr",
        "qlink":"qlc",
        "red pulse":"rpx",
        "sia":"sia",
        "tron":"trx",
        "vechain":"ven",
        "wepower":"wpr",
        "wanchain":"wan",
        "waves":"waves",
        "zilliqa":"zil",
        
    }
    def __init__(self):
        self.__url="https://bitbns.com/order/getTickerAll"
        self.__api=api(self.__url)

    def cryptos_list_ratio(self):
        all_rates=dict()
        base_buy=self.__api[0]["BTC"]["sellPrice"]
        base_sell=self.__api[0]["BTC"]["buyPrice"]
        for each in self.__api:
            for coin,price_dict in each.items():
                market_buy=float(price_dict["sellPrice"])/base_buy
                market_sell=float(price_dict["buyPrice"])/base_sell
                all_rates[coin.lower()]=(market_buy,market_sell)
        return all_rates
    def cryptos_list_price(self):
        all_rates=dict()
        for each in self.__api:
            for coin,price_dict in each.items():
                market_buy=float(price_dict["sellPrice"])
                market_sell=float(price_dict["buyPrice"])
                all_rates[coin.lower()]=(market_buy,market_sell)
        return all_rates
    
    def crypto_rates(self,crypto):
        l=self.cryptos_list()
        return l[crypto.lower()]
        
    def get_volume(self):
        driver=webdriver.Firefox()
        driver.get("https://bitbns.com/trade/#/")
        time.sleep(2)
        btn=driver.find_element_by_xpath(
        "//button[@class='js-modal__close c-btn--size2 c-btn c-btn--outline']")
        btn.click()
        rows=driver.find_elements_by_xpath("//tbody/tr")
        vol_dict=dict()
        for row in rows:
            columns=row.find_elements_by_xpath("td")
            vol_dict[columns[1].text]=\
            (float(columns[2].text.strip("₹").replace(",",""))*float(columns[6].text.replace(",","")),\
             float(columns[2].text.strip("₹").replace(",","")))
        driver.close()
        vol_dict=sorted(vol_dict.items(),key=lambda t:t[1][0],reverse=True)
        return vol_dict
    def get_exclusion_list_on_vol(self):
        exclusion_list_names=exclusion_list(self.get_volume())
        short_forms=lambda x:self._COINS_DICT[x.lower()]
        return list(map(short_forms,exclusion_list_names))
    
#from forex_python.bitcoin import BtcConverter
   # add "force_decimal=True" parmeter to get Decimal rates

class Binance:
    def __init__(self):
        self.__url="https://api.binance.com/api/v3/ticker/bookTicker"
        self.__infoURL="https://www.binance.com/assetWithdraw/getAllAsset.html"
        self.__api=api(self.__url)
    def cryptos_list(self,base="btc"):
        all_rates=dict()
        #b = BtcConverter()
        #btc=b.get_latest_price('INR')
        for each in self.__api:
            if each["symbol"][-len(base):]==base.upper():
                market_buy=float(each["askPrice"])#round(float(each["askPrice"])*btc,2)
                market_sell=float(each["bidPrice"])#round(float(each["bidPrice"])*btc,2)
                all_rates[each["symbol"][:-len(base)].lower()]=(market_buy,market_sell)
        return all_rates
    
    def crypto_rates(self,crypto,base="btc"):
        all_dict=self.cryptos_list(base)
        return all_dict[crypto.lower()]
    def get_deposit_disabled_list(self):
        disabled=[]
        a=api(self.__infoURL)
        for each in a:
            if not each["enableCharge"]:
                disabled.append(each["assetCode"].lower())
        return disabled
    def get_withdraw_disabled_list(self):
        disabled=[]
        a=api(self.__infoURL)
        for each in a:
            if not each["enableWithdraw"]:
                disabled.append(each["assetCode"].lower())
        return disabled