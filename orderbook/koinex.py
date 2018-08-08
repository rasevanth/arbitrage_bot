#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 19:00:54 2018

@author: chennam
"""
#import time
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException,TimeoutException,StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

class Koinex:
    coins_dict={
            "btc":"bitcoin",
            "eth":"ether",
            "bch":"bitcoin_cash",
            "ltc":"litecoin",
            "xrp":"ripple",
            "xlm":"stellar",
            "xrb":"nano",
            "neo":"neo",
            "gas":"gas",
            "elf":"aelf",
            "ae":"aeternity",
            "omg":"omisego",
            "req":"request",
            "zrx":"zerox",
            "gnt":"golem",
            "bat":"basic_attention_token",
            "trx":"tron",
            "ncash":"nucleus_vision",
            "aion":"aion",
            "eos":"eos",
            "ont":"ontology",
            "zil":"zilliqa",
            "iost":"ios_token",
            "zco":"zebi",
            "poly":"polymath",
            "cmt":"cyber_miles",
            "act":"achain",
            "snt":"status",
            "rep":"augur",
            "qkc":"quarkchain",
            "xzc":"zcoin",
            "tusd":"true_usd",
            }
    def __init__(self):
        self.__driver=self.driver()
        self.__driver.get("https://koinex.in/")
        try:
            btn=self.__driver.find_element_by_class_name("solidBtn")
            btn.click()
        except:
            pass

    def driver(self):
        options = Options()
        options.set_headless(headless=True)
        return webdriver.Firefox(firefox_options=options)
    def get_webpage(self,crypto):
        self.__driver.get("https://koinex.in/exchange/inr/{}".format(crypto))

    def find_column_text(self,row):
        columns=row.find_elements_by_tag_name("td")
        try:
            return (float(columns[0].text.replace(",","")),float(columns[-1].text.replace(",","")))
        except ValueError:
            pass
    
    def find_staledcolumn_text(self,row,i,table,reverse):
        try:
            new_row=table.find_elements_by_tag_name("tr")[::reverse][i]
            return self.find_column_text(new_row)
        except:
            self.find_staledcolumn_text(row,i,table,reverse)
    def sell_orderbook(self):
        sell_table=WebDriverWait(self.__driver,30).until(EC.presence_of_element_located(
                (By.CLASS_NAME,"sell-orders")))
        orders=[]
        WebDriverWait(self.__driver,10).until(EC.presence_of_element_located(
                (By.XPATH,"//tbody[@class='sell-orders']/tr[3]")))
        sell_orders=sell_table.find_elements_by_tag_name("tr")
        for i,row in enumerate(sell_orders[::-1]):
            if i%2==1:
                try:
                    order=self.find_column_text(row)
                    if order is not None:
                        orders.append(order)
                except StaleElementReferenceException:
                    #print("staled")
                    order=self.find_staledcolumn_text(row,i,sell_table,1)
                    if order is not None:
                        orders.append(order)
        return orders
    def buy_orderbook(self):
        buy_table=WebDriverWait(self.__driver,30).until(EC.presence_of_element_located(
                (By.CLASS_NAME,"buy-orders")))
        orders=[]
        WebDriverWait(self.__driver,30).until(EC.presence_of_element_located(
                (By.XPATH,"//tbody[@class='buy-orders']/tr[3]")))
        buy_orders=buy_table.find_elements_by_tag_name("tr")
        for i,row in enumerate(buy_orders[::1]):
            if i%2==0:
                try:
                    order=self.find_column_text(row)
                    if order is not None:
                        orders.append(order)
                except StaleElementReferenceException:
                    #print("staled")
                    order=self.find_staledcolumn_text(row,i,buy_table,1)
                    if order is not None:
                        orders.append(order)
        return orders
    def orderbook(self,crypto):
        #print(crypto)
        self.get_webpage(self.coins_dict[crypto.lower()])
        buy_orders=self.buy_orderbook()
        sell_orders=self.sell_orderbook()
        
        rdict={"buy":buy_orders,
               "sell":sell_orders
               }
        return rdict   
    def close_driver(self):
        self.__driver.close()
#print(Koinex().orderbook("cmt"))