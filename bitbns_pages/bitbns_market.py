#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 15:06:55 2018

@author: revanth
"""
import time
import math
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException,TimeoutException,StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.action_chains import ActionChains
from bitbns_pages.bitbns_base import Bitbns
class Bitbns_market(Bitbns):
    def __init__(self):
        Bitbns.__init__(self)
    def click_on_allcoins(self):
        all_coins=WebDriverWait(self.driver,30).until(
        EC.presence_of_element_located((
        By.XPATH,"//div[@class='u-disp--ib u-cursor--pointer bb-currencies__btn u-overflow--initial u-padding-vertical-2x  u-padding-horizontal-1x u-margin-right-1x bb-currencies__dropDown  c-toolTips__container c-toolTips__container--bottomRight']")))
        all_coins.click()
        
    def click_crypto_bar(self,crypto_full):
        title="Trade {} Tokens".format(crypto_full)
        crypto_dropdown=self.driver.find_element_by_xpath("//a[@title='{}']".format(title))
        crypto_dropdown.click()
    def navigate_to_market_page(self,crypto_full):
        time.sleep(1)
        self.click_on_allcoins()
        time.sleep(1)
        self.click_crypto_bar(crypto_full.capitalize())
        time.sleep(1)
    ####################################################################
    def move_to_market_page(self,crypto):
        url=self._market_base_url+crypto
        self.driver.get(url)
    #############################################################################
    def toggle_buy_section(self):
        if not self.is_buy_btn_displayed():
            try:
                buy_toggle=WebDriverWait(self.driver,30).until(EC.presence_of_element_located(
                    (By.XPATH,"//div[@data-ctab='buy']")))
                buy_toggle.click()
            except TimeoutException as e:
                print(e)
                print("failed_toggling_buysection")
    def toggle_sell_section(self):
        if not self.is_sell_btn_displayed():
            try:
                sell_toggle=WebDriverWait(self.driver,30).until(EC.presence_of_element_located(
                    (By.XPATH,"//div[@data-ctab='sell']")))
                sell_toggle.click()
            except TimeoutException as e:
                print(e)
                print("failed_toggling_sellsection")
    def fill_buy_volume(self,volume):
        buy_vol=self.driver.find_element_by_id("buyVolume")
        buy_vol.clear()
        buy_vol.send_keys(str(volume))
    def fill_sell_volume(self,volume):
        sell_vol=self.driver.find_element_by_id("sellVolume")
        sell_vol.clear()
        sell_vol.send_keys(str(volume))
    def fill_buy_price(self,price):
        buy_price=self.driver.find_element_by_id("buyPrice")
        buy_price.clear()
        buy_price.send_keys(str(price))
    def fill_sell_price(self,price):
        sell_price=self.driver.find_element_by_id("sellPrice")
        sell_price.clear()
        sell_price.send_keys(str(price))
    def fill_sell_amount(self,amount):
        sell_amount=self.driver.find_element_by_id("sellAmtFinal")
        sell_amount.clear()
        sell_amount.send_keys(str(amount))
    def fill_buy_amount(self,amount):
        buy_amount=self.driver.find_element_by_id("buyAmtFinal")
        buy_amount.clear()
        buy_amount.send_keys(str(amount))
    def press_buy_btn(self):
        buy_btn=self.driver.find_element_by_id("buy__coin")
        buy_btn.click()
    def is_sell_btn_displayed(self):
        try:
            sell_btn=WebDriverWait(self.driver,30).until(EC.presence_of_element_located(
                    (By.ID,"sel__coin")))
            return sell_btn.is_displayed()
        except TimeoutException as e:
            return False
    def is_buy_btn_displayed(self):
        try:
            buy_btn=WebDriverWait(self.driver,30).until(EC.presence_of_element_located(
                    (By.ID,"buy__coin")))
            return buy_btn.is_displayed()
        except TimeoutException as e:
            return False 
    def press_sell_btn(self):
        sell_btn=self.driver.find_element_by_id("sel__coin")
        sell_btn.click()
    #########################################################3
    def place_buy_order(self,crypto,price,volume):
        self.move_to_market_page(crypto)
        self.get_crypto_balance(crypto)
        self.get_inr_balance()
        vol_precision=self._precision_digits[crypto]["trade"]
        
        self.fill_buy_volume(float(math.floor(float(volume)*(10**vol_precision)))/(10**vol_precision))
        self.fill_buy_price(price)
        self.press_buy_btn()
        #self.click_order_okay()
        self.confirm_order()
        time.sleep(5)
        self.update_cryptobalances(crypto)
    ################################################################################
    def place_sell_order(self,crypto,price,volume):
        self.move_to_market_page(crypto)
        self.get_inr_balance()
        self.get_crypto_balance(crypto)
        vol_precision=self._precision_digits[crypto]["trade"]
        self.fill_sell_volume(float(math.floor(float(volume)*(10**vol_precision)))/(10**vol_precision))
        self.fill_sell_price(price)
        self.press_sell_btn()
        #self.click_order_okay()
        self.confirm_order()
        time.sleep(5)
        self.update_cryptobalances(crypto)
    #################################################################################
    def cancel_press(self):
        try:
            btn=WebDriverWait(self.driver,30).until(EC.element_to_be_clickable(
                    (By.XPATH,"//td[@class='c-table__cell bb-orderList__cancel u-highlight-target']")))
            btn.location_once_scrolled_into_view
            btn.click()
        except TimeoutException as e:
            print(e,"failed cancelling orders")
    
    def confirm_order(self):
        try:
            btn=WebDriverWait(self.driver,30).until(EC.presence_of_element_located(
                    (By.XPATH,"//button[@class='js-focusOnOpen js-modal__close c-btn--size2 c-btn c-btn--violet']")))
            btn.location_once_scrolled_into_view
            btn.click()
        except TimeoutException as e:
            print(e,"failed confirmed orders")
    #######################################################
    def are_open_orders(self):
        
        try:
            btn=WebDriverWait(self.driver,5).until(EC.element_to_be_clickable(
                    (By.XPATH,"//td[@class='c-table__cell bb-orderList__cancel u-highlight-target']")))
            return btn.is_displayed()
        except TimeoutException as e:
            print("no open orders")
            return False
    ####################################################################################
    def cancel_order(self,crypto):
        self.cancel_press()
        self.confirm_order()
        time.sleep(5)
        self.get_inr_balance()
        self.get_crypto_balance(crypto)
    def cancel_all_orders(self,crypto):
        while(self.are_open_orders()):
            self.cancel_order(crypto)
    ##############################################################################3####
    def get_inr_balance(self):
        self.toggle_buy_section()
        bal=self.driver.find_element_by_xpath("//form[@name='bns__buy']/div[7]")
        inr_bal=bal.text.split("₹")[1].strip(" ").replace(",","")
        self.wallets["inr"]=float(inr_bal)

    def get_crypto_balance(self,crypto):
        self.toggle_sell_section()
        bal=self.driver.find_element_by_xpath("//form[@name='bns__sell']/div[7]")
        crypto_bal=bal.text.split("=")[1].rstrip(crypto.upper()).strip(" ").replace(",","")
        
        self.wallets[crypto.lower()]=float(crypto_bal)

    
    def click_order_okay(self):
        btn=WebDriverWait(self.driver,30).until(EC.element_to_be_clickable(
                    (By.XPATH,"//button[@class='js-focusOnOpen js-modal__close c-btn--size2 c-btn c-btn--outline']")))
        btn.click()
#####################################################################################    
    def update_cryptobalances(self,crypto,start=False):
        if start==True:
            logged_in=False
        else:
            logged_in=self.is_signed_in()
        if not logged_in:
            self.sign_in()
        if not self.driver.current_url==self._market_base_url+crypto:
            self.move_to_market_page(crypto)
        else:
            self.driver.refresh()
        self.close_popup()
        self.get_inr_balance()
        self.get_crypto_balance(crypto)
################################################################################
    def find_column_text(self,row):
        columns=row.find_elements_by_tag_name("td")
        try:
            return (float(columns[0].text.strip("₹").replace(",","")),
                float(columns[-1].text.strip("₹").replace(",","")))
        except ValueError:
            pass
    def find_staledcolumn_text(self,row,i,table):
        try:
            WebDriverWait(self.driver,5).until(EC.staleness_of(row.find_elements_by_tag_name("td")[-1]))
        except TimeoutException as e:
            pass
        finally:
            try:
                new_row=table.find_elements_by_tag_name("tr")[i]
                return self.find_column_text(new_row)
            except:
                self.find_staledcolumn_text(row,i,table)
    def buy_orderbook(self):
        buy_table=WebDriverWait(self.driver,30).until(EC.visibility_of_element_located((By.ID,"buyOrderBid")))
        orders=[]
        WebDriverWait(self.driver,30).until(EC.presence_of_element_located(
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
        sell_table=WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.ID,"sellOrderBid")))
        orders=[]
        WebDriverWait(self.driver,30).until(EC.presence_of_element_located(
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