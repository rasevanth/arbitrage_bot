#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 18:58:32 2018

@author: chennam
"""

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException,TimeoutException,StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

class Bitbns:
    def __init__(self):
        self.__driver=self.driver()
        self.__driver.get("https://bitbns.com/trade/#")
        try:
            btn=self.__driver.find_element_by_xpath("//button[@class='js-modal__close c-btn--size2 c-btn c-btn--outline']")
            btn.click()
        except:
            pass

    def driver(self):
        options = Options()
        options.set_headless(headless=True)
        return webdriver.Firefox(firefox_options=options)
    def get_webpage(self,crypto):
        self.__driver.get("https://bitbns.com/trade/#/{}".format(crypto))
        
    def find_column_text(self,row):
        columns=row.find_elements_by_tag_name("td")
        try:
            return (float(columns[0].text.strip("₹").replace(",","")),
                float(columns[-1].text.strip("₹").replace(",","")))
        except ValueError:
            pass
    def find_staledcolumn_text(self,row,i,table):
        try:
            WebDriverWait(self.__driver,5).until(EC.staleness_of(row.find_elements_by_tag_name("td")[-1]))
        except TimeoutException as e:
            pass
        finally:
            try:
                new_row=table.find_elements_by_tag_name("tr")[i]
                return self.find_column_text(new_row)
            except:
                self.find_staledcolumn_text(row,i,table)
    def buy_orderbook(self):
        buy_table=WebDriverWait(self.__driver,30).until(EC.visibility_of_element_located((By.ID,"buyOrderBid")))
        orders=[]
        WebDriverWait(self.__driver,30).until(EC.presence_of_element_located(
                (By.XPATH,"//tbody[@id='buyOrderBid']/tr[2]")))
        buy_orders=buy_table.find_elements_by_tag_name("tr")
        for i,row in enumerate(buy_orders):
            try:
                order=self.find_column_text(row)
                if order is not None:
                    orders.append(order)
            except StaleElementReferenceException:
                #print("staled")
                order=self.find_staledcolumn_text(row,i,buy_table)
                if order is not None:
                    orders.append(order)
        return orders
    def sell_orderbook(self):
        sell_table=WebDriverWait(self.__driver,10).until(EC.visibility_of_element_located((By.ID,"sellOrderBid")))
        orders=[]
        WebDriverWait(self.__driver,30).until(EC.presence_of_element_located(
                (By.XPATH,"//tbody[@id='sellOrderBid']/tr[2]")))
        sell_orders=sell_table.find_elements_by_tag_name("tr")

        for i,row in enumerate(sell_orders):
            try:
                order=(self.find_column_text(row)[1],self.find_column_text(row)[0])
                if order is not None:
                    orders.append(order)
            except StaleElementReferenceException:
                #print("staled")
                order=(
                    self.find_staledcolumn_text(row,i,sell_table)[1],
                     self.find_staledcolumn_text(row,i,sell_table)[0])
                if order is not None:
                    orders.append(order)
        return orders
    
    def orderbook(self,crypto):
        self.get_webpage(crypto)
        buy_orders=self.buy_orderbook()
        sell_orders=self.sell_orderbook()
        
        rdict={"buy":buy_orders,
               "sell":sell_orders
               }
        return rdict
    def close_driver(self):
        self.__driver.close()
#print(Koinex().orderbook("eth"))