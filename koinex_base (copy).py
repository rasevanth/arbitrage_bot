#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 14:41:27 2018

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
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from wallet.wallet import Wallets
class Koinex(Wallets):
    
    def __init__(self):
        self._user_name="##############"
        self._password="#############"
        self._key="############"
        self._base_url="http://www.koinex.in"
        self._market_url="https://koinex.in/exchange/inr/"
        self._inr_url="https://koinex.in/INRWallet"
        self._fullforms={"btc":"bitcoin",
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
        Wallets.__init__(self)
        #self.inr_wallet=Wallet()
        #self.crypto_wallet=Wallet()
        
    #open start page

    def get_driver(self):
        self.driver=webdriver.Firefox()
    def start_page(self):
        self.driver=webdriver.Firefox()
        self.driver.get(self._base_url)

    #close the popup at the start pages
    def pop_checkin(self):
        try:
            WebDriverWait(self.driver,10).until(
        EC.element_to_be_clickable((By.XPATH,"//input[@type='checkbox']"))).click()
        except Exception as e:
            print(e)
    
    def pop_up(self):
        self.pop_checkin()
        try :
            elem=self.driver.find_element_by_class_name("solidBtn")
            elem.click()
        except NoSuchElementException:
            print("popup not present")
    #click on the sign in link on any page
    def sign_in_link(self):
        signin=self.driver.find_element_by_link_text('SIGN IN')
        signin.click()
    
    #fill the userid and password on the sign in popup
    def sign_in_fill(self):
        #fill user id
        user_id=self.driver.find_element_by_name("user_name")
        user_id.clear()
        user_id.send_keys(self._user_name)
        #fill password
        password=self.driver.find_element_by_name("password")
        password.clear()
        password.send_keys(self._password)
    
    def dismiss_alert(self):
        Alert(self.driver).dismiss()
    #click on the sign in button
    def sign_in_buttons(self):
        #click next btn
        btn=self.driver.find_element_by_xpath(
                "//div[@class='sign-in-button']/button[1]")
        btn.click()
    #generate the otp
    def get_OTP(self):
        return pyotp.TOTP(self._key).now()
    #fill the otp in signin popup2
    def fill_OTP(self):
        try:
            otp = WebDriverWait(self.driver, 30).until(
        EC.presence_of_element_located((By.NAME, "otp")))
            otp.clear()
            time.sleep(2)
            otp.send_keys(self.get_OTP())
        except TimeoutException as e:
            print(e)
    #check if the signin is true
    ##################################################
    def is_signed_in(self):
        try:
            chen=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.LINK_TEXT, "##username")))
            return chen.is_displayed()
        except TimeoutException as e:
            print(e)
            return False
    ###########################################################################
    #signin to the koinex website
    def sign_in(self):
        self.start_page()
        self.pop_up()
        self.sign_in_link()
        self.sign_in_fill()
        self.sign_in_buttons()
        time.sleep(1)
        self.fill_OTP()
        #self.sign_in_buttons()
        time.sleep(10)
        self.pop_up()
        #print(self.is_signedin())
    
    ##################################################################################
    #click on the nav bar after signin links
    def click_on_link(self,link_name):
        try:
            link=WebDriverWait(self.driver,30).until(
                EC.presence_of_element_located((By.LINK_TEXT,link_name)))
            time.sleep(1)
            link.click()
        except TimeoutException as e:
            print(e)
            print('failed clicking on {} '.format(link_name))
    
    def click_on_name(self):
        self.click_on_link("###########username")
####################################################################################    
    def sign_out(self):
        self.click_on_name()
        self.click_on_link("SIGN OUT")
#######################################################
    def balances(self):
        self.click_on_link("BALANCES")
    
    def koin_wallets_page(self):
        self.balances()
        self.click_on_link("KOIN WALLET")
    ##################################################################################################

    ###################################################################################################
    def navigate_to_inr_wallet_page(self):
        self.balances()
        self.click_on_link("INR WALLET")
        
    def my_history_page(self):
        self.balances()
        self.click_on_link("MY HISTORY")
    def inr_page(self):
        self.driver.get(self._inr_url)
    #click on the crypto_price_row after signin
    def click_on_crypto_price_row(self,crypto):
        try:
            crypto_elem=WebDriverWait(self.driver,30).until(
                EC.presence_of_element_located((By.CLASS_NAME,crypto.upper())))
            crypto_elem.location_once_scrolled_into_view
            time.sleep(1)
            new_elem=WebDriverWait(self.driver,30).until(
                EC.presence_of_element_located((By.CLASS_NAME,crypto.upper())))
            #time.sleep(1)
            ActionChains(self.driver).move_to_element(
                    new_elem).click(new_elem).perform()
            #new_elem.click()
        except TimeoutException as e:
            print(e)
            print('failed clicking on {} row'.format(crypto.upper()))
    #navigate to the marketpage before or after signin
    ######################################################################
    def navigate_to_market_page(self,crypto):
        #self.click_on_crypto_price_row(crypto)
        market=self._market_url+self._fullforms[crypto]
        self.driver.get(market)
    ############################################################################
    def get_inr_text(self):
        try:
            table=self.driver.find_elements_by_tag_name("tbody")[1]
            row=table.find_elements_by_tag_name("tr")[0]
            col=row.find_elements_by_tag_name("td")[0]
            inr_text=float(col.text.rstrip("INR").strip(" ").replace(",",""))
            if isinstance(inr_text,float):
                #print(inr_text)
                #print(isinstance(inr_text,float))
                return inr_text
            else:
                time.sleep(5)
                return self.get_inr_text()
        except ValueError as e:
            #print(e)
            time.sleep(5)
            return self.get_inr_text()
    ##################inr bal##############################################
    def get_inr_balance(self):
        self.inr_page()
        inr_bal=self.get_inr_text()
        self.wallets["inr"]=inr_bal
##############################################################################    
    def close(self):
        self.driver.close()
    #################################################################
#Koinex().sign_in()
