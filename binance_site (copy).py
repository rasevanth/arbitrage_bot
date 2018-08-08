


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 14:24:23 2018

@author: chennam
"""
import math
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceWithdrawException
import requests
import json
class Binance:
    def __init__(self):
        self.__api_key="#########"
        self.__secret_key="############"
        self.__client=Client(self.__api_key,self.__secret_key)
        self._info=self.exchange_info()
    def exchange_info(self):
        return self.__client.get_exchange_info()
    def deposit_credentials(self,crypto):
        credentials=self.__client.get_deposit_address(asset=crypto)
        if credentials["success"]:
            return credentials
        else:
            return self.deposit_credentials(crypto)
    def coin_info(self,coin,base="btc"):
        coin_ex=coin.upper()+base.upper()
        return self.__client.get_symbol_info(coin_ex)
    def deposit_enable(self,coin):
        s=requests.get("https://www.binance.com/assetWithdraw/getAllAsset.html")
        a=json.loads(s.text)
        for each in a:
            if each["assetCode"]==coin.upper():
                return each["enableCharge"]
    def withdraw_enable(self,coin):
        s=requests.get("https://www.binance.com/assetWithdraw/getAllAsset.html")
        a=json.loads(s.text)
        for each in a:
            if each["assetCode"]==coin.upper():
                return each["enableWithdraw"]
    def system_status(self):
        return self.__client.get_system_status()
    def account_info(self):
        return self.__client.get_account()
    def account_status(self):
        return self.__client.get_account_status()
    def withdraw_crypto(self,crypto,withdraw_amount,crypto_address,crypto_tag=None):
        if (crypto.lower()=="neo"):
            withdraw_amount=int(float(withdraw_amount))
        elif (crypto.lower()=="qtum"):
            withdraw_amount=int(float(withdraw_amount))+float(self.withdrawal_fee(crypto))
            if withdraw_amount>float(self.balance(crypto)):
                withdraw_amount=withdraw_amount-1
        if (crypto_tag==None):
            try:
                result = self.__client.withdraw(
                    asset=crypto.upper(),
                    address=crypto_address,
                    amount=withdraw_amount)
            except BinanceAPIException as e:
                print(e)
            except BinanceWithdrawException as e:
                print(e)
                self.withdraw_crypto(crypto,withdraw_amount,crypto_address)
            else:
                print("Success")
        else:
            try:
                result= self.__client.withdraw(
                    asset=crypto.upper(),
                    address=crypto_address,
                    addressTag=crypto_tag,
                    amount=withdraw_amount)
            except BinanceAPIException as e:
                print(e)
            except BinanceWithdrawException as e:
                print(e)
                self.withdraw_crypto(crypto,withdraw_amount,crypto_address,crypto_tag)
            else:
                print("Success")
    def withdrawal_fee(self,crypto):
        return self.__client.get_withdraw_fee(asset=crypto)
    def get_balance(self,crypto):
        try:
            return self.__client.get_asset_balance(asset=crypto)
        except BinanceWithdrawException:
            self.balance(crypto)
        except BinanceAPIException:
            self.balance(crypto)
    def balance(self,crypto):
        bal=self.get_balance(crypto)
        if isinstance(bal,dict):
            return bal
        return self.balance(crypto)
    def withdraw_history(self):
        return self.__client.get_withdraw_history()
    def place_market_order(self,crypto,order_type,quantity,base="btc"):
        symbol=crypto+base
        lot_precision=self.format_specifics(crypto)[1]
        quantity=float(math.floor(float(quantity)*(10**lot_precision)))/(10**lot_precision)
        if order_type.lower()=="buy":
            order = self.__client.order_market_buy(
                symbol=symbol.upper(),
                quantity=str(quantity))
        elif order_type.lower()=="sell":
            bal=float(self.balance(crypto)["free"])
            if quantity>bal:
                quantity=quantity-lot_precision
            order = self.__client.order_market_sell(
                symbol=symbol.upper(),
                quantity=str(quantity))
        return order
    def format_specifics(self,crypto,base="btc"):
        for coin in self._info["symbols"]:
            if coin["symbol"]==crypto.upper()+base.upper():
                price_precision=-int(math.log10(float(coin["filters"][0]["tickSize"])))
                lot_precision=-int(math.log10(float(coin["filters"][1]["stepSize"])))
                return price_precision,lot_precision
    def place_limit_order(self,crypto,order_type,quantity,price,base="btc"):
        symbol=crypto+base
        price_precision,lot_precision=self.format_specifics(crypto)
        if order_type.lower()=="buy":
            order = self.__client.order_limit_buy(
                symbol=symbol.upper(),
                quantity=str(float(math.floor(float(quantity)*(10**lot_precision)))/(10**lot_precision)),
                price=str(float(math.floor(float(price)*(10**price_precision)))/(10**price_precision)))
        elif order_type.lower()=="sell":
            order = self.__client.order_limit_sell(
                symbol=symbol.upper(),
                quantity=str(float(math.floor(float(quantity)*(10**lot_precision)))/(10**lot_precision)),
                price=str(float(math.floor(float(price)*(10**price_precision)))/(10**price_precision)))
        return order
    def orderbook(self,crypto,base="btc"):
        symbol=crypto+base
        try:
            return self.__client.get_order_book(symbol=symbol.upper())
        except :
            self.orderbook(crypto,base="btc")
    def buy_vol_decider(self,crypto,amount):
        cum_amount=0
        cum_vol=0
        for i,each in enumerate(self.orderbook(crypto)["asks"]):
            cum_amnt=cum_amount+float(each[0])*float(each[1])*1.001
            cum_vol=cum_vol+float(each[1])
            if cum_amnt>amount:
                prev_amnt=cum_amnt-float(each[0])*float(each[1])*1.001
                cum_vol=cum_vol-float(each[1])+(amount-prev_amnt)/(1.001*float(each[0]))
                break
        return cum_vol
    def open_orders(self,crypto,base="btc"):
        symbol=crypto+base
        return self.__client.get_open_orders(symbol=symbol.upper())
    def cancel_order(self,crypto,order_id,base="btc"):
        symbol=crypto+base
        return self.__client.cancel_order(
                                symbol=symbol.upper(),
                                orderId=order_id)
    def order_status(self,crypto,order_id,base="btc"):
        symbol=crypto+base
        return self.__client.get_order(
                                symbol=symbol.upper(),
                                orderId=order_id)
    def place_sell_order(self,crypto):
        vol=self.balance(crypto)["free"]
        self.place_market_order(crypto,"sell",vol)
    def place_buy_order(self,crypto):
        try:
            amount=float(self.balance("btc")["free"])
            if amount>0.001:
                vol=self.buy_vol_decider(crypto,amount)
                self.place_market_order(crypto,"buy",vol)
        except Exception as e:
            print(e)
            self.place_buy_order(crypto)
