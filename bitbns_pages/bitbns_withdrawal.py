#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 15:09:41 2018

@author: revanth
"""
import time
import math
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.action_chains import ActionChains
from bitbns_pages.bitbns_base import Bitbns
from bitbns_pages.mail_verify import verify_mail
class Bitbns_withdrawal(Bitbns):
    def __init__(self):
        Bitbns.__init__(self)
        self._wallet_url="https://bitbns.com/trade/#/wallets"
    def navigate_to_wallet_page(self):
        time.sleep(1)
        wallet_link=self.driver.find_element_by_xpath("//a[@title='Wallet Balance']")
        wallet_link.click()
    def go_to_wallet_page(self):
        self.driver.get(self._wallet_url)
    def get_wallet_window(self,crypto):
        try:
            bwallets=WebDriverWait(self.driver,30).until(EC.presence_of_all_elements_located(
                        (By.XPATH,"//div[@class='bb-wallets__wallet']")))
            for bwallet in bwallets:
                if crypto.upper() in bwallet.get_attribute("innerText"):
                    #print(crypto)
                    scroll=self.driver.find_element_by_xpath(
                    "//div[@class='bb-wallets__wrapper bb-wallets__wrapper--left c-window__main--maxHeight']")
                    scroll.click()
                    bwallet.location_once_scrolled_into_view
                    send=bwallet.find_element_by_xpath(".//div[@data-transtype='withdraw']")
                    send.click()
        except TimeoutException as e:
            print(e,"failed openinig wallet window")
    def fill_crypto_address(self,addr):
        try:
            addr_box=WebDriverWait(self.driver,30).until(EC.element_to_be_clickable(
                    (By.ID,"withdraw__coinAddr")))
            addr_box.location_once_scrolled_into_view
            addr_box.clear()
            addr_box.send_keys(addr)
        except TimeoutException as e:
            print(e)
            print("failed_filling_crypto_address")
    def fill_crypto_tag(self,tag):
        tag_box=self.driver.find_element_by_id("withdraw__coinTag")
        tag_box.clear()
        tag_box.send_keys(tag)
    def fill_crypto_memo(self,memo):
        memo_box=self.driver.find_element_by_id("withdraw__coinMemo")
        memo_box.clear()
        memo_box.send_keys(memo)
    def fill_payment_id(self,payment_id):
        payment_id_box=self.driver.find_element_by_id("withdraw__paymentId")
        payment_id_box.clear()
        payment_id_box.send_keys(payment_id)
    def fill_message(self,message):
        message_box=self.driver.find_element_by_id("withdraw__coinMessage")
        message_box.clear()
        message_box.send_keys(message)
    def fill_volume(self,vol):
        vol_box=self.driver.find_element_by_id("withdraw__coin")
        vol_box.clear()
        vol_box.send_keys(str(vol))
    def fill_withdraw_otp(self):
        otp_box=self.driver.find_element_by_id("withdrawCointuFac__otp")
        otp_box.clear()
        otp_box.send_keys(self.get_OTP())
    def press_withdrawal_btn(self):
        
        btn=self.driver.find_element_by_xpath("//button[@class='c-btn']")
        btn.click()
    def blocked_coins(self):
        black_text=self.driver.find_element_by_xpath("//div[@class='bb-updateHeader u-animated slideInDown']")
        deposit_black_list=[]
        withdrawal_black_list=[]
        erc20_list=["etc","lsk","npxs","trx","req","powr","nexo","lrc","loom","dgd","blz","poly","omg","zrx","gnt","eth","zil","poly","rep","ncash","qkc","wpr","wan","storm","ven","sub"]
        neg_words=["disable","pause","congestion"]
        b_coins=self.addresses_dict.keys()
        for line in black_text.text.split("\n"):
            for each in b_coins:
                if each in line.lower():
                    if any(word in line.lower() for word in neg_words):
                        if "deposit" in line.lower():
                            deposit_black_list.append(each)
                        if "withdraw" in line.lower():
                            withdrawal_black_list.append(each)
            if "erc20" in line.lower():
                if "deposit" in line.lower():
                    deposit_black_list.extend(erc20_list)
                if "withdraw" in line.lower():
                    withdrawal_black_list.extend(erc20_list)
        return deposit_black_list,withdrawal_black_list
    def check_withdrawal_working(self,crypto):
        if crypto not in self.blocked_coins()[1]:
            return True
        else:
            return False
    def check_deposit_working(self,crypto):
        if crypto not  in self.blocked_coins()[0]:
            return True
        else:
            return False
    ######################################################################
    def withdraw_crypto(self,crypto,vol,addr,tag=None):
        self.update_balances()
        self.get_wallet_window(crypto)
        #crypto_bal=self.wallets[crypto]
        self.fill_crypto_address(addr)
        vol_precision=self._precision_digits[crypto]["withdraw"]
        vol=float(math.floor(float(vol)*(10**vol_precision)))/(10**vol_precision)
        self.fill_volume(vol)
        if crypto=="xrp":
            self.fill_crypto_tag(tag)
        if crypto=="xlm":
            self.fill_crypto_memo(tag)
        if (crypto=="etn") or (crypto=="xmr"):
            self.fill_payment_id(tag)
        if crypto=="xem":
            self.fill_message(tag)
        self.fill_withdraw_otp()
        self.press_withdrawal_btn()
        self.press_okay_btn()
        self.withdrawal(crypto,vol)
        time.sleep(150)
        verify_mail()
    ####################################################################################
    def press_okay_btn(self):
        try:
            okay=WebDriverWait(self.driver,30).until(EC.element_to_be_clickable(
                (By.XPATH,"//button[@class='js-focusOnOpen js-modal__close c-btn--size2 c-btn c-btn--outline']")))
            okay.click()
        except TimeoutException as e:
            print(e)
            print("failed_pressing_okay btn")
    def get_crypto_balances(self):
        
        bwallets=WebDriverWait(self.driver,30).until(EC.presence_of_all_elements_located(
                        (By.XPATH,"//div[@class='bb-wallets__wallet']")))
        for bwallet in bwallets:
            leftwrapper=bwallet.find_elements_by_tag_name("div")[0]
            amtwrapper=leftwrapper.find_element_by_class_name("bb-wallet__cryptoAmtWrapper")
            name=amtwrapper.find_elements_by_tag_name("div")[0].text.replace("(",")").split(")")[1]
            bal=float(amtwrapper.find_elements_by_tag_name("div")[1].text.split("\n")[0].replace(",","").strip("Bytes"))
            self.wallets[name.lower()]=bal
    
    def inr_balances(self):
        bal_window=self.driver.find_element_by_id("wallet__balance")
        balance=float(bal_window.find_element_by_xpath(
                "div[@class='u-padding-2x']/div[@class='u-fSize-6 u-textBreak--all']").text.strip("₹").replace(",",""))
        self.wallets["inr"]=balance
    def update_balances(self):
        if not self.driver.current_url==self._wallet_url:
            self.go_to_wallet_page()
        else:
            self.driver.refresh()
        self.close_popup()
        self.get_crypto_balances()
        self.inr_balances()