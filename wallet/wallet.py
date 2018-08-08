#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 14:39:58 2018

@author: revanth
"""
from collections import defaultdict
class Wallets:
    def __init__(self):
        self.__wallets=defaultdict(float)
    @property
    def wallets(self):
        return self.__wallets
    def balance(self,crypto):
        return self.__wallets[crypto.lower()]
    @wallets.setter
    def wallets(self,crypto,balance):
        self.__wallets[crypto.lower()]=float(balance)
    def deposit(self,crypto,deposit_amount):
        self.__wallets[crypto.lower()]+=float(deposit_amount)
    def withdrawal(self,crypto,withdraw_amount):
        self.__wallets[crypto.lower()]-=float(withdraw_amount)


