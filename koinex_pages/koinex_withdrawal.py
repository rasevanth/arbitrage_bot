#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 14:48:21 2018

@author: revanth
"""
import time
import math
from koinex_pages.koinex_base import Koinex
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
class Koinex_withdrawal(Koinex):
    def __init__(self):
        Koinex.__init__(self)
        self._koin_url="https://koinex.in/KOINWallet"
        self._base_withdrawal_url="https://koinex.in/wallet_withdrawals/"
        self._base_deposits_url="https://koinex.in/wallet_deposits/"
    def search_koin_koinwallet(self,crypto):
        search_box=self.driver.find_element_by_xpath(
                "//input[@placeholder='Search Coin']")
        search_box.clear()
        search_box.send_keys(crypto)
    def click_withdraw_walletpage(self):
        WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                        (By.XPATH, "//a[@class='link newtooltip']")))
        withdraw=self.driver.find_elements_by_xpath("//a[@class='link newtooltip']")[1]
        withdraw.click()
    def koin_wallet_page(self):
        self.driver.get(self._koin_url)
    def crypto_withdrawal_page(self,crypto):
        withdrawal_url=self._base_withdrawal_url+self._fullforms[crypto]
        self.driver.get(withdrawal_url)
    def crypto_deposits_page(self,crypto):
        deposit_url=self._base_deposits_url+self._fullforms[crypto]
        self.driver.get(deposit_url)
    ###################################################################
    def fill_withdrawal_volume(self,volume):
        try:
            vol=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                        (By.XPATH, "//input[@placeholder='Volume']")))
            vol.clear()
            vol.send_keys(str(volume))
        except TimeoutException as e:
            print(e)
   
    def check_withdrawal_working(self,crypto):
        self.crypto_withdrawal_page(crypto)
        time.sleep(2)
        try:
            vol=WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                        (By.XPATH, "//input[@placeholder='Volume']")))
            return True
        except TimeoutException as e:
            return False
    def check_deposit_working(self,crypto):
        self.crypto_deposits_page(crypto)
        time.sleep(2)
        try:
            addr=WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                        (By.XPATH, "//input[@id='wallet-address']")))
            return True
        except TimeoutException as e:
            return False
        
    def fill_withdrawal_dest_addr(self,address):
        addr_box=self.driver.find_element_by_xpath(
                "//input[@placeholder='Wallet Address']")
        addr_box.clear()
        addr_box.send_keys(address)
    def fill_withdrawal_tag(self,tag):
        tag_box=self.driver.find_element_by_xpath(
                "//input[@placeholder='Destination Tag']")
        tag_box.clear()
        tag_box.send_keys(tag)
    def fill_withdrawal_memo(self,memo):
        memo_box=self.driver.find_element_by_xpath(
                "//input[@placeholder='Memo']")
        memo_box.clear()
        memo_box.send_keys(memo)   
    def withdrawal_next_btn(self):
        next_btn=self.driver.find_element_by_xpath(
                "//button[@class='form-control SignIn ladda-button']")
        next_btn.click()
    def withdrawal_authenticator_otp_fill(self):
        try:
            otp = WebDriverWait(self.driver, 30).until(
        EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='OTP']")))
            otp.clear()
            time.sleep(3)
            otp.send_keys(self.get_OTP())
            otp.send_keys(Keys.ENTER)
        except TimeoutException as e:
            print(e)
    def is_otp_window_present(self):
        try:
            otp = WebDriverWait(self.driver, 30).until(
        EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='OTP']")))
            return otp.is_displayed()
        except TimeoutException as e:
            print(e)
            return False
    
    def confirm_withdrawal_next_btn(self):
        try:
            btn=self.driver.find_element_by_xpath("//button[@class='ladda-button']")
            btn.click()
        except Exception as e:
            print(e)
    def get_crypto_balances(self):
        tbody=self.driver.find_elements_by_tag_name("tbody")[2]
        rows=tbody.find_elements_by_tag_name("tr")
        for row in rows:
            cols=row.find_elements_by_tag_name("td")
            crypto_name=cols[0].text.replace("(",")").split(")")[1]
            crypto_balance=float(cols[1].text.replace(",",""))
            self.wallets[crypto_name.lower().strip(" ")]=crypto_balance
    def crypto_balances(self):
        self.koin_wallet_page()
        try:
            self.get_crypto_balances()
        except:
            time.sleep(5)
            self.get_crypto_balances()
    def update_balances(self):
        self.crypto_balances()
        self.get_inr_balance()
    
    ########################################################################
    def withdraw_crypto(self,crypto,volume,address,tag=123456):
        if crypto.lower()=="neo":
            volume=int(float(volume))
        else:
            volume=float(math.floor(volume*(10**4)))/(10**4)
        self.crypto_withdrawal_page(crypto)
        #self.driver.get(self._base_url)
        #self.koin_wallets_page()
        #self.search_koin_koinwallet(crypto)
        #time.sleep(1)
        #self.click_withdraw_walletpage()
        
        while not (self.driver.current_url==self._base_withdrawal_url+self._fullforms[crypto]):
            time.sleep(1)
        self.fill_withdrawal_volume(volume)
        self.fill_withdrawal_dest_addr(address)
        if crypto=="xrp":
            self.fill_withdrawal_tag(tag)
        if crypto=="xlm":
            self.fill_withdrawal_memo(tag)
        time.sleep(6)
        self.withdrawal_next_btn()
        time.sleep(1)
        self.withdrawal_authenticator_otp_fill()
        time.sleep(10)
        while(self.is_otp_window_present()):
            try:
                self.withdrawal_authenticator_otp_fill()
                self.confirm_withdrawal_next_btn()
            except:
                pass
            time.sleep(5)
        #self.fill_OTP()
        self.withdrawal(crypto,volume)
    #############################################################
