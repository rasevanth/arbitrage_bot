#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 15:05:25 2018

@author: revanth
"""

import pyotp
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from wallet.wallet import Wallets
class Bitbns(Wallets):

    def __init__(self):
        self._email_id="##########"
        self._password="######"
        self._key="#################"
        self._base_url="https://bitbns.com/"
        self._login_url="https://bitbns.com/trade/#/login"
        self._market_base_url="https://bitbns.com/trade/#/"
        self._precision_digits={
                "eosd":{"trade":2,"deposit":4,"withdraw":4},
                "gnt":{"trade":2,"deposit":0,"withdraw":0},
                "qtum":{"trade":2,"deposit":0,"withdraw":0},
                "qkc":{"trade":2,"deposit":0,"withdraw":0},
                "storm":{"trade":2,"deposit":0,"withdraw":0},
                "zrx":{"trade":2,"deposit":0,"withdraw":0},
                "act":{"trade":2,"deposit":2,"withdraw":2},
                "cpx":{"trade":2,"deposit":2,"withdraw":2},
                "rep":{"trade":2,"deposit":2,"withdraw":2},
                "btc":{"trade":8,"deposit":4,"withdraw":4},
                "bch":{"trade":4,"deposit":4,"withdraw":4},
                "blz":{"trade":2,"deposit":0,"withdraw":0},
                "ada":{"trade":1,"deposit":1,"withdraw":1},
                "dash":{"trade":4,"deposit":2,"withdraw":2},
                "dbc":{"trade":2,"deposit":2,"withdraw":2},
                "dgb":{"trade":0,"deposit":0,"withdraw":0},
                "dgd":{"trade":4,"deposit":2,"withdraw":2},
                "doge":{"trade":0,"deposit":0,"withdraw":0},
                "efx":{"trade":2,"deposit":2,"withdraw":2},
                "etn":{"trade":1,"deposit":0,"withdraw":0},
                "eth":{"trade":4,"deposit":3,"withdraw":3},
                "gas":{"trade":4,"deposit":3,"withdraw":3},
                "icx":{"trade":2,"deposit":0,"withdraw":0},
                "loom":{"trade":2,"deposit":0,"withdraw":0},
                "ltc":{"trade":4,"deposit":3,"withdraw":3},
                "lrc":{"trade":2,"deposit":0,"withdraw":0},
                "xmr":{"trade":4,"deposit":2,"withdraw":2},
                "xem":{"trade":2,"deposit":0,"withdraw":0},
                "neo":{"trade":0,"deposit":0,"withdraw":0},
                "nexo":{"trade":2,"deposit":0,"withdraw":0},
                "ncash":{"trade":0,"deposit":0,"withdraw":0},
                "omg":{"trade":2,"deposit":0,"withdraw":0},
                "ont":{"trade":2,"deposit":2,"withdraw":2},
                "poly":{"trade":1,"deposit":1,"withdraw":1},
                "powr":{"trade":2,"deposit":0,"withdraw":0},
                "qlc":{"trade":2,"deposit":2,"withdraw":2},
                "rpx":{"trade":2,"deposit":2,"withdraw":2},
                "req":{"trade":1,"deposit":0,"withdraw":0},
                "xrp":{"trade":2,"deposit":2,"withdraw":2},
                "sia":{"trade":0,"deposit":0,"withdraw":0},
                "xlm":{"trade":2,"deposit":2,"withdraw":2},
                "sub":{"trade":2,"deposit":0,"withdraw":0},
                "trx":{"trade":0,"deposit":0,"withdraw":0},
                "ven":{"trade":2,"deposit":0,"withdraw":0},
                "xvg":{"trade":2,"deposit":2,"withdraw":2},
                "wan":{"trade":2,"deposit":2,"withdraw":2},
                "waves":{"trade":2,"deposit":2,"withdraw":2},
                "wpr":{"trade":1,"deposit":0,"withdraw":0},
                "zil":{"trade":0,"deposit":0,"withdraw":0},
                "usdt":{"trade":2,"deposit":0,"withdraw":0},
                }
        Wallets.__init__(self)
    def start_page(self):
        self.driver=webdriver.Firefox()
        self.driver.get(self._base_url)
    
    def sign_in_page(self):
        self.driver=webdriver.Firefox()
        self.driver.get(self._login_url)
    
    def close_popup(self):
        try:
            cross_btn=WebDriverWait(self.driver,2).until(
                EC.element_to_be_clickable((By.XPATH,"//button[@class='js-modal__close c-btn--size2 c-btn c-btn--outline']")))
            cross_btn.click()
        except  TimeoutException as e:
            #print(e,"failed closing popup")
            pass
    def fill_email_id(self):
        try:
            email_box=WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter Your Email ID:']")))
            email_box.clear()
            email_box.send_keys(self._email_id)
        except NoSuchElementException as e:
            print(e)
            print('failed filling email')
    def fill_password(self):
        pwd_box=self.driver.find_element_by_xpath("//input[@placeholder='Password:']")
        pwd_box.clear()
        pwd_box.send_keys(self._password)
    def press_login_btn(self):
        try:
            login_btn=WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "loginnext")))
            login_btn.click()
        except TimeoutException as e:
            print(e,"failed_clicking_element")
    def login_first_prompt(self):
        self.close_popup()
        self.fill_email_id()
        self.fill_password()
        self.press_login_btn()
    def get_OTP(self):
        return pyotp.TOTP(self._key).now()
    
    def fill_OTP(self):
        try:
            otp = WebDriverWait(self.driver, 30).until(
        EC.presence_of_element_located((By.NAME, "OTP")))
            otp.clear()
            time.sleep(2)
            otp.send_keys(self.get_OTP())
        except NoSuchElementException as e:
            print(e)
    def press_verify_btn(self):
        verify_btn=self.driver.find_element_by_id("step2next")
        verify_btn.click()
    def login_second_prompt(self):
        self.fill_OTP()
        self.press_verify_btn()

    def check_terms(self):
        try:
            rows=WebDriverWait(self.driver,10).until(
            EC.presence_of_all_elements_located(
                    (By.XPATH,"//label[@class='c-radio__labelText u-padding-left-0x']")))
            for row in rows:
                row.click()
            return True
        except NoSuchElementException as e:
            print(e)
            print("failed checking terms")
            return False
    def click_accept_terms_btn(self,boolean):
        if boolean:
            btn=self.driver.find_element_by_xpath(
            "//button[@class='c-btn--minWidth c-btn c-btn--primary arrow arrow-right']")
            btn.click()
        else:
            pass
            
    def agree_terms(self):
        check_present=self.check_terms()
        self.click_accept_terms_btn(check_present)
        if check_present:
            time.sleep(3)
    ########################### ########################
    def sign_in(self):
        self.sign_in_page()
        self.login_first_prompt()
        self.login_second_prompt()
        self.agree_terms()
    ######################################################################
    def is_signed_in(self):
        try:
            wallet_link=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH,"//a[@title='Wallet Balance']")))
            return wallet_link.is_displayed()
        except TimeoutException as e:
            print(e)
            return False
    #############################################################################################         
    def sign_out(self):
        profile=self.driver.find_element_by_xpath("//div[@title='User Profile']")
        signout_link=self.driver.find_element_by_xpath("//div[@class='bb-loginTooltip__item c-links']")
        ActionChains(self.driver).move_to_element(profile).move_to_element(
            signout_link).click(signout_link).perform()
    ###################################################################################
    
    ########################################################################
    def close(self):
        self.driver.close()
