#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 21:58:44 2018

@author: chennam
"""

from collections import defaultdict,OrderedDict
from threading import Thread,Lock

fees={
    "bitbns":0.25/100,
    "koinex":0.15/100,
    "binance":0.1/100
}
koinex_withdrawal_dict={'xrp': 0.25,'eth': 0.003,'btc': 0.0005,'cmt': 9,'elf': 3.5,'poly': 5,'zco': 50,'iost': 85,
'zil': 40,'ont': 0,'xrb': 0.05,'ncash': 120,'aion': 1.5,'gas': 0,'neo': 0,'xlm': 0.02,'trx': 60,'gnt': 10,
'ae': 2,'bat': 10,'zrx': 5,'omg': 0.25,'req': 15,'bch': 0.001,'ltc': 0.01,'act':0.2,'eos':0.4,"snt":30,"rep":0.1,
"qkc":15,"xzc": 0.02,"tusd":4,}

bitbns_withdrawal_dict={"zrx":3,"rep":0.1,"cpx":1,"act":0.1,"btc":0.0005,"bch":0.001,"blz":10,"ada":1,"dgd":0.01,
"dash":0.02,"dbc":0.1,"dgb":1,"doge":2,"efx":1,"etn":5,"eos":0.5,"eth":0.002,"gas":0,"icx":1.5,"ltc":0.01,
"loom":10,"lrc":10,"xmr":0.02,"xem":1,"neo":0,"nexo":30,"ncash":200,"omg":0.2,"ont":0.1,"poly":5,"powr":8,
"qlc":0.1,"rpx":0.1,"req":40,"xrp":0.1,"sia":1,"xlm":0.01,"sub":10,"trx":60,"ven":0.5,"xvg":2,"wan":0.01,
"waves":0.01,"wpr":30,"zil":50,"eosd":25,"gnt":10,"qtum":0.01,"qkc":20,"storm":150,"usdt":10}

binance_withdrawal_dict={'bnb': 1.0,'btc': 0.0005,'neo': 0.0,'eth': 0.01,'ltc': 0.01,'qtum': 0.01,'eos': 0.3,
 'snt': 41.0,'bnt': 0.9,'gas': 0.0,'bcc': 0.001,'btm': 5.0,'usdt': 3.8,'hcc': 0.0005,'hsr': 0.0001,'oax': 6.1,
'dnt': 56.0,'mco': 0.53,'icn': 3.7,'zrx': 2.8,'omg': 0.38,'wtc': 0.4,'lrc': 7.0,'llt': 67.8,'yoyo': 35.0,
'trx': 60.0,'strat': 0.1,'sngls': 55.0,'bqx': 1.5,'knc': 2.3,'snm': 18.0,'fun': 101.0,'link': 9.9,'xvg': 0.1,
 'ctr': 35.0,'salt': 1.8,'mda': 4.6,'iota': 0.5,'sub': 8.3,'etc': 0.01,'mtl': 1.2,'mth': 45.0,'eng': 1.9,
 'ast': 12.3,'dash': 0.002,'btg': 0.001,'evx': 3.3,'req': 24.2,'vib': 27.0,'powr': 10.6,'ark': 0.1,'xrp': 0.25,
 'mod': 3.0,'enj': 34.0,'storj': 4.3,'ven': 1.1,'kmd': 0.002,'rcn': 38.0,'nuls': 0.9,'rdn': 2.5,'xmr': 0.04,
'dlt': 18.7,'amb': 8.3,'bat': 12.0,'zec': 0.005,'bcpt': 11.0,'arn': 2.9,'gvt': 0.21,'cdt': 83.0,'gxs': 0.3,
'poe': 126.0,'qsp': 21.0,'bts': 1.0,'xzc': 0.02,'lsk': 0.1,'tnt': 46.0,'fuel': 62.0,'mana': 35.0,'bcd': 1.0,'dgd': 0.03,
 'adx': 5.6,'ada': 1.0,'ppt': 0.29,'cmt': 11.0,'xlm': 0.01,'cnd': 56.0,'lend': 75.0,'wabi': 4.7,'sbtc': 0.0005,
'bcx': 0.5,'waves': 0.002,'tnb': 94.0,'gto': 15.0,'icx': 1.3,'ost': 23.0,'elf': 3.3,'aion': 1.7,'cvc': 10.9,
'rep': 0.1,'gnt': 5.7,'etf': 1.0,'brd': 6.2,'nebl': 0.01,'vibe': 22.8,'lun': 0.3,'chat': 42.9,'rlc': 2.2,
 'ins': 3.0,'iost': 77.6,'steem': 0.01,'nano': 0.01,'ae': 1.2,'via': 0.01,'blz': 8.4,'sys': 0.001,
 'rpx': 1.0,'ncash': 190.5,'poa': 0.01,'ont': 0.1,'zil': 32,'storm': 107.0,'xem': 4.0,'wan': 0.1,'wpr': 42.3,
 'qlc': 1.0,'grs': 0.2,'cloak': 0.02,'loom': 9.6,'bcn': 1.0,'tusd': 3.47,'zen': 0.002,'sky': 0.01,'theta': 24.0,
'iotx': 52.7,'edo': 2.4,'wings': 8.6,'nav': 0.2,'trig': 19.1,'appc': 9.4,'pivx': 0.02,"qkc":38.21}

withdrawal_fee={
    "koinex":koinex_withdrawal_dict,
    "bitbns":bitbns_withdrawal_dict,
    "binance":binance_withdrawal_dict
}
def arbitrage_calculation(indian_site,international_site):
    stage1_arb=defaultdict(dict)
    stage2_arb=defaultdict(dict)
    indian_dict_ratio=indian_site.cryptos_list_ratio()
    international_dict=international_site.cryptos_list()
    indian_dict_price=indian_site.cryptos_list_price()
    indian_name=indian_site.__class__.__name__
    international_name=international_site.__class__.__name__
    for coin in indian_dict_ratio.keys():
        if coin in international_dict.keys():
            stage1_arb[coin]["arb"]=((international_dict[coin][1]*(1-fees[international_name.lower()]))/
                                    (indian_dict_ratio[coin][0]*(1+fees[indian_name.lower()])))
            
            stage1_arb[coin]["buy"]=indian_dict_price[coin][0]
            stage1_arb[coin]["sell"]=international_dict[coin][1]
            stage2_arb[coin]["arb"]=((indian_dict_ratio[coin][1]*(1-fees[indian_name.lower()]))/
                                    (international_dict[coin][0]*(1+fees[international_name.lower()])))
            stage2_arb[coin]["buy"]=international_dict[coin][0]
            stage2_arb[coin]["sell"]=indian_dict_price[coin][1]
            
    stage1_arb=OrderedDict(sorted(stage1_arb.items(),key=lambda t:t[1]["arb"],reverse=True))
    stage2_arb=OrderedDict(sorted(stage2_arb.items(),key=lambda t:t[1]["arb"],reverse=True))
    return stage1_arb,stage2_arb
def direct_arbitrage(indian_site,international_site,indian_exclusion_dict,international_exclusion_dict):
    indian_dict=indian_site.cryptos_list_ratio()
    indian_arb,international_arb=arbitrage_calculation(
        indian_site,international_site)
    indian_arb_keys=indian_dict.keys()
    for each in indian_arb_keys:
        if (each in indian_exclusion_dict["withdraw"]) or (each in indian_exclusion_dict["deposit"]):
           # print(each,"excluded")
            indian_arb.pop(each,None)
        
        if (each in indian_exclusion_dict["deposit"] )or (each in international_exclusion_dict["withdraw"]):
            #print(each,"excluded")
            international_arb.pop(each,None)
    return indian_arb,international_arb
def thresholding(arb_dict,value=1):
    popped_list=[]
    for coin in arb_dict.keys():
        if arb_dict[coin]["arb"] <value:
            popped_list.append(coin)
    for each in popped_list:
            arb_dict.pop(each)
    return arb_dict
#thresholding(b_b[1],1)
def all_sites_arbitrage_dict(list_of_indian_sites,list_of_internatonal_sites,
                             list_of_indian_sites_exclusion_dict,list_of_international_sites_exclusion_dict):
    arbitrage_dict=defaultdict(dict)
    for index,indian_site in enumerate(list_of_indian_sites):
        for i_index,international_site in enumerate(list_of_internatonal_sites):
            indian_name=indian_site.__class__.__name__
            international_name=international_site.__class__.__name__
            direct_arb=direct_arbitrage(
                    indian_site,international_site,list_of_indian_sites_exclusion_dict[index],
                list_of_international_sites_exclusion_dict[i_index])
            arbitrage_dict[indian_name+"_"+international_name]=thresholding(direct_arb[0],0.99)
            arbitrage_dict[international_name+"_"+indian_name]=thresholding(direct_arb[1],0.99)
    return arbitrage_dict
def names_of_sites(list_of_sites):
    sites_name_list=[]
    for site in list_of_sites:
        sites_name_list.append(site.__class__.__name__)
    return sites_name_list

def triangular_arbitrage(list_of_indian_sites,list_of_international_sites,
                         list_of_indian_sites_coin_exclusion_dict,list_of_international_sites_coin_exclusion_dict,
                        indian_deposit_exclusion_names=[],international_exclusion_names=[],
                        indian_withdrawal_exclusion_names=[]):
    
    total_arb=defaultdict(dict)
    final_list=list()
    indian_names=names_of_sites(list_of_indian_sites)
    
    international_names=list(set(names_of_sites(list_of_international_sites))-set(international_exclusion_names))
    indian_deposit_names=list(set(indian_names)-set(indian_deposit_exclusion_names))
    indian_withdrawal_names=list(set(indian_names)-set(indian_withdrawal_exclusion_names))

    full_arbitrage=all_sites_arbitrage_dict(list_of_indian_sites,list_of_international_sites,
                         list_of_indian_sites_coin_exclusion_dict,list_of_international_sites_coin_exclusion_dict)
    for buyindian_site in indian_deposit_names:
        for midint_site in international_names:
            for sellindian_site in indian_withdrawal_names:
                arb1_dict=full_arbitrage[buyindian_site+"_"+midint_site]
                arb2_dict=full_arbitrage[midint_site+"_"+sellindian_site]
                for coin1 in arb1_dict.keys():
                    for coin2 in arb2_dict.keys():
                        if (arb1_dict[coin1]["arb"]*arb2_dict[coin2]["arb"]>1.01):
                            total_arb[buyindian_site+"_"+midint_site+"_"+sellindian_site][coin1+"_"+coin2]=\
                        ({coin1:arb1_dict[coin1],coin2:arb2_dict[coin2]},arb1_dict[coin1]["arb"]*
                                                                               arb2_dict[coin2]["arb"])
                        
    for sites,coins_arb_dict in total_arb.items():
        for coins,coins_tuple in coins_arb_dict.items():
            final_list.append((sites,coins,coins_tuple))
    final_list=sorted(final_list,key=lambda t:t[2][1],reverse=True)[:50]
    return final_list
def refine_triangular_arbitrage(triangular_arbitrage_list,threshold):
    ref_list=[]
    for each in triangular_arbitrage_list:
        if not each[2][1]<threshold:
            ref_list.append(each)
    return ref_list

def validate_arb_form(list_of_arbs):
    def dict_in_dict():
        return defaultdict(dict)
    validate_dict=defaultdict(dict_in_dict)
    for arb in list_of_arbs:
        buyIndian,midInt,sellIndian=arb[0].split("_")
        coin1,coin2=arb[1].split("_")
        if coin1 not in validate_dict[buyIndian].keys():
            #print(coin1,buyIndian)
            validate_dict[buyIndian]["buy"][coin1]=arb[2][0][coin1]#.pop("sell")
        if coin2 not in validate_dict[sellIndian].keys():
            #print(coin2,sellIndian)
            validate_dict[sellIndian]["sell"][coin2]=arb[2][0][coin2]#.pop("buy")
    return validate_dict
def buy_amount_decider(quote_price,total_amount,sell_orderbook):
    cum_amnt=0
    cum_vol=0
    global new_quote_price
    lob=len(sell_orderbook)
    for ii,order_row in enumerate(sell_orderbook):
        if order_row[1]>quote_price:
            new_quote_price=sell_orderbook[ii-1][1]
            break
        cum_amnt=cum_amnt+sell_orderbook[ii][0]*sell_orderbook[ii][1]
        cum_vol=cum_vol+sell_orderbook[ii][0]
        
        if cum_amnt>total_amount:
            prev_amount=cum_amnt-order_row[0]*order_row[1]
            cum_vol=(cum_vol-sell_orderbook[ii][0])+((total_amount-prev_amount)/sell_orderbook[ii][1])
            cum_amnt=total_amount
            new_quote_price=sell_orderbook[ii][1]
            break
        if ii==lob-1:
            new_quote_price=sell_orderbook[ii][1]
            break
    try:
        avg_price=round(cum_amnt/cum_vol,2)
    except ZeroDivisionError:
        avg_price=-1
    return cum_vol,cum_amnt,new_quote_price,avg_price

def sell_amount_decider(quote_price,total_amount,buy_orderbook):
    cum_amount=0
    cum_vol=0
    lob=len(buy_orderbook)
    global new_quote_price
    for i,order_row in enumerate(buy_orderbook):
        
        if order_row[1]<quote_price:
            new_quote_price=buy_orderbook[i-1][1]
            break
        cum_amount=cum_amount+order_row[0]*order_row[1]
        cum_vol=cum_vol+order_row[0]
        
        if cum_amount>total_amount:
            prev_amount=cum_amount-buy_orderbook[i][0]*buy_orderbook[i][1]
            cum_vol=(cum_vol-order_row[0])+((total_amount-prev_amount)/buy_orderbook[i][1])
            cum_amount=total_amount
            new_quote_price=buy_orderbook[i][1]
            break
        if i==lob-1:
            new_quote_price=buy_orderbook[i][1]
            break
    try:
        avg_price=round(cum_amount/cum_vol,2)
    except ZeroDivisionError:
        avg_price=-1
    return cum_vol,cum_amount,new_quote_price,avg_price

        
def get_coins(list_of_arbs):
    coins_dict=defaultdict(list)
    for each in list_of_arbs.keys():
        coins_dict[each.lower()]=list(list_of_arbs[each]["buy"].keys())+list(list_of_arbs[each]["sell"].keys())
    return coins_dict
def get_orderbooks_for_list_of_coins(list_of_coins,orderbook_mod,name,live_orderbooks,lock):
    orderbook_dict=dict()
    for coin in list_of_coins:
        orderbook_dict[coin]=orderbook_mod.orderbook(coin)
    lock.acquire()
    live_orderbooks[name.lower()]=orderbook_dict
    lock.release()

def get_site_orderbooks(orderbooks,coins_list_dict):
    lock=Lock()
    live_orderbooks=dict()
    threads=[]
    for i,module in enumerate(orderbooks):
        name=module.__class__.__name__
        #print(name)
        threads.append(Thread(target=get_orderbooks_for_list_of_coins,args=(coins_list_dict[name.lower()],module,name,live_orderbooks,lock,)))
        threads[i].start()
    for thread in threads:
        thread.join()
    return live_orderbooks
def approved_triangular_arbitrages(list_of_arbs,list_of_balances,orderbooks):
    expected_arb_list=list()
    list_of_coins=get_coins(validate_arb_form(list_of_arbs))
    list_of_orderbooks=get_site_orderbooks(orderbooks,list_of_coins)
    for arb in list_of_arbs:
    #print(arb)
        buyIndian,inter,sellIndian=arb[0].split("_")
        coin1,coin2=arb[1].split("_")
        buy_arb_details=arb[2][0][coin1]
        expected_buy_price=buy_arb_details["buy"]
        expected_buy_arb=buy_arb_details["arb"]
        coin1_sell_orderbook=list_of_orderbooks[buyIndian.lower()][coin1]["sell"]
        amount=list_of_balances[buyIndian.lower()]
        if expected_buy_arb<1:
            expected_buy_arb=1
        buy_quote_price=expected_buy_price*expected_buy_arb
        buy_vol,buy_amnt,new_buy_quote_price,avg_buy_price=buy_amount_decider(
            buy_quote_price,amount,coin1_sell_orderbook)
        if avg_buy_price==0:
            avg_buy_price=-1
        new_buy_arb=buy_arb_details["sell"]/avg_buy_price
    
        sell_arb_details=arb[2][0][coin2]
        expected_sell_price=sell_arb_details["sell"]
        expected_sell_arb=sell_arb_details["arb"]
        coin2_buy_orderbook=list_of_orderbooks[sellIndian.lower()][coin2]["buy"]
    
        sell_quote_price=expected_sell_price/expected_sell_arb
        sell_vol,sell_amnt,new_sell_quote_price,avg_sell_price=sell_amount_decider(
        sell_quote_price,amount,coin2_buy_orderbook)
        if avg_sell_price==0:
            avg_sell_price=-1
        new_sell_arb=avg_sell_price/sell_arb_details["buy"]
    
        new_total_arb=new_buy_arb*new_sell_arb
        expected_details=arb[2]
        amount_to_be_traded=min(buy_amnt,sell_amnt)
        
        withdrawal_cost=withdrawal_fee[buyIndian.lower()][coin1]*avg_buy_price+\
                                withdrawal_fee[inter.lower()][coin2]*avg_sell_price
        if not amount_to_be_traded==0:
            new_total_arb_withdraw=new_total_arb*(1-(withdrawal_cost/(amount_to_be_traded*0.9)))
        else:
            new_total_arb_withdraw=0
        real_details={
            coin1:{"new_arb":new_buy_arb,"quote_price":new_buy_quote_price,"avg price":avg_buy_price,
               "vol":buy_vol,"amnt":buy_amnt},
            coin2:{"new_arb":new_sell_arb,"quote_price":new_sell_quote_price,"avg price":avg_sell_price,
              "vol":sell_vol,"amnt":sell_amnt},
            "amount":amount_to_be_traded
        }
        if new_total_arb_withdraw>1.015 and new_total_arb_withdraw<2 and amount_to_be_traded*(new_total_arb_withdraw-1)>200:
            expected_arb_list.append((arb[0],arb[1],(expected_details,real_details,new_total_arb_withdraw)))
    return sorted(expected_arb_list,key=lambda t:(t[2][2]-1)*t[2][1]["amount"],reverse=True)
def main(indian_sites_list,international_sites_list,
         indian_exclusion_list,international_exclusion_list,balance_list,orderbooks,
         indian_deposit_exclusion_names=[],international_exclusion_names=[],
         indian_withdrawal_exclusion_names=[]):
    triangle_arbitrage=triangular_arbitrage(indian_sites_list,international_sites_list,
                         indian_exclusion_list,international_exclusion_list,
            indian_deposit_exclusion_names=[],international_exclusion_names=[],
         indian_withdrawal_exclusion_names=[])
    
    refined_triangular_arb=refine_triangular_arbitrage(triangle_arbitrage,1.01)
    
    return approved_triangular_arbitrages(refined_triangular_arb,balance_list,orderbooks)