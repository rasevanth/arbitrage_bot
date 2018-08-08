#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 14:44:08 2018

@author: revanth
"""
#import pyotp
import math
import time
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException,TimeoutException,StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.alert import Alert
#from selenium.webdriver.common.action_chains import ActionChains
from koinex_pages.koinex_base import Koinex
class Koinex_market(Koinex):
    def __init__(self):
        Koinex.__init__(self)
       # self.start_page()
        #self.sign_in()
        self.market_precision={"zrx":3,"eth":3,"btc":4,"ltc":3,"xrp":0,"bch":4,
                               "omg":3,"req":3,"gnt":3,"bat":3,"ae":3,"trx":0,
                               "xlm":0,"neo":0,"gas":3,"xrb":3,"ncash":0,
                               "aion":2,"eos":2,"cmt":0,"ont":3,"zil":0,"iost":0,
                               "act":0,"zco":0,"poly":0,"elf":0,"snt":0,"rep":0,
                               "qkc":0,"xzc":2}
    def fill_buy_volume(self,volume):
        try:
            buy_vol=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "buyquantity")))
            buy_vol.clear()
            buy_vol.send_keys(str(volume))
        except TimeoutException as e:
            print(e)
            print('failed filling buy_quantity')
    
    def fill_sell_volume(self,volume):
        try:
            sell_vol=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "sellquantity")))
            sell_vol.clear()
            sell_vol.send_keys(str(volume))
        except TimeoutException as e:
            print(e)
            print('failed filling sell_quantity')
    def fill_buy_price(self,price):
        try:
            price_col = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "buyprice")))
            price_col.clear()
            price_col.send_keys(str(price))
        except TimeoutException as e:
            print(e)
            print('failed filling buy_price')
        
    def fill_sell_price(self,price):
        try:
            price_col = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "sellprice")))
            price_col.clear()
            price_col.send_keys(str(price))
        except TimeoutException as e:
            print(e)
            print('failed filling sell_price')
        
    def fill_buy_amount(self,amount):
        price_col=self.driver.find_element_by_id("buyTotalAmount")
        price_col.clear()
        price_col.send_keys(str(amount))
    def fill_sell_amount(self,amount):
        price_col=self.driver.find_element_by_id("selltotalamount")
        price_col.clear()
        price_col.send_keys(str(amount))
    def press_buy_button(self):
        try:
            buy_button= WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(
                        (By.XPATH, "//button[@ladda='order.askBidLadda']")))
            time.sleep(1)
            buy_button.click()
        except TimeoutException as e:
            print(e)
            print('failed confirming price')

    def press_sell_button(self):
        try:
            sell_button= WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(
                        (By.XPATH, "//button[@ladda='order.sellBidLadda']")))
            time.sleep(1)
            sell_button.click()
        except TimeoutException as e:
            print(e)
            print('failed confirming price')                

    def order_confirm_window(self):
        try:
            confirm_button= WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@ladda='ladda']")))
            time.sleep(1)
            confirm_button.click()
        except TimeoutException as e:
            print(e)
            print('failed confirming price')
    ################################### ###########       
    def place_buy_order(self,crypto,price,volume):
        
        self.navigate_to_market_page(crypto)
        #assert self.driver.current_url=self.__market_url+crypto_full_form+"/"
        time.sleep(1)
        vol_precision=self.market_precision[crypto]
        self.fill_buy_volume(float(math.floor(float(volume)*(10**vol_precision)))/(10**vol_precision))
        self.fill_buy_price(round(float(price),2))
        #self.fill_buy_amount(amount)
        self.press_buy_button()
        self.order_confirm_window()
        time.sleep(5)
        self.update_cryptobalances(crypto)
        #self.dismiss_alert()
    #################################################
    def place_sell_order(self,crypto,price,volume):

        self.navigate_to_market_page(crypto)
        #assert self.driver.current_url=self.__market_url+crypto_full_form+"/"
        time.sleep(1)
        #
        vol_precision=self.market_precision[crypto]
        self.fill_sell_price(round(float(price),2))
        self.fill_sell_volume(float(math.floor(float(volume)*(10**vol_precision)))/(10**vol_precision))
        #self.fill_sell_amount(amount)
        self.press_sell_button()
        self.order_confirm_window()
        time.sleep(5)
        self.update_cryptobalances(crypto)
        #self.dismiss_alert()
    #################################################################
    def are_open_orders(self):
        try:
            cancl=WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME,"cancel-link")))
            #cancl.click()
            return cancl.is_displayed()
        except TimeoutException as e:
            print(e)
            return False
            
    ###############################################################
    def cancel_order(self,crypto):
        try:
            cancl=WebDriverWait(self.driver,30).until(
            EC.presence_of_element_located((By.CLASS_NAME,"cancel-link")))
            cancl.click()
            self.order_confirm_window()
            time.sleep(5)
            self.get_inr_bal_available()
            self.get_crypto_bal_available(crypto)
        except TimeoutException as e:
            print(e,("cancel_orders is not available"))
    def cancel_all_orders(self,crypto):
        while(self.are_open_orders()):
            self.cancel_order(crypto)
    ######################################################################
    def get_inr_bal_available(self):
        try:
            inr_text=WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located(
                    (By.XPATH,"//div[@class='ask-bid']/div[1]/div[1]"))).text
            inr_bal=inr_text.replace("INR Balance: ","").replace(",","")
            self.wallets["inr"]=float(inr_bal)
        except TimeoutException as e:
            print(e,("inr_bal is not available"))

    def get_crypto_bal_available(self,crypto):
        try:
            crypto_texts=WebDriverWait(self.driver,5).until(
            EC.presence_of_all_elements_located(
                    (By.XPATH,"//div[@class='ask-bid']/div[1]/div[1]")))
            crypto_text=crypto_texts[1].text
            string_to_be_removed=crypto.upper()+" Balance: "
            crypto_bal=crypto_text.replace(string_to_be_removed,"").replace(",","")
            self.wallets[crypto.lower()]=float(crypto_bal)
        except TimeoutException as e:
            print(e,("crypto_bal is not available"))
    ########################################################################
    def update_cryptobalances(self,crypto,start=False):
        if start==True:
            logged_in=False
        else:
            logged_in=self.is_signed_in()
        if not logged_in:
            self.sign_in()
        present_url=self.driver.current_url
        crypto_market_url=self._market_url+self._fullforms[crypto]
        if not present_url==crypto_market_url:
            self.navigate_to_market_page(crypto)
        else:
            self.driver.refresh()
        self.get_inr_bal_available()
        self.get_crypto_bal_available(crypto)
    #############################################################
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
        sell_table=WebDriverWait(self.driver,30).until(EC.presence_of_element_located(
                (By.CLASS_NAME,"sell-orders")))
        orders=[]
        WebDriverWait(self.driver,10).until(EC.presence_of_element_located(
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
        buy_table=WebDriverWait(self.driver,30).until(EC.presence_of_element_located(
                (By.CLASS_NAME,"buy-orders")))
        orders=[]
        WebDriverWait(self.driver,30).until(EC.presence_of_element_located(
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
