# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 19:38:45 2019

@author: 28723
"""

import pickle
import datetime 
import time
import pandas as pd
import numpy as np
from OkcoinSpotAPI import OKCoinSpot
from OkcoinFutureAPI import OKCoinFuture
import json
from pytz import timezone #timezone('Asia/Shanghai') #东八区
#import warnings
#warnings.filterwarnings("ignore")
apikey = ""
secretkey =  ""
okcoinRESTURL = 'www.okex.com'   #请求注意：国内账号需要 修改为 www.okcoin.cn  

import os
root = 'C:\数字货币cta策略\y1eth'

'''基本参数'''
#tic = time.clock()
#toc = time.clock()
run_tate = 1 # 1为实盘运行   0为测试运行（开平仓交易函数关闭）d12k12
hedge_fund = 762 # 对冲数账字货币现货对应的合约数量 每个户不一样
coin ='eth_usdt'
asset_rate=0.6
need_taobao=1#金本位为1
initial_price=250
#one_coin_asset_rate=1/2
Asset0 = 64745#9558usdt=9360usd  
account_name = 'y1_eth测试'# 账号_版本号
user = '813823246@qq.com'
password = chr(107)+chr(108)+'yecbgnunhdbgba'#chr(97) ord('i')
to = ['813823246@qq.com']
Asset1 = Asset0
#p1=2
#p2=2
#p3=2
if need_taobao==1:
    Asset0 = Asset0*asset_rate#9558usdt=9360usd 
else:
     Asset0 = Asset0*asset_rate/initial_price#9558usdt=9360usd
     
time_pid=pd.DataFrame(np.zeros((1,2)))
pid1=os.getpid()
p1=1
p2=1
p3=1   
# %%
'''数据初始化'''
while(1):
    try:
        pk1 = open(root+'\\buy_total_%s.spydata'%coin,'rb')
        buy_total = pickle.load(pk1)
        pk1.close()
        break
    except:
        buy_total = pd.DataFrame(np.zeros([1,5])) 
        buy_total.iloc[0,:] = '下单时间', '买入方式', '开仓价格', '开仓数量','开仓金额'
        pk1 = open(root+'\\buy_total_%s.spydata'%coin,'wb')
        pickle.dump(buy_total,pk1)
        pk1.close()
        buy_total1 = buy_total
        pk1 = open(root+'\\buy_total1_%s.spydata'%coin,'wb')
        pickle.dump(buy_total1,pk1)
        pk1.close()
        BeijingTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # 北京时间
        while(1):
            try:
                okcoinFuture = OKCoinFuture(okcoinRESTURL,apikey,secretkey)
                break
            except:
                print('\t 期货登陆超时')
                time.sleep(1)
                continue
        while(1):
            try:
                time.sleep(1)
                f_index_eth = okcoinFuture.future_index('eth_usdt').get('future_index') #OKEx合约指数 btc
                break
            except:
                print('\t 获取etc指数超时')
                time.sleep(2)
                continue
        capital_change_total = pd.DataFrame(np.zeros([2,7]))
        capital_change_total.iloc[0,:] = "日期","合约账户资产(币)","合约价值(保证金.币)","可用资金(币)","总资产(美元)","指数(币)","汇率"
        capital_change_total.iloc[1,:] = BeijingTime , Asset0/f_index_eth , 0.0 , Asset0/f_index_eth , float(Asset0) , 0.0 , 0.0
        pk1 = open(root+'\\capital_change_total_%s.spydata'%coin,'wb')
        pickle.dump(capital_change_total,pk1)
        pk1.close()
        capital_change_total1 = capital_change_total
        pk1 = open(root+'\\capital_change_total1_%s.spydata'%coin,'wb')
        pickle.dump(capital_change_total1,pk1)
        pk1.close()
   

#capital_change_total.to_excel('C:/Users/Administrator/Desktop/capital_change_total.xls',index=False, header=False)
while(1):
    time11 = datetime.datetime.now()
    numtime = time11.minute
    numtime1 = time11.minute*100+time11.second
    #print('\t 正在运行中,eth zhuzhong 9500美金账户',time11,'\n')
    print('\t 正在运行中,%s %s %s美金账户'%( coin[:3],account_name,Asset0 ),time11,'\n')
    time.sleep(3)
    #实时收益率计算
    while(1):
        try:
            okcoinSpot = OKCoinSpot(okcoinRESTURL,apikey,secretkey)
            break
        except:
            print('\t 现货登陆超时')
            time.sleep(1)
            continue
            
    while(1):
        try:
            okcoinFuture = OKCoinFuture(okcoinRESTURL,apikey,secretkey)
            break
        except:
            print('\t 期货登陆超时')
            time.sleep(1)
            continue
      
    while(1):
        try:
            f_kline_1hour = okcoinFuture.future_kline('eth_usdt','1hour','quarter','600','')
            assert len(f_kline_1hour)>2
            break
        except:
            print('\t 获取1小时数据超时')
            time.sleep(1)
            continue
        
  
    coin_date = pd.DataFrame(np.zeros([len(f_kline_1hour),len(f_kline_1hour[0])])) #时间 开盘价 最高价 最低价 收盘价 交易量 交易量转化BTC数量
    print ("\t 实时K线数据更新 开始 %s" %time.ctime())
    for i in range(len(f_kline_1hour)): 
        coin_date.iloc[i,0] = datetime.datetime.fromtimestamp(f_kline_1hour[i][0]/1000,timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S') #时间戳 转化为 北京时间
        coin_date.iloc[i,1] = float(f_kline_1hour[i][1])
        coin_date.iloc[i,2] = float(f_kline_1hour[i][2])
        coin_date.iloc[i,3] = float(f_kline_1hour[i][3])
        coin_date.iloc[i,4] = float(f_kline_1hour[i][4])
        coin_date.iloc[i,5] = float(f_kline_1hour[i][5])
    print ("\t 实时K线数据更新 结束 %s \n" %time.ctime())
    close_ratio_present = (coin_date.iloc[-1,4]/coin_date.iloc[-2,4]-1)*100
    hh_ratio_present = (coin_date.iloc[-1,2]/coin_date.iloc[-1,4]-1)*100
    ll_ratio_present = (coin_date.iloc[-1,4]/coin_date.iloc[-1,3]-1)*100
    coin_date1 = coin_date

    coin_date = coin_date.iloc[:-1,:]    
    f = open(root+'\\buy_total_%s.spydata'%coin,'rb')#open('C:/Data_P1/buy_total_%s.spydata'%coin,'rb')
    buy_total = pickle.load(f)
    f.close()   
    #can_sell_market_empty_loss_present = list(np.array(*np.where((buy_total.values[1:,1]<0) & (close_ratio_present>3.5) ))+1)#该平的亏损空单位置
    #can_sell_market_much_loss_present = list(np.array(*np.where((buy_total.values[1:,1]>0) & (close_ratio_present<-3.5) ))+1)#该平的亏损空单位置
    #can_sell_market_loss_present = can_sell_market_empty_loss_present+can_sell_market_much_loss_present
    
    can_sell_market_empty_loss_present1 = list(np.array(*np.where((buy_total.values[1:,1]<0) & (buy_total.values[1:,1]!=-2) & (close_ratio_present>3.5) ))+1)#该平的亏损空单位置 3.5
    can_sell_market_empty_loss_present2 = list(np.array(*np.where((buy_total.values[1:,1]<0) & (buy_total.values[1:,1]==-2) & (close_ratio_present>7.0) ))+1)#该平的亏损空单位置 7.0
    can_sell_market_much_loss_present1 = list(np.array(*np.where((buy_total.values[1:,1]>0) & (buy_total.values[1:,1]!=2) & (close_ratio_present<-3.5) ))+1)#该平的亏损空单位置 -3.5
    can_sell_market_much_loss_present2 = list(np.array(*np.where((buy_total.values[1:,1]>0) & (buy_total.values[1:,1]==2) & (close_ratio_present<-6.0) ))+1)#该平的亏损空单位置 -6.0
    can_sell_market_much_loss_hh1 = list(np.array(*np.where((buy_total.values[1:,1]>0) & (buy_total.values[1:,1]!=2) & (hh_ratio_present>4.0) ))+1)#该平的亏损空单位置
    can_sell_market_much_loss_hh2 = list(np.array(*np.where((buy_total.values[1:,1]==2) & (hh_ratio_present>6.5) ))+1)#该平的亏损空单位置
#    can_sell_market_empty_loss_ll = list(np.array(*np.where((buy_total.values[1:,1]==-7) & (ll_ratio_present>3.5) ))+1)#该平的亏损空单位置

    can_sell_market_loss_present = can_sell_market_empty_loss_present1 + can_sell_market_empty_loss_present2 + can_sell_market_much_loss_present1 + can_sell_market_much_loss_present2 + can_sell_market_much_loss_hh1 + can_sell_market_much_loss_hh2
    
    ib=[]
    if (numtime>50) and (numtime1<5955):
        p1=1
        p2=1
        p3=1
        
    numtime1 = time11.minute*60+time11.second
    if (numtime1>5) and (numtime<10) and (p1==1):
        p1=2
        f = open(root+'\\buy_total_%s.spydata'%coin,'rb')#open('C:/Data_P1/buy_total_%s.spydata'%coin,'rb')
        buy_total = pickle.load(f)
        f.close()
        
        #buy_total.drop(buy_total.index[1:17],inplace=True) 
        #buy_total.index = range(len(buy_total))
        ##buy_total = buy_total.append(buy_total,ignore_index=True) #type(buy_total.iloc[1,4])
        #pk1 = open(root+'\\buy_total_%s.spydata'%coin,'wb')
        #pickle.dump(buy_total,pk1)
        #pk1.close()
        #capital_change_total = pickle.load(open(root+'\\capital_change_total_%s.spydata'%coin,'rb'))
        #type(capital_change_total.iloc[16,2]=35.55
        #pk1 = open(root+'\\capital_change_total_%s.spydata'%coin,'wb')
        #pickle.dump(capital_change_total,pk1)
        #pk1.close()
        
        #buy_total=buy_total.iloc[[0,8]]
        #buy_total.index=range(len(buy_total))
        #现货API
        
        '''开平仓信号计算'''
        print ("\t 开仓信号计算 开始 %s" %time.ctime())
        close2 =coin_date.iloc[:,4] 
        hh2 = coin_date.iloc[:,2] 
        ll2 = coin_date.iloc[:,3] 
        open2 = coin_date.iloc[:,1] 
        ma5 = close2.rolling(5).mean()
        ma5_degree=np.arctan((ma5/(ma5.shift(1))-1)*100)*180/np.pi
        ma10 = close2.rolling(10).mean()
        ma10_degree=np.arctan((ma10/(ma10.shift(1))-1)*100)*180/np.pi
        ma20 = close2.rolling(20).mean()
        ma20_degree=np.arctan((ma20/(ma20.shift(1))-1)*100)*180/np.pi
        ma30 = close2.rolling(30).mean()
        ma30_degree=np.arctan((ma30/(ma30.shift(1))-1)*100)*180/np.pi
        ma60 = close2.rolling(60).mean()
        ma60_degree=np.arctan((ma60/(ma60.shift(1))-1)*100)*180/np.pi
        ma90 = close2.rolling(90).mean()
        ma120 = close2.rolling(120).mean()
        ma120_degree=np.arctan((ma120/(ma120.shift(1))-1)*100)*180/np.pi
        ma250 = close2.rolling(250).mean()
        ma360 = close2.rolling(360).mean()
        ma360_degree=np.arctan((ma360/(ma360.shift(1))-1)*100)*180/np.pi
        where_nan=np.isnan(ma250)
        cmp_logictable_redK_greenK = np.zeros([len(close2),1])
        #前1小时收盘价>开盘价 & 现在收盘价<开盘价 & 前1小时的涨幅<当前小时的跌幅 & 跌幅>-0.7 & 收盘价<ma10 & 开盘价>ma10 
        for i in range(10,len(close2)):
            cmp_logictable_redK_greenK[i,:] = close2[i-1]>open2[i-1] and close2[i]<open2[i] and abs((close2[i-1]/close2[i-2]-1)*100)<abs((close2[i]/close2[i-1]-1)*100) and (close2[i]/close2[i-1]-1)*100<-0.7 and close2[i]<ma10[i] and open2[i]>ma10[i]  

        # 计算 每日收盘涨幅，最大涨跌幅
        close_ratio = (close2-close2.shift(1))/close2.shift(1)*100
        hh_ratio = (hh2-close2.shift(1))/close2.shift(1)*100
        ll_ratio = (ll2-close2.shift(1))/close2.shift(1)*100
        open_ratio = (open2-close2.shift(1))/close2.shift(1)*100
        cmp_logictable_redK = close2>open2
        cmp_logictable_greenK=close2<open2
        cmp_logictable_o_more_ma5 = open2>ma5
        cmp_logictable_o_less_ma5=open2<ma5
        cmp_logictable_c_less_ma5=close2<ma5
        cmp_logictable_c_less1_ma5 = close2<ma5*1.002
        cmp_logictable_c_more_ma5 = close2>ma5
        cmp_logictable_o_more_ma10 = open2>ma10
        cmp_logictable_c_less_ma10 = close2<ma10
        cmp_logictable_l_less_ma10 = ll2<ma10
        cmp_logictable_c_more_ma10 = close2>ma10
        cmp_logictable_o_less_ma20 = open2<ma20
        cmp_logictable_c_more_ma20=close2>ma20
        cmp_logictable_delt_c_more_ma20 = close2/ma20>1.002
        cmp_logictable_c_less_ma20=close2<ma20
        cmp_logictable_c_more_ma30 = close2>ma30
        cmp_logictable_o_less_ma30 = open2<ma30
        cmp_logictable_o_more_ma30 = open2>ma30
        cmp_logictable_c_more_ma60 = close2>ma60
        cmp_logictable_delt_c_less_ma60 = close2<ma60*0.995
        cmp_logictable_delt_c_ma60=close2/ma60>0.95
        cmp_logictable_c_more_ma90 = close2>ma90
        cmp_logictable_c_less_ma60 = close2<ma60
        cmp_logictable_c_more_ma120 = close2>ma120
        cmp_logictable_c_less1_ma120 = close2<ma120*0.99
        cmp_logictable_l_more_ma120 = ll2>ma120
        cmp_logictable_l_less_ma120 = ll2<ma120
        cmp_logictable_l_less1_ma120 = ll2<ma120*1.005
        cmp_logictable_delt_c_ma120 = abs(close2-ma120)/ma120>0.02
        cmp_logictable_delt_c_ma250 = abs(close2-ma250)/ma250>0.02
        cmp_logictable_c_less_ma120 = close2<ma120
        cmp_logictable_o_more_ma120 = open2>ma120
        cmp_logictable_c_less_ma250 = close2<ma250
        cmp_logictable_c_more_ma250 = close2>ma250
        cmp_logictable_c_more_ma360 = close2>ma360
        cmp_logictable_c_less_ma5_ma10 = (close2<ma5) & (close2<ma10)
        cmp_logictable_c_more_ma5_ma10 = (close2>ma5) & (close2>ma10)
        cmp_logictable_o_less_ma5_ma10 = (open2<ma5) & (open2<ma10)
        cmp_logictable_o_more_ma5_ma10 = (open2>ma5) & (open2>ma10)
        cmp_logictable_c_more_ma20_ma30_ma60 = (close2>ma20) & (close2>ma30) & (close2>ma60) 
        cmp_logictable_c_less_ma20_ma30 = (close2<ma20) & (close2<ma30)
        cmp_logictable_o_more_ma20_ma30 = (open2>ma20) & (open2>ma30)
        cmp_logictable_c_more_ma20_ma30 = (close2>ma20) & (close2>ma30) 
        cmp_logictable_c_more_ma20_or_ma30 = (close2>ma20) | (close2>ma30)
        cmp_logictable_c_less_ma20_or_ma30 = (close2<ma20) | (close2<ma30)
        cmp_logictable_c_less_ma5_ma10_ma20 = (close2<ma5) & (close2<ma10)  & (close2<ma20)
        cmp_logictable_c_more_ma5_ma10_ma20_ma30 = (close2>ma5) & (close2>ma10) & (close2>ma20) & (close2>ma30) 
        cmp_logictable_c_more_ma5_ma10_ma20 = (close2>ma5) & (close2>ma10) & (close2>ma20)
        cmp_logictable_c_less_ma5_ma10_ma20_ma30 = (close2<ma5) & (close2<ma10) & (close2<ma20) & (close2<ma30)
        cmp_logictable_cross_ma20_ma30_much=(open2<ma20) &(open2<ma30)&(close2>ma20)&(close2>ma30)
        cmp_logictable_cross_ma5_empty = (close2<ma5) & (hh2>ma5)
        cmp_logictable_cross_ma10_empty = (close2<ma10) & (hh2>ma10)
        cmp_logictable_cross_ma10_empty1 = (close2<ma10) & (open2>ma10)
        cmp_logictable_cross_ma10_much = (close2>ma10) & (open2<ma10)
        cmp_logictable_cross_ma20_empty = (close2<ma20) & (hh2>ma20)
        #cmp_logictable_cross_ma30_empty = (close2<ma30) & (hh2>ma30)
        cmp_logictable_cross_ma30 = (hh2>ma30) & (ll2<ma30)
        cmp_logictable_cross_ma60_empty = (close2<ma60) & (hh2>ma60)
        cmp_logictable_cross_ma20_empty1=(close2<ma20) &(open2>ma20) &(close_ratio<-0.5)
        cmp_logictable_cross_ma30_empty1=(close2<ma30) &(open2>ma30) &(close_ratio<-0.5)
        cmp_logictable_cross_ma60_empty1=(close2<ma60) &(open2>ma60) &(close_ratio<-0.5)
        cmp_logictable_cross_ma90_empty1=(close2<ma90) &(open2>ma90) &(close_ratio<-0.5)
        cmp_logictable_cross_ma60_much = (close2>ma60) & (ll2<ma60)
        cmp_logictable_cross_ma60 = (hh2>ma60) & (ll2<ma60)
        cmp_logictable_cross2_ma60 = (close2>ma60) & (open2<ma60)
        cmp_logictable_cross_ma30_much = (close2>ma30) & (ll2<ma30)
        cmp_logictable_cross_ma90_empty = (close2<ma90) & (hh2>ma90)
        cmp_logictable_cross_ma120_empty=(close2<ma120) &(hh2>ma120)
        cmp_logictable_cross_ma5_ma10_much1 = (close2>ma5) & (close2>ma10) & (ll2<ma5) & (ll2<ma10)
        cmp_logictable_cross_ma120_empty1=(close2<ma120) &(open2>ma120) &(close_ratio<-0.5)
        cmp_logictable_cross_ma250_empty1=(close2<ma250) &(open2>ma250) &(close_ratio<-0.5)
        cmp_logictable_cross_ma20_ma30_empty = (open2>ma20) & (open2>ma30) & (close2<ma20) & (close2<ma30)
        cmp_logictable_ma5_less_ma10 = ma5<ma10
        cmp_logictable_ma5_more_ma20 = ma5>ma20
        cmp_logictable_ma5_less_ma20 = ma5<ma20
        cmp_logictable_ma10_more_ma20 = ma10>ma20
        cmp_logictable_ma10_more_ma30 = ma10>ma30
        cmp_logictable_ma10_less_ma20 = ma10<ma20
        cmp_logictable_ma10_less_ma30 = ma10<ma30
        cmp_logictable_ma60_more_ma120 = ma60>ma120
        cmp_logictable_ma60_less_ma120 = ma60<ma120
        cmp_logictable_ma20_less_ma30 = ma20<ma30
        cmp_logictable_ma20_more_ma30 = ma20>ma30
        cmp_logictable_ma30_more_ma60 = ma30>ma60
        
        cmp_logictable_c_less_ma30 = close2<ma30
        cmp_logictable_ma5_more_ma10 = ma5>ma10
        cmp_logictable_ma20_more_ma60 = ma20>ma60
        cmp_logictable_ma20_less_ma60 = ma20<ma60
        cmp_logictable_ma30_less_ma60 = ma30<ma60
        cmp_logictable_c_more_o = close2>open2
        cmp_logictable_c_less_o = close2<open2
        cmp_logictable_much_ma5_ma10_ma20 = (ma5>ma10) & (ma10>ma20)
        cmp_logictable_much_ma10_ma20_ma30 = (ma10>ma20) & (ma20>ma30)
        cmp_logictable_much_ma20_ma30_ma60 = (ma20>ma30) & (ma30>ma60)
        cmp_logictable_empty_ma10_ma20_ma30 = (ma10<ma20) & (ma20<ma30)
        cmp_logictable_empty_ma5_ma10_ma20 = (ma5<ma10) & (ma10<ma20)
        cmp_logictable_empty_ma5_ma10_ma20_ma30 = (ma5<ma10) & (ma10<ma20) & (ma20<ma30)
        cmp_logictable_cross_ma5_ma10_empty = (open2>ma5) & (open2>ma10) & (close2<ma5) & (close2<ma10)
        cmp_logictable_cross_ma5_ma10_ma20_much = (ll2<ma5) & (ll2<ma10) & (ll2<ma20) & (close2>ma5) & (close2>ma10) & (close2>ma20)
        cmp_logictable_delt_ma5_ma10 = (ma5/ma10>0.985) & (ma5/ma10<1.015)
        cmp_logictable_delt_ma10_ma20 = (ma10/ma20>0.978) & (ma10/ma20<1.022)
        cmp_logictable_delt_ma20_ma30 = (ma20/ma30>0.982) & (ma20/ma30<1.018)
        cmp_logictable_ma10_less_ma20_ma30 = (ma10<ma20) & (ma10<ma30)
        cmp_logictable_ma5_ma10_less_ma20 = (ma5<ma20) & (ma10<ma20)
        cmp_logictable_ma5_ma10_ma20_more_ma60 = (ma5>ma60) & (ma10>ma60) & (ma20>ma60)
        cmp_logictable_ma5_ma10_ma20_ma30_more_ma60 = (ma5>ma60) & (ma10>ma60) & (ma20>ma60) & (ma30>ma60)
        cmp_logictable_ma5_ma10_golden_cross = (ma5.shift(1)<ma10.shift(1)) & (ma5>=ma10)
        cmp_logictable_ma5_ma10_death_cross = (ma5.shift(1)>ma10.shift(1)) & (ma5<ma10)
        cmp_logictable_ma20_ma30_golden_cross = (ma20.shift(1)<ma30.shift(1)) & (ma20>ma30)
        cmp_logictable_ma20_ma30_death_cross = (ma20.shift(1)>ma30.shift(1)) & (ma20<ma30)
        cmp_logictable_ma20_ma60_golden_cross = (ma20.shift(1)<ma60.shift(1)) & (ma20>ma60)
        cmp_logictable_ma20_ma60_death_cross = (ma20.shift(1)>ma60.shift(1)) & (ma20<ma60)
        cmp_logictable_ma10_ma20_golden_cross = (ma10.shift(1)<ma20.shift(1)) & (ma10>ma20)
        cmp_logictable_ma10_ma20_death_cross = (ma10.shift(1)>ma20.shift(1)) & (ma10<ma20)
        cmp_logictable_cross1_ma120 = (open2>ma120) & (close2<ma120)
        cmp_logictable_cross1_ma250 = (open2>ma250) &(close2<ma250)
        cmp_logictable_cross1_ma60 = (open2>ma60) &(close2<ma60)
        cmp_logictable_shock = hh2/close2
        cmp_logictable_c_less1_ma10 = close2<ma10*0.99
        cmp_logictable_c_less1_ma20 = close2<ma20*0.992
        cmp_logictable_c_less2_ma10 = close2<ma10*0.994
        cmp_logictable_h_more_ma10_ma20_ma30 = (hh2>ma10) & (hh2>ma20) & (hh2>ma30)
        cmp_logictable_c_less_ma5_ma10_ma20_ma30_ma60 = (close2<ma5) & (close2<ma10) & (close2<ma20) & (close2<ma30) & (close2<ma60)
        cmp_logictable_c_more_ma5_ma10_ma20_ma30_ma60 = (close2>ma5) & (close2>ma10) & (close2>ma20) & (close2>ma30) & (close2>ma60)
        cmp_logictable_c_more_ma5_ma10_ma20_ma30_ma60_ma120 = (close2>ma5) & (close2>ma10) & (close2>ma20) & (close2>ma30) & (close2>ma60) & (close2>ma120)
        cmp_logictable_c_more_ma5_ma20_ma30_ma60_ma120 = (close2>ma5) & (close2>ma20) & (close2>ma30) & (close2>ma60) & (close2>ma120)
        cmp_logictable_c_more1_ma10 = close2>ma10*1.01
        cmp_logictable_ma5_ma10_ma20_ma30_less_ma60 = (ma5<ma60) & (ma10<ma60) & (ma20<ma60) & (ma30<ma60)
        cmp_logictable_c_more_ma10_ma20_ma30 = (close2>ma10) & (close2>ma20) & (close2>ma30) 
        cmp_logictable_o_more_ma5_ma10_ma20 = (open2>ma5) & (open2>ma10) & (open2>ma20)
        cmp_logictable_o_less_ma5_or_ma10_or_ma20 = (open2<ma5) | (open2<ma10) | (open2<ma20)
        cmp_logictable_o_less_ma20_or_ma30 = (open2<ma20) | (open2<ma30)
        cmp_logictable_c_more_ma5_or_ma10_or_ma20 = (close2>ma5*1.004) | (close2>ma10*1.004) | (close2>ma20*1.006)
        cmp_logictable_c_more1_ma20_or_ma30 = (close2>ma20*1.004) | (close2>ma30*1.004)
        cmp_logictable_h_more1_ma120 = hh2>ma120*0.99
        cmp_logictable_c_more1_ma120 = close2>ma120*1.01
        buy_much_signal1 = np.zeros([len(close2),1])
        buy_much_signal2 = np.zeros([len(close2),1])
        buy_much_signal3 = np.zeros([len(close2),1])
        buy_much_signal4 = np.zeros([len(close2),1])
        buy_much_signal5 = np.zeros([len(close2),1])
        buy_much_signal6 = np.zeros([len(close2),1])
        buy_much_signal7 = np.zeros([len(close2),1])
        buy_much_signal8 = np.zeros([len(close2),1])
        buy_much_signal9 = np.zeros([len(close2),1])
        buy_much_signal10 = np.zeros([len(close2),1])
        buy_empty_signal1 = np.zeros([len(close2),1])
        buy_empty_signal2 = np.zeros([len(close2),1])
        buy_empty_signal3 = np.zeros([len(close2),1])
        buy_empty_signal4 = np.zeros([len(close2),1])
        buy_empty_signal5 = np.zeros([len(close2),1])
        buy_empty_signal6 = np.zeros([len(close2),1])
        buy_empty_signal7 = np.zeros([len(close2),1])
        buy_empty_signal8 = np.zeros([len(close2),1])
        buy_empty_signal9 = np.zeros([len(close2),1])
        sell_much_signal1 = np.zeros([len(close2),1])
        sell_much_signal2 = np.zeros([len(close2),1])
        sell_much_signal3 = np.zeros([len(close2),1])
        sell_much_signal4 = np.zeros([len(close2),1])
        sell_much_signal5 = np.zeros([len(close2),1])
        sell_much_signal6 = np.zeros([len(close2),1])
        sell_much_signal7 = np.zeros([len(close2),1])
        sell_much_signal8 = np.zeros([len(close2),1])
        sell_much_signal9 = np.zeros([len(close2),1])
        sell_much_signal10 = np.zeros([len(close2),1])
        sell_much_signal11 = np.zeros([len(close2),1])
        sell_much_signal12 = np.zeros([len(close2),1])
        sell_much_signal13 = np.zeros([len(close2),1])
        sell_much_signal14 = np.zeros([len(close2),1])
        sell_much_signal15 = np.zeros([len(close2),1])
        sell_much_signal16 = np.zeros([len(close2),1])
        sell_much_signal17 = np.zeros([len(close2),1])
        sell_much_signal18 = np.zeros([len(close2),1])
        
        sell_empty_signal1 = np.zeros([len(close2),1])
        sell_empty_signal2 = np.zeros([len(close2),1])
        
        sell_empty_signal4 = np.zeros([len(close2),1])
        sell_empty_signal5 = np.zeros([len(close2),1])
        sell_empty_signal6 = np.zeros([len(close2),1])
        
        max_back = np.zeros([len(close2),1])
        max_drop = np.zeros([len(close2),1])
        max_back1 = np.zeros([len(close2),1])
        max_back_empty = np.zeros([len(close2),1])
        max_back_empty1 = np.zeros([len(close2),1])
        for i in range(450,len(close2)):
            
            buy_much_signal1[i,:] = ( close2[i]>max(close2[i-96:i-23])*1.003 and close2[i]>max(close2[i-23:i])*1.0015 and cmp_logictable_redK[i]==1 and close_ratio[i]>0.25 and sum(close_ratio[i-36:i+1]>1)>=1 and max(close2[i-24:i+1])/min(close2[i-24:i+1])>=1.03 and cmp_logictable_c_more_ma5_ma10_ma20_ma30_ma60_ma120[i]==1 and ( close2[i]>max(ma120[i-96:i+1]) or (close2[i]>max(close2[i-120:i])*1.004 and close2[i]>max(close2[i-120:i-23])*1.01) )   )
            buy_much_signal2[i,:] = ( ( sum(cmp_logictable_c_more_ma120[i-3:i+1])==4 and sum(cmp_logictable_l_more_ma120[i-2:i+1])==3 and sum(cmp_logictable_l_less_ma120[i-5:i-2])>=1 and sum(cmp_logictable_c_more_ma20[i-9:i+1])>=7 and sum(cmp_logictable_c_more_ma30[i-7:i+1])>=5 and sum(cmp_logictable_c_more_ma60[i-10:i+1])>=8 and max(close2[i-23:i+1])/min(close2[i-23:i+1])>1.015 and max(close_ratio[i-23:i+1])>1 and max(close2[i-23:i+1])>=max(close2[i-68:i+1]) ) or ( sum(cmp_logictable_c_more_ma120[i-4:i+1])==5 and sum(cmp_logictable_c_more_ma120[i-7:i+1])>=5 and sum(cmp_logictable_c_more_ma60[i-6:i+1])==7 and sum(cmp_logictable_c_more_ma60[i-8:i+1])>=7 and sum(cmp_logictable_c_more_ma30[i-8:i+1])>=7 and sum(cmp_logictable_c_more_ma30[i-9:i+1])>=7  and sum(cmp_logictable_c_more_ma20[i-11:i+1])>=7 and sum(cmp_logictable_c_more_ma20[i-13:i+1])>=9 and sum(cmp_logictable_l_less1_ma120[i-23:i-3])>=1 and  max(close2[i-1:i+1])>=max(close2[i-47:i+1]) and ( max(close2[i-9:i-1])<max(close2[i-47:i-19])*1.01 or ( max(close2[i-23:i-1])<=max(close2[i-47:i-23])*1.1 and  max(close2[i-14:i-5])<max(close2[i-47:i-19])*1.01 and max(close2[i-11:i-5])<=max(close2[i-23:i-11])*1.01  ) ) ) )
            buy_much_signal3[i,:] = ( ( cmp_logictable_o_less_ma5_or_ma10_or_ma20[i]==1 and cmp_logictable_c_more_ma5_or_ma10_or_ma20[i]==1 and sum(cmp_logictable_much_ma20_ma30_ma60[i-4:i+1])>=4 and sum(cmp_logictable_c_more_ma30[i-17:i+1])>=15 and sum(ma30_degree[i-13:i+1]>0)>=12 and sum(ma30_degree[i-13:i+1]>5)>=10 and sum(cmp_logictable_c_less_ma10[i-4:i+1])>=2 and cmp_logictable_c_more_ma5_ma20_ma30_ma60_ma120[i]==1 and sum(cmp_logictable_ma5_ma10_death_cross[i-11:i+1])==1 and ( close_ratio[i]>1 or (sum(close_ratio[i-2:i+1]>0.2)>=2 and close_ratio[i]>0.8) or (sum(close_ratio[i-3:i+1]>0.2)>=3 and close_ratio[i]>0.6) ) and close2[i]==max(close2[i-2:i+1]) and close2[i]<max(close2[i-19:i-4])*1.02 and max(close2[i-19:i-4])>max(close2[i-108:i-19])*1.01 and open2[i]<max(close2[i-19:i-5])*0.99 and ( (min(close_ratio[i-6:i+1])<=-4 and max(close_ratio[i-1:i+1])>2) or (min(close_ratio[i-6:i+1])>-4 and close2[i]>(max(hh2[i-19:i-4])*0.45 + min(ll2[i-6:i+1])*0.55 )  ) ) and close2[i]>max(close2[i-108:i-19])*1.002 and (close2[i]>max(ma120[i-72:i+1]) or close2[i]>ma360[i])   )    or    ( sum(cmp_logictable_c_more_ma60[i-23:i+1])>=23 and sum(ma60_degree[i-23:i+1]>0)>=22 and sum(ma60_degree[i-19:i+1]>5)>=18 and sum(cmp_logictable_ma5_ma10_ma20_ma30_more_ma60[i-23:i+1])>=23 and sum(cmp_logictable_c_more_ma30[i-23:i+1])>=12 and sum(ma30_degree[i-23:i+1]>5)>=18 and sum(cmp_logictable_ma20_more_ma30[i-23:i+1])>=12 and cmp_logictable_o_less_ma20_or_ma30[i]==1 and cmp_logictable_c_more1_ma20_or_ma30[i]==1 and cmp_logictable_c_more_ma5_ma10_ma20_ma30_ma60[i]==1 and ( close_ratio[i]>1 or (sum(close_ratio[i-2:i+1]>0.2)>=2 and close_ratio[i]>0.8) or (sum(close_ratio[i-3:i+1]>0.15)>=3 and close_ratio[i]>0.6) ) and close2[i]==max(close2[i-4:i+1]) and close2[i]<max(close2[i-35:i-4])*1.035 and max(close2[i-35:i-4])>max(close2[i-120:i-35])*1.02 and open2[i]<max(close2[i-35:i-5])*0.99 and cmp_logictable_c_more_ma5_ma10_ma20_ma30_ma60_ma120[i]==1 and close2[i]>max(close2[i-120:i-35])*1.01 and close2[i]>(max(hh2[i-35:i-14])*0.45 + min(ll2[i-14:i+1])*0.55 ) and sum(cmp_logictable_ma20_ma30_death_cross[i-14:i+1])==1    )    or   ( close2[i]<=max(close2[i-96:i])*1.003 and max(close2[i-29:i+1])/min(close2[i-29:i+1])>1.035 and max(close2[i-16:i+1])/min(close2[i-16:i+1])>1.025 and close2[i]==max(close2[i-23:i+1]) and close2[i]>max(close2[i-16:i-1])*1.004 and sum(cmp_logictable_c_more_ma10[i-9:i+1])>=6 and sum(cmp_logictable_c_more_ma20[i-9:i+1])>=6 and cmp_logictable_c_more_ma5_ma10_ma20_ma30[i]==1 and sum(ma120_degree[i-120:i+1]>-1.5)>=96 and sum(ma10_degree[i-14:i+1]>5)>=6 and (cmp_logictable_c_more_ma60[i]==1 or cmp_logictable_c_more_ma120[i]==1 or cmp_logictable_c_more_ma360[i]==1) and sum(cmp_logictable_ma10_more_ma20[i-9:i+1])>=8 and cmp_logictable_redK[i]==1 and sum(close_ratio[i-35:i+1]>1)>=1 and close_ratio[i]>0.4  ) )
            
            buy_much_signal4[i,:] = sum(cmp_logictable_c_more_ma120[i-24:i-4])>0 and cmp_logictable_c_more_ma120[i]==1 and cmp_logictable_delt_ma10_ma20[i]==1 and sum(cmp_logictable_delt_ma20_ma30[i-9:i+1])==10 and sum(cmp_logictable_ma10_ma20_golden_cross[i-25:i+1])>0 and cmp_logictable_c_more_ma10[i]==1  and cmp_logictable_c_more_ma20[i]==1 and (cmp_logictable_c_less_ma10[i-1]==1 or cmp_logictable_cross_ma10_much[i]==1)
            buy_much_signal5[i,:] = ( close2[i]>max(hh2[i-96:i]) and max(close2[i-30:i])<max(hh2[i-96:i-30]) and cmp_logictable_c_more_ma5_ma10_ma20_ma30[i]==1 ) or ( (close2[i]>max(hh2[i-72:i-1])*1.014 or close2[i]>max(close2[i-72:i-1])*1.025 ) and max(close2[i-29:i-1])<max(hh2[i-72:i-29]) and cmp_logictable_c_more_ma5_ma10_ma20_ma30[i]==1 and close_ratio[i]<8 )
            buy_much_signal6[i,:] = close2[i]>max(close2[i-9:i]) and sum(cmp_logictable_ma5_more_ma10[i-9:i+1])>=7 and sum(cmp_logictable_ma5_more_ma20[i-9:i+1])>=8 and sum(cmp_logictable_ma10_more_ma20[i-9:i+1])>=9 and sum(cmp_logictable_much_ma5_ma10_ma20[i-9:i+1])>=7 and sum(cmp_logictable_c_more_ma10[i-9:i+1])>=7 and sum(cmp_logictable_c_more_ma10[i-6:i+1])>=5 and max(close_ratio[i-3:i])<1 and min(close_ratio[i-3:i])>-1 and close_ratio[i]>max(abs(close_ratio[i-3:i])) and sum(ma10_degree[i-9:i+1]<35)>=7 and cmp_logictable_c_more_ma5_ma10_ma20[i]==1 and cmp_logictable_redK[i]==1
            
            buy_much_signal7[i,:] =  sum(cmp_logictable_c_more_ma30[i-5:i+1])>=3  and  sum(cmp_logictable_c_more_ma20[i-14:i+1])>=12  and  sum(cmp_logictable_c_more_ma20[i-5:i+1])==6  and  sum(cmp_logictable_ma5_more_ma20[i-8:i+1])==9  and  sum(cmp_logictable_c_more_ma5[i-14:i-4])>=5  and  sum(cmp_logictable_c_more_ma5[i-7:i+1])>=3  and  ( cmp_logictable_c_less_ma5[i-1]==1  or  ( min(close_ratio[i-2:i])>-1.4  and  max(close_ratio[i-2:i])<1.4  and  close_ratio[i]>0.7  and  close_ratio[i]>max(abs(close_ratio[i-2:i])) ) )  and  cmp_logictable_c_more_ma5[i]==1  and  sum(ma5_degree[i-14:i+1]>2)>=8  and  sum(ma5_degree[i-1:i+1]>-15)==2  and  min(ma5_degree[i-14:i+1])>-28  and  max(hh2[i-9:i])/close2[i]<1.02  and  max(ma5[i-6:i+1])>max(ma5[i-14:i-6]) and cmp_logictable_delt_c_ma120[i]==1 and cmp_logictable_delt_c_ma250[i]==1
            buy_much_signal8[i,:] = (sum(cmp_logictable_c_less_ma60[i-6:i+1])==7 or sum(cmp_logictable_cross2_ma60[i-3:i+1])>0)  and sum(cmp_logictable_delt_c_ma60[i-39:i+1])>39 and sum(cmp_logictable_redK[i-3:i+1])==3 and cmp_logictable_redK[i]==1 and sum( ma60_degree[i-14:i+1]<-1)<2
            buy_much_signal9[i,:] = ((cmp_logictable_c_more_ma60[i-19:i+1].sum()>=15)|(cmp_logictable_c_more_ma90[i-19:i+1].sum()>=15)) &( ( ((cmp_logictable_cross_ma60_empty1[i-1]==1)&(close_ratio[i]>0.5)) | ((cmp_logictable_cross_ma60_empty1[i-2]==1)&(close_ratio[i-1]<0.5)&(close_ratio[i]>0.5))|((cmp_logictable_cross_ma60_empty1[i-3]==1)&(close_ratio[i-2]<0.5)&(close_ratio[i-1]<0.5)&(close_ratio[i]>0.5))) | ( ((cmp_logictable_cross_ma90_empty1[i-1]==1)&(close_ratio[i]>0.5))| ((cmp_logictable_cross_ma90_empty1[i-2]==1)&(close_ratio[i-1]<0.5)&(close_ratio[i]>0.5))|((cmp_logictable_cross_ma90_empty1[i-3]==1)&(close_ratio[i-2]<0.5)&(close_ratio[i-1]<0.5)&(close_ratio[i]>0.5))))
            buy_much_signal10[i,:] = (((close_ratio[i-14:i+1]<-1).sum()==1) &((close_ratio[i-4:i+1]<-1).sum()==0)&(close_ratio[i]>1)&((close_ratio[i-14:i+1]>1).sum()==1)) or ( (cmp_logictable_redK[i-2:i+1].sum()==3)&(cmp_logictable_redK[i-3:i+1].sum()==3)&(cmp_logictable_redK[i-4:i+1].sum()>=4)&((close_ratio[i-7:i+1]<-1).sum()==1)&(close_ratio[i]>0.2)&(cmp_logictable_c_less_ma30[i-4:i+1].sum()==5))
            
            
            buy_empty_signal1[i,:] = ( ( max(close2[i-72:i+1])<max(close2[i-192:i-72]) and max(close2[i-24:i+1])<max(close2[i-72:i-24]) and \
                             ( ( sum(cmp_logictable_h_more_ma10_ma20_ma30[i-6:i+1])>=1 and cmp_logictable_c_less_ma5_ma10_ma20_ma30_ma60[i]==1 and close2[i]==min(close2[i-72:i+1]) and close2[i]<min(close2[i-72:i])*0.99 and close_ratio[i]<-1.5 ) or \
                             ( sum(cmp_logictable_h_more_ma10_ma20_ma30[i-7:i])>=1 and cmp_logictable_c_less_ma5_ma10_ma20_ma30_ma60[i-1]==1 and close2[i-1]==min(close2[i-73:i]) and close2[i-1]<min(close2[i-73:i-1])*0.99 and close_ratio[i-1]<-1.5 and cmp_logictable_c_less_ma5_ma10_ma20_ma30_ma60[i]==1 and close2[i]==min(close2[i-73:i+1]) and cmp_logictable_greenK[i]==1 ) or \
                             ( sum(cmp_logictable_h_more_ma10_ma20_ma30[i-8:i-1])>=1 and cmp_logictable_c_less_ma5_ma10_ma20_ma30_ma60[i-2]==1 and close2[i-2]==min(close2[i-74:i-1]) and close2[i-2]<min(close2[i-74:i-2])*0.99 and close_ratio[i-2]<-1.5 and cmp_logictable_c_less_ma5_ma10_ma20_ma30_ma60[i]==1 and close2[i]==min(close2[i-74:i+1]) and cmp_logictable_greenK[i]==1 ) or \
                             ( sum(cmp_logictable_h_more_ma10_ma20_ma30[i-9:i-2])>=1 and cmp_logictable_c_less_ma5_ma10_ma20_ma30_ma60[i-3]==1 and close2[i-3]==min(close2[i-75:i-2]) and close2[i-3]<min(close2[i-75:i-3])*0.99 and close_ratio[i-3]<-1.5 and cmp_logictable_c_less_ma5_ma10_ma20_ma30_ma60[i]==1 and close2[i]==min(close2[i-75:i+1]) and cmp_logictable_greenK[i]==1 ) or \
                             ( sum(cmp_logictable_c_less_ma10[i-9:i+1])>=7 and sum(cmp_logictable_c_less_ma20[i-9:i+1])>=7 and sum(cmp_logictable_c_less_ma30[i-9:i+1])>=7 and cmp_logictable_c_less_ma60[i]==1 and cmp_logictable_c_less_ma5_ma10_ma20_ma30[i]==1 and close2[i]==min(close2[i-47:i+1]) and cmp_logictable_greenK[i]==1 ) ) ) or \
                             ( max(close2[i-48:i+1])/min(close2[i-48:i+1])>1.035 and close2[i]==min(close2[i-96:i+1]) and close2[i]<min(close2[i-96:i])*0.997 and cmp_logictable_greenK[i]==1 and close_ratio[i]<-0.5 and cmp_logictable_c_less_ma60[i]==1 and cmp_logictable_c_less_ma5_ma10_ma20_ma30[i]==1 and ( ( close_ratio[i]<-1.5 and close2[i]<min(close2[i-144:i])*0.996 and sum(cmp_logictable_c_less_ma120[i-96:i+1])>=10 and cmp_logictable_c_less_ma120[i]==1 and close2[i]<ma120[i]*0.98 ) or sum(ma120_degree[i-120:i+1]<2)>=96 or sum(ma360_degree[i-120:i+1]<1)>=96 ) )  )
            buy_empty_signal2[i,:] = ( sum(cmp_logictable_h_more1_ma120[i-19:i-3])>=1 and sum(cmp_logictable_c_less_ma120[i-3:i+1])==4 and sum(cmp_logictable_c_less_ma60[i-9:i+1])>=7 and sum(cmp_logictable_c_less_ma30[i-9:i+1])>=7 and sum(cmp_logictable_c_less_ma20[i-9:i+1])>=7 and sum(cmp_logictable_c_less_ma10[i-9:i+1])>=6 and cmp_logictable_c_less_ma5_ma10_ma20_ma30_ma60[i]==1 and cmp_logictable_greenK[i]==1 and close2[i]==min(close2[i-44:i+1]) and max(hh2[i-72:i+1])/min(ll2[i-72:i+1])>1.03 )

            
            
            buy_empty_signal3[i,:] = ( sum(cmp_logictable_ma20_less_ma30[i-9:i+1])>=3 and sum(cmp_logictable_c_less_ma5_ma10[i-15:i-5])>2 and sum(cmp_logictable_ma5_ma10_golden_cross[i-5:i+1])>0 and  cmp_logictable_o_more_ma5_ma10[i]==1 and cmp_logictable_greenK[i]==1 and cmp_logictable_c_less_ma20[i]==1 ) or ( sum(cmp_logictable_ma20_less_ma30[i-9:i+1])>=3 and sum(cmp_logictable_c_less_ma30[i-9:i+1])==10 and sum(cmp_logictable_c_less_ma20[i-9:i+1])>=9 and sum(cmp_logictable_c_less_ma10[i-9:i+1])>=7 and sum(cmp_logictable_empty_ma5_ma10_ma20[i-10:i+1])>=6 and close2[i]==min(close2[i-9:i+1]) and close_ratio[i]>-6 and abs(close_ratio[i])>max(abs(close_ratio[i-2:i])) and cmp_logictable_greenK[i]==1 and cmp_logictable_c_less_ma5_ma10_ma20[i]==1 )
            buy_empty_signal4[i,:] = sum(cmp_logictable_c_less_ma20[i-13:i+1])>=4 and sum(cmp_logictable_ma20_more_ma30[i-1:i+1])==2 and cmp_logictable_greenK[i]==1 and cmp_logictable_c_less_ma20_ma30[i]==1 and (sum(cmp_logictable_o_more_ma30[i-1:i+1])>0 or cmp_logictable_c_more_ma30[i-1]==1)  and sum(cmp_logictable_ma20_ma30_golden_cross[i-20:i+1])>0 and close_ratio[i]<=-0.3 and sum(cmp_logictable_c_more_ma30[i-72:i+1])>=23 and sum(cmp_logictable_c_more_ma30[i-48:i+1])>=18 and max(close2[i-72:i+1])/min(close2[i-72:i+1])>=1.045 and max(close2[i-48:i+1])/min(close2[i-48:i+1])<=1.2
            buy_empty_signal5[i,:] = close2[i]<min(close2[i-23:i]) and min(close2[i-4:i])>min(close2[i-23:i-4]) and cmp_logictable_greenK[i]==1 and max(close2[i-23:i+1])<max(close2[i-57:i-23]) and sum(cmp_logictable_c_more_ma20_ma30[i-30:i+1])>0 and close_ratio[i]<-0.6 and sum(close_ratio[i-24:i+1]<-0.6)>=2 and max(close2[i-72:i+1])/min(close2[i-72:i+1])>1.03 and ( close2[i]==min(close2[i-96:i+1]) or max(close2[i-23:i+1])<max(close2[i-72:i-23])*0.985 ) 
            buy_empty_signal6[i,:] = close2[i]<min(close2[i-90:i]) and min(close2[i-30:i])>min(close2[i-90:i-30]) and cmp_logictable_c_less_ma5_ma10_ma20_ma30[i]==1
            #buy_empty_signal7[i,:] =  (sum(cmp_logictable_greenK[i-1:i+1])==2 and sum(cmp_logictable_greenK[i-2:i+1])==2   and  min(close2[i-49:i-9])>min(close2[i-9:i+1])*1.01 and close_ratio[i]>-4 and sum(close_ratio[i-9:i+1]>5)==0 and max(close2[i-90:i+1])/close2[i]<1.2 and close2[i]<ma20[i]) or (sum(cmp_logictable_greenK[i-2:i+1])==3 and sum(cmp_logictable_greenK[i-3:i+1])==3   and  min(close2[i-49:i+1])==min(close2[i-2:i+1]) and close_ratio[i]>-4 and sum(close_ratio[i-9:i+1]>5)==0 and max(close2[i-90:i+1])/close2[i]<1.2 and close2[i]<ma20[i]) or ( min(close2[i-49:i+1])==min(close2[i-1:i+1]) and  min(close2[i-3:i+1])*1.01<min(close2[i-49:i-3]) and close_ratio[i]<-4 and max(close2[i-90:i+1])/close2[i]<1.15) or (sum(cmp_logictable_greenK[i-1:i+1])==2 and sum(cmp_logictable_greenK[i-2:i+1])==2   and  min(close2[i-49:i-1])>min(close2[i-1:i+1])*1.01 and max(close2[i-90:i+1])/close2[i]>1.2 and close2[i]<ma20[i]) and cmp_logictable_delt_c_ma120[i]==1 and cmp_logictable_delt_c_ma250[i]==1
            buy_empty_signal7[i,:] =  (sum(cmp_logictable_greenK[i-1:i+1])==2 and sum(cmp_logictable_greenK[i-2:i+1])==2   and  min(close2[i-49:i-9])>min(close2[i-9:i+1])*1.01 and close_ratio[i]>-4 and sum(close_ratio[i-9:i+1]>5)==0 and max(close2[i-90:i+1])/close2[i]<1.2 and close2[i]<ma20[i]) or (sum(cmp_logictable_greenK[i-2:i+1])==3 and sum(cmp_logictable_greenK[i-3:i+1])==3   and  min(close2[i-49:i+1])==min(close2[i-2:i+1]) and close_ratio[i]>-4 and sum(close_ratio[i-9:i+1]>5)==0 and max(close2[i-90:i+1])/close2[i]<1.2 and close2[i]<ma20[i]) or ( min(close2[i-49:i+1])==min(close2[i-1:i+1]) and close_ratio[i]<-4 and sum(close_ratio[i-1:i+1])>-13 and max(close2[i-90:i+1])/close2[i]<1.15) or (sum(cmp_logictable_greenK[i-1:i+1])==2 and sum(cmp_logictable_greenK[i-2:i+1])==2   and  min(close2[i-49:i-1])>min(close2[i-1:i+1])*1.01 and max(close2[i-90:i+1])/close2[i]>1.2 and close2[i]<ma20[i]) #eos-7

            buy_empty_signal8[i,:] = cmp_logictable_ma10_less_ma20[i]==1 and sum(cmp_logictable_ma10_ma20_death_cross[i-11:i+1])>0 and ((cmp_logictable_greenK[i]==1 and cmp_logictable_greenK[i-2]==1 and cmp_logictable_redK[i-1]==1) or (cmp_logictable_greenK[i]==1 and cmp_logictable_greenK[i-1]==1 and cmp_logictable_redK[i-2]==1)) and sum(cmp_logictable_c_less_ma20[i-6:i+1])>4 and cmp_logictable_c_less_ma20[i]==1 and close_ratio[i-1]<2 and max(close2[i-19:i+1])/close2[i]>1.02 and (close2[i]/ma120[i]>1.02  or  close2[i]/ma120[i]<0.98) and cmp_logictable_delt_c_ma120[i]==1 and cmp_logictable_delt_c_ma250[i]==1 and sum(close_ratio[i-19:i+1]<-1.5)>0
            buy_empty_signal9[i,:] = ma20[i]<ma30[i] and ma30[i]<ma60[i] and ma60[i]<ma120[i] and (float(ma20_degree[i])<0) and (float(ma30_degree[i])<0) and (float(ma60_degree[i])<0) and (float(ma120_degree[i])<0) and close_ratio[i]<-2 and sum(cmp_logictable_c_more_ma60[i-24:i+1])>=1 and sum(close_ratio[i-14:i+1]>3)==0 and sum(cmp_logictable_c_less_ma20[i-9:i+1])>=10
            
            
            sell_much_signal1[i,:] = cmp_logictable_cross_ma60_empty[i]==1
            sell_much_signal2[i,:] = cmp_logictable_cross_ma60_empty[i]==1
            sell_much_signal3[i,:] = sum(cmp_logictable_greenK[i-3:i+1])==4
            sell_much_signal4[i,:] = cmp_logictable_shock[i]>1.03
            sell_much_signal5[i,:] = abs(close_ratio[i])/abs(close_ratio[i-1])>0.85 and cmp_logictable_greenK[i]==1 and close_ratio[i]<-1.9 
            sell_much_signal6[i,:] = sum(cmp_logictable_c_less_ma5[i-2:i+1])>=2 and sum(cmp_logictable_c_less_ma10[i-2:i+1])>=2 and sum(close_ratio[i-2:i+1]<-0.4)>=2 and close_ratio[i]<-0.4 and cmp_logictable_greenK[i]==1 
            sell_much_signal7[i,:] = close2[i-1]==max(close2[i-96:i]) and close_ratio[i-1]<0.4 and cmp_logictable_redK[i-1]==1 and cmp_logictable_greenK[i]==1 and close_ratio[i]<-1 and abs(close_ratio[i]/close_ratio[i-1])>4.5 
            sell_much_signal8[i,:] = sum(cmp_logictable_redK_greenK[i-4:i+1])>=2 and cmp_logictable_redK_greenK[i]==1 and abs(close_ratio[i])/abs(close_ratio[i-1])>4 
            sell_much_signal9[i,:] = cmp_logictable_c_less_ma5_ma10_ma20[i]==1 and cmp_logictable_o_more_ma5_ma10_ma20[i]==1 and close_ratio[i]<-1 and cmp_logictable_greenK[i]==1 
            sell_much_signal10[i,:] = (close2[i]/max(hh2[i-2:i+1])-1)*100<-3.7 
            sell_much_signal11[i,:] = cmp_logictable_o_more_ma30[i]==1 and cmp_logictable_c_less_ma30[i]==1 and close_ratio[i]<0 and cmp_logictable_greenK[i]==1 
            sell_much_signal12[i,:] = cmp_logictable_ma5_ma10_death_cross[i]==1 and cmp_logictable_c_less2_ma10[i]==1
            sell_much_signal13[i,:] = ma5_degree[i]<-16 and sum(close_ratio[i-2:i+1]<-1)>=1 
            
            sell_much_signal14[i,:] = 1==1 and ( sum(cmp_logictable_c_less_ma5[i-1:i+1])==2 and sum(close_ratio[i-1:i+1]<-1.5 )>=1 )
            sell_much_signal15[i,:] = 1==1 and ( abs(close_ratio[i])/abs(close_ratio[i-1])>5 and close_ratio[i]<-1.1 )
            sell_much_signal16[i,:] = 1==1 and ( cmp_logictable_cross_ma5_ma10_empty[i]==1 and close_ratio[i]<-1 )
            sell_much_signal17[i,:] = 1==1 and (close2[i]/max(close2[i-23:i])-1)*100<-10
            sell_much_signal18[i,:] = 1==1 and sum(cmp_logictable_c_less_ma20[i-29:i+1])>=26 and sum(cmp_logictable_c_less_ma30[i-23:i+1])>=20
            
            sell_empty_signal1[i,:] = cmp_logictable_cross_ma60_much[i]==1
            sell_empty_signal2[i,:] = cmp_logictable_cross_ma60_much[i]==1
            
            sell_empty_signal4[i,:] = 1==1 and sum(cmp_logictable_redK[i-4:i+1])==5
            sell_empty_signal5[i,:] = 1==1 and (close2[i]/min(ll2[i-20:i+1])-1)*100>9
            sell_empty_signal6[i,:] = 1==1 and close2[i]>=(max(hh2[i-72:i])+min(ll2[i-72:i+1])*2)/3 and cmp_logictable_c_more_ma20[i]==1 and max(hh2[i-72:i])/min(ll2[i-72:i])>1.06 

            max_back[i,:] = (close2[i]/max(close2[i-23:i])-1)*100
            max_drop[i,:] = close2[i]<max(close2[i-40:i+1])*0.85
            max_back1[i,:] = (close2[i]/max(hh2[i-2:i+1])-1)*100
            max_back_empty[i,:] = (close2[i]/min(ll2[i-20:i+1])-1)*100
            max_back_empty1[i,:] = close2[i]>=(max(hh2[i-72:i])+min(ll2[i-72:i+1])*2)/3 and cmp_logictable_c_more_ma20[i]==1 and max(hh2[i-72:i])/min(ll2[i-72:i])>1.06 
            
        buy_much_signal_all = buy_much_signal1 + buy_much_signal2 + buy_much_signal3 + buy_much_signal4 + buy_much_signal5 + buy_much_signal6 + buy_much_signal7 + buy_much_signal8 + buy_empty_signal1 + buy_empty_signal2 + buy_empty_signal3 + buy_empty_signal4 + buy_empty_signal5 + buy_empty_signal6 + buy_empty_signal7 + buy_empty_signal8
        print ("\t 开平仓信号计算 结束 %s \n" %time.ctime())
        #np.where(buy_much_signal3==1)
        #np.where(buy_empty_signal2==1)
        
        time11 = datetime.datetime.now()
        numtime = time11.minute
        numtime1 = time11.minute*60+time11.second
        if (numtime1>5) and (numtime<14):
            close2 = coin_date.iloc[:,4] 
            
            
            print('\t 平仓信号计算 开始 %s' %time.ctime())
            while(1):
                try:
                    present_price = float(okcoinFuture.future_ticker('eth_usd','quarter').get('ticker').get('last'))
                    break
                except:
                    time.sleep(2)
                    print('\t 获取合约现价超时')
                    continue
            '''
            while(1):
                try:
                     max_price = okcoinFuture.future_price_limit('quarter').get('high') #最高买价
                     break
                except:
                    time.sleep(2)
                    print('获取合约最高限价超时')
                    continue
            while(1):
                try:
                    time.sleep(1)
                    min_price = okcoinFuture.future_price_limit('quarter').get('low') #最低卖价
                    break
                except:
                    time.sleep(1)
                    print('获取合约最低限价超时')
                    continue'''
           
          
            can_sell_time = pd.Series([buy_total.iloc[:,0][i] for i in range(1,len(buy_total))] )
            can_sell_time = can_sell_time.apply(lambda x: datetime.datetime.fromtimestamp(time.mktime(time.strptime(x, '%Y-%m-%d %H:%M:%S'))))
            can_sell_time = [can_sell_time[i].year*1000000+can_sell_time[i].month*10000+can_sell_time[i].day*100+can_sell_time[i].hour for i in range(len(can_sell_time))]
            
            #c_more_ma5_ma10_ma20_ma30 = np.zeros([len(buy_total)-1,1])
            #max_drop = np.zeros([len(buy_total)-1,1])
            #
            #c_more_ma5_ma10_ma20_ma30[:] = cmp_logictable_c_more_ma5_ma10_ma20_ma30.values[-1]
            #max_drop[:] = close2.values[-1]<max(close2[-40:])*0.85
      
            
            ref2=datetime.datetime.now()-datetime.timedelta(hours=2)
            ref2_num=ref2.year*1000000+ref2.month*10000+ref2.day*100+ref2.hour
            ref3=datetime.datetime.now()-datetime.timedelta(hours=3)
            ref3_num=ref3.year*1000000+ref3.month*10000+ref3.day*100+ref3.hour
            ref4=datetime.datetime.now()-datetime.timedelta(hours=4)
            ref4_num=ref4.year*1000000+ref4.month*10000+ref4.day*100+ref4.hour
            ref5=datetime.datetime.now()-datetime.timedelta(hours=5)
            ref5_num=ref5.year*1000000+ref5.month*10000+ref5.day*100+ref5.hour
            ref6=datetime.datetime.now()-datetime.timedelta(hours=6)
            ref6_num=ref6.year*1000000+ref6.month*10000+ref6.day*100+ref6.hour
            ref7=datetime.datetime.now()-datetime.timedelta(hours=7)
            ref7_num=ref7.year*1000000+ref7.month*10000+ref7.day*100+ref7.hour
            ref12=datetime.datetime.now()-datetime.timedelta(hours=12)
            ref12_num=ref12.year*1000000+ref12.month*10000+ref12.day*100+ref12.hour
            ref15=datetime.datetime.now()-datetime.timedelta(hours=15)
            ref15_num=ref15.year*1000000+ref15.month*10000+ref15.day*100+ref15.hour
            ref24=datetime.datetime.now()-datetime.timedelta(hours=24)
            ref24_num=ref24.year*1000000+ref24.month*10000+ref24.day*100+ref24.hour
            ref25=datetime.datetime.now()-datetime.timedelta(hours=25)
            ref25_num=ref25.year*1000000+ref25.month*10000+ref25.day*100+ref25.hour
            ref30=datetime.datetime.now()-datetime.timedelta(hours=30)
            ref30_num=ref30.year*1000000+ref30.month*10000+ref30.day*100+ref30.hour
            ref35=datetime.datetime.now()-datetime.timedelta(hours=35)
            ref35_num=ref35.year*1000000+ref35.month*10000+ref35.day*100+ref35.hour
            ref10=datetime.datetime.now()-datetime.timedelta(hours=10)
            ref10_num=ref10.year*1000000+ref10.month*10000+ref10.day*100+ref10.hour
            ref20=datetime.datetime.now()-datetime.timedelta(hours=20)
            ref20_num=ref20.year*1000000+ref20.month*10000+ref20.day*100+ref20.hour
            ref17=datetime.datetime.now()-datetime.timedelta(hours=17)
            ref17_num=ref17.year*1000000+ref17.month*10000+ref17.day*100+ref17.hour
            ref19=datetime.datetime.now()-datetime.timedelta(hours=19)
            ref19_num=ref19.year*1000000+ref19.month*10000+ref19.day*100+ref19.hour
            ref70=datetime.datetime.now()-datetime.timedelta(hours=70)
            ref70_num=ref70.year*1000000+ref70.month*10000+ref70.day*100+ref70.hour
            ref72=datetime.datetime.now()-datetime.timedelta(hours=72)
            ref72_num=ref72.year*1000000+ref72.month*10000+ref72.day*100+ref72.hour
            ib1 = [i+1  for i in range(len(can_sell_time)) if  (buy_total.iloc[i+1,1]==1) & (can_sell_time[i]<=ref35_num)]
            ib2 = [i+1  for i in range(len(can_sell_time)) if  (buy_total.iloc[i+1,1]==20) & (can_sell_time[i]<=ref12_num)]
            ib3 = [i+1  for i in range(len(can_sell_time)) if  (buy_total.iloc[i+1,1]==3) & (can_sell_time[i]<=ref10_num)]
            ib4 = [i+1  for i in range(len(can_sell_time)) if  (buy_total.iloc[i+1,1]==40) & (can_sell_time[i]<=ref6_num)]
            ib5 = [i+1  for i in range(len(can_sell_time)) if  (buy_total.iloc[i+1,1]==50) & (can_sell_time[i]<=ref6_num)]
            ib6 = [i+1  for i in range(len(can_sell_time)) if  (buy_total.iloc[i+1,1]==6) & (can_sell_time[i]<=ref6_num)]
            ib7 = [i+1  for i in range(len(can_sell_time)) if  (buy_total.iloc[i+1,1]==7) & (can_sell_time[i]<=ref6_num)]
            ib8 = [i+1  for i in range(len(can_sell_time)) if  (buy_total.iloc[i+1,1]==8) & (can_sell_time[i]<=ref5_num)]
            ib9 = [i+1  for i in range(len(can_sell_time)) if  (buy_total.iloc[i+1,1]==9) & (can_sell_time[i]<=ref24_num)]
            ib10 = [i+1  for i in range(len(can_sell_time)) if  (buy_total.iloc[i+1,1]==10) & (can_sell_time[i]<=ref5_num)]
            ib11 = [i+1  for i in range(len(can_sell_time)) if  (buy_total.iloc[i+1,1]==-1) & (can_sell_time[i]<=ref35_num)]
            ib12 = [i+1  for i in range(len(can_sell_time)) if  (buy_total.iloc[i+1,1]==-2) & (can_sell_time[i]<=ref72_num)]
            ib13 = [i+1  for i in range(len(can_sell_time)) if  (buy_total.iloc[i+1,1]==-3) & (can_sell_time[i]<=ref10_num)]
            ib14 = [i+1  for i in range(len(can_sell_time)) if  (buy_total.iloc[i+1,1]==-40) & (can_sell_time[i]<=ref30_num)]
            ib15 = [i+1  for i in range(len(can_sell_time)) if  (buy_total.iloc[i+1,1]==-5) & (can_sell_time[i]<=ref25_num)]
            ib16 = [i+1  for i in range(len(can_sell_time)) if  (buy_total.iloc[i+1,1]==-60) & (can_sell_time[i]<=ref6_num)]
            ib17 = [i+1  for i in range(len(can_sell_time)) if  (buy_total.iloc[i+1,1]==-7) & (can_sell_time[i]<=ref15_num)]
            ib18 = [i+1  for i in range(len(can_sell_time)) if  (buy_total.iloc[i+1,1]==-8) & (can_sell_time[i]<=ref10_num)]
             
            ib0 =ib1+ib2+ib3+ib4+ib5+ib6+ib7+ib8+ib9+ib10+ib11+ib12+ib13+ib14+ib15+ib16+ib17+ib18
            
            
            ##平盈利多单
            can_sell_market_much_profit_ind1 = list(*np.where( ( present_price>buy_total.values[1:,2]*1.03) & (buy_total.values[1:,1]==1) ))#该平的盈利多单位置
            can_sell_market_much_profit_ind2 = list(*np.where( ( present_price>buy_total.values[1:,2]*1.5) & (buy_total.values[1:,1]==2) ))#该平的盈利多单位置
            can_sell_market_much_profit_ind3 = list(*np.where( ( present_price>buy_total.values[1:,2]*1.03) & (buy_total.values[1:,1]==3) ))#该平的盈利多单位置
            can_sell_market_much_profit_ind4 = list(*np.where( ( present_price>buy_total.values[1:,2]*2) & (buy_total.values[1:,1]==4) ))#该平的盈利多单位置
            can_sell_market_much_profit_ind5 = list(*np.where( ( present_price>buy_total.values[1:,2]*2) & (buy_total.values[1:,1]==5) ))#该平的盈利多单位置
            can_sell_market_much_profit_ind6 = list(*np.where( ( present_price>buy_total.values[1:,2]*1.06) & (buy_total.values[1:,1]==6) ))#该平的盈利多单位置
            can_sell_market_much_profit_ind7 = list(*np.where( ( present_price>buy_total.values[1:,2]*1.06) & (buy_total.values[1:,1]==7) ))#该平的盈利多单位置
            can_sell_market_much_profit_ind8 = list(*np.where( ( present_price>buy_total.values[1:,2]*1.05) & (buy_total.values[1:,1]==8) ))#该平的盈利多单位置
            can_sell_market_much_profit_ind9 = list(*np.where( ( present_price>buy_total.values[1:,2]*1.03) & (buy_total.values[1:,1]==9) ))#该平的盈利多单位置
            can_sell_market_much_profit_ind10 = list(*np.where( ( present_price>buy_total.values[1:,2]*1.02) & (buy_total.values[1:,1]==10) ))#该平的盈利多单位置
            can_sell_market_much_profit_ind = can_sell_market_much_profit_ind1+can_sell_market_much_profit_ind2+can_sell_market_much_profit_ind3+can_sell_market_much_profit_ind4+can_sell_market_much_profit_ind5+can_sell_market_much_profit_ind6+can_sell_market_much_profit_ind7+can_sell_market_much_profit_ind8+can_sell_market_much_profit_ind9+can_sell_market_much_profit_ind10
        
            ##平盈利空单
            can_sell_market_empty_profit_ind1 = list(*np.where( ( present_price<buy_total.values[1:,2]*0.93) & (buy_total.values[1:,1]==-1)))#该平的盈利空单位置*0.89
            can_sell_market_empty_profit_ind2 = list(*np.where( ( present_price<buy_total.values[1:,2]*0.7) & (buy_total.values[1:,1]==-2)))#该平的盈利空单位置
            can_sell_market_empty_profit_ind3 = list(*np.where( ( present_price<buy_total.values[1:,2]*0.92) & (buy_total.values[1:,1]==-3)))#该平的盈利空单位置*0.92
            can_sell_market_empty_profit_ind4 = list(*np.where( ( present_price<buy_total.values[1:,2]*0.8) & (buy_total.values[1:,1]==-4)))#该平的盈利空单位置
            can_sell_market_empty_profit_ind5 = list(*np.where( ( present_price<buy_total.values[1:,2]*0.9) & (buy_total.values[1:,1]==-5)))#该平的盈利空单位置
            can_sell_market_empty_profit_ind6 = list(*np.where( ( present_price<buy_total.values[1:,2]*0.8) & (buy_total.values[1:,1]==-6)))#该平的盈利空单位置
            can_sell_market_empty_profit_ind7 = list(*np.where( ( present_price<buy_total.values[1:,2]*0.93) & (buy_total.values[1:,1]==-7)))#该平的盈利空单位置
            can_sell_market_empty_profit_ind8 = list(*np.where( ( present_price<buy_total.values[1:,2]*0.95) & (buy_total.values[1:,1]==-8)))#该平的盈利空单位置
            can_sell_market_empty_profit_ind = can_sell_market_empty_profit_ind1+can_sell_market_empty_profit_ind2+can_sell_market_empty_profit_ind3+can_sell_market_empty_profit_ind4+can_sell_market_empty_profit_ind5+can_sell_market_empty_profit_ind6+can_sell_market_empty_profit_ind7+can_sell_market_empty_profit_ind8
           
            ##平亏损多单
            can_sell_market_much_loss_ind1 = list(*np.where( ( (present_price<buy_total.values[1:,2]*0.98) | (cmp_logictable_c_less1_ma10.values[-1]==1) | (cmp_logictable_c_less1_ma20.values[-1]==1) | (sell_much_signal3[-1]==1) | (sell_much_signal4[-1]==1) | (sell_much_signal5[-1]==1) | (sell_much_signal6[-1]==1) | (sell_much_signal7[-1]==1) | (sell_much_signal8[-1]==1) | (sell_much_signal9[-1]==1) | (sell_much_signal10[-1]==1) | (sell_much_signal11[-1]==1) | (sell_much_signal12[-1]==1) | (sell_much_signal13[-1]==1) ) & (buy_total.values[1:,1]==1) ) )#该平的亏损多单位置
            #can_sell_market_much_loss_ind2 = list(*np.where( ( (present_price<buy_total.values[1:,2]*0.97) | (cmp_logictable_c_less1_ma120.values[-1]==1) | (max_back[-1,:]<-10) | (sum(cmp_logictable_c_less_ma20[-29:])>=26 and sum(cmp_logictable_c_less_ma30[-23:])>=20) ) & (buy_total.values[1:,1]==2)))#该平的亏损多单位置
            can_sell_market_much_loss_ind2 = list(*np.where( ( (present_price<buy_total.values[1:,2]*0.97) | (cmp_logictable_c_less1_ma120.values[-1]==1) | (sell_much_signal17[-1]==1) | (sell_much_signal18[-1]==1) ) &  (buy_total.values[1:,1]==2)  ) )#该平的亏损多单位置
            #can_sell_market_much_loss_ind3 = list(*np.where( ( present_price<buy_total.values[1:,2]*0.985) & (buy_total.values[1:,1]==3)))#该平的亏损多单位置
            can_sell_market_much_loss_ind3 = list(*np.where( ( (present_price<buy_total.values[1:,2]*0.98) | (sell_much_signal10[-1]==1) | (sell_much_signal14[-1]==1) | (cmp_logictable_c_less1_ma5.values[-1]==1 ) | (sell_much_signal15[-1]==1) | (sell_much_signal16[-1]==1) ) & (buy_total.values[1:,1]==3)  ) )#该平的亏损多单位置
            can_sell_market_much_loss_ind4 = list(*np.where( ( (present_price<buy_total.values[1:,2]*0.98) | (cmp_logictable_c_less_ma20.values[-1]==1) ) & (buy_total.values[1:,1]==4)))#该平的亏损多单位置
            can_sell_market_much_loss_ind5 = list(*np.where( ( (present_price<buy_total.values[1:,2]*0.97) | (cmp_logictable_c_less_ma5_ma10_ma20_ma30.values[-1]==1) ) & (buy_total.values[1:,1]==5)))#该平的亏损多单位置
            can_sell_market_much_loss_ind6 = list(*np.where( ( present_price<buy_total.values[1:,2]*0.985) & (buy_total.values[1:,1]==6)))#该平的亏损多单位置
            can_sell_market_much_loss_ind7 = list(*np.where( ( present_price<buy_total.values[1:,2]*0.99) & (buy_total.values[1:,1]==7)))#该平的亏损多单位置
            can_sell_market_much_loss_ind8 = list(*np.where( ( present_price<buy_total.values[1:,2]*0.98) & (buy_total.values[1:,1]==8)))#该平的亏损多单位置
            can_sell_market_much_loss_ind9 = list(*np.where( ( present_price<buy_total.values[1:,2]*0.97) & (buy_total.values[1:,1]==9)))#该平的亏损多单位置
            can_sell_market_much_loss_ind10 = list(*np.where( ( present_price<buy_total.values[1:,2]*0.99) & (buy_total.values[1:,1]==10)))#该平的亏损多单位置
            can_sell_market_much_loss_ind = can_sell_market_much_loss_ind1+can_sell_market_much_loss_ind2+can_sell_market_much_loss_ind3+can_sell_market_much_loss_ind4+can_sell_market_much_loss_ind5+can_sell_market_much_loss_ind6+can_sell_market_much_loss_ind7+can_sell_market_much_loss_ind8+can_sell_market_much_loss_ind9+can_sell_market_much_loss_ind10
             
            ##平亏损空单
            #can_sell_market_empty_loss_ind1 = list(*np.where(( (present_price>buy_total.values[1:,2]*1.02) | (cmp_logictable_c_more1_ma10.values[-1]==1) | (sum(cmp_logictable_redK[-5:])==5) ) & (buy_total.values[1:,1]==-1)))#该平的亏损空单位置
            can_sell_market_empty_loss_ind1 = list(*np.where(( (present_price>buy_total.values[1:,2]*1.02) | (cmp_logictable_c_more1_ma10.values[-1]==1) | (sell_empty_signal4[-1]==1) ) & (buy_total.values[1:,1]==-1)))#该平的亏损空单位置
            #can_sell_market_empty_loss_ind2 = list(*np.where(( ( present_price>buy_total.values[1:,2]*1.02) | (cmp_logictable_c_more1_ma120.values[-1]==1) | (max_back_empty[-1,:]>9) | (max_back_empty1[-1,:]==1)  ) & (buy_total.values[1:,1]==-2)))#该平的亏损空单位置
            can_sell_market_empty_loss_ind2 = list(*np.where(( ( present_price>buy_total.values[1:,2]*1.02) | (cmp_logictable_c_more1_ma120.values[-1]==1) | (sell_empty_signal5[-1]==1) | (sell_empty_signal6[-1]==1)  ) & (buy_total.values[1:,1]==-2)))#该平的亏损空单位置
            
            can_sell_market_empty_loss_ind3 = list(*np.where(( present_price>buy_total.values[1:,2]*1.02) & (buy_total.values[1:,1]==-3)))#该平的亏损空单位置
            can_sell_market_empty_loss_ind4 = list(*np.where(( (present_price>buy_total.values[1:,2]*1.02) | (cmp_logictable_c_more_ma20.values[-1]==1)) & (buy_total.values[1:,1]==-4)))#该平的亏损空单位置
            can_sell_market_empty_loss_ind5 = list(*np.where((present_price>buy_total.values[1:,2]*1.015) & (buy_total.values[1:,1]==-5)))#该平的亏损空单位置
            can_sell_market_empty_loss_ind6 = list(*np.where(( (present_price>buy_total.values[1:,2]*1.02) | (cmp_logictable_c_more_ma5_ma10_ma20_ma30.values[-1]==1)) & (buy_total.values[1:,1]==-6)))#该平的亏损空单位置
            can_sell_market_empty_loss_ind7 = list(*np.where(( (present_price>buy_total.values[1:,2]*1.03) | (cmp_logictable_c_more_ma20.values[-1]==1) | (sum(cmp_logictable_redK[i-3:i+1])==4)) & (buy_total.values[1:,1]==-7)))#该平的亏损空单位置
            can_sell_market_empty_loss_ind8 = list(*np.where(( (present_price>buy_total.values[1:,2]*1.03) | (sum(cmp_logictable_redK[i-3:i+1])==4)) & (buy_total.values[1:,1]==-8)))#该平的亏损空单位置
            can_sell_market_empty_loss_ind = can_sell_market_empty_loss_ind1+can_sell_market_empty_loss_ind2+can_sell_market_empty_loss_ind3+can_sell_market_empty_loss_ind4+can_sell_market_empty_loss_ind5+can_sell_market_empty_loss_ind6+can_sell_market_empty_loss_ind7+can_sell_market_empty_loss_ind8
            
            
            ###
            can_sell_market_much_ind = list(np.array(list(set(can_sell_market_much_profit_ind+can_sell_market_much_loss_ind)))+1)#同ind 与 ind+1
            can_sell_market_empty_ind = list(np.array(list(set(can_sell_market_empty_profit_ind+can_sell_market_empty_loss_ind)))+1)
            if len(ib0):#非空时执行
                can_sell_market_much_ind = list(set(can_sell_market_much_ind+[ib0[i] for i in range(len(ib0)) if buy_total.values[ib0[i],1]>0  ]))
                can_sell_market_empty_ind = list(set(can_sell_market_empty_ind+[ib0[i] for i in range(len(ib0)) if buy_total.values[ib0[i],1]<0  ]))
            else:
                print('\t ib0为空')
                
            ib = can_sell_market_much_ind+can_sell_market_empty_ind
            can_sell = pd.DataFrame(np.zeros((len(ib),5)))
    ib = ib+can_sell_market_loss_present
    can_sell = pd.DataFrame(np.zeros((len(ib),6)))
    if len(ib)>0:
        while(1):
            try:
                high_price_limit = okcoinFuture.future_price_limit('eth_usd','quarter').get('high')
                break
            except:
                print('\t 获取最高限价超时')
                time.sleep(1)
                continue
        
        while(1):
            try:
                low_price_limit = okcoinFuture.future_price_limit('eth_usd','quarter').get('low')
                break
            except:
                print('\t 获取最低限价超时')
                time.sleep(1)
                continue
        present_price_margin_much_sell = max(coin_date1.iloc[:,4].iloc[-1]*0.98,low_price_limit*1.005)
        present_price_margin_empty_sell = min(coin_date1.iloc[:,4].iloc[-1]*1.02,high_price_limit*0.995)
        can_sell.iloc[:,[0,1,2,3,4,5]] = [['eth_usd','quarter',present_price_margin_much_sell if buy_total.iloc[i,1]>0 else present_price_margin_empty_sell,np.floor(buy_total.iloc[i,2]*buy_total.iloc[i,3]/1),3 if buy_total.iloc[i,1]>0 else 4 , buy_total.iloc[i,1]]for i in ib]
        #can_sell里面1,2,3,4列为现在平仓的 '1合约类型','2委托数量','3委托价格','4委托方式'(1:开多 2:开空 3:平多 4:平空)
        can_sell1 = can_sell.iloc[np.where(can_sell.iloc[:,3]>=500)]
        sell_num = len(can_sell1)
        can_sell2 = can_sell.iloc[np.where(can_sell.iloc[:,3]<500)]
        can_sell1 = pd.DataFrame(np.tile(can_sell1,[5,1]))#分5次下单
        buy_total.drop(ib,inplace=True)
        buy_total.index = range(len(buy_total))
        pk1 = open(root+'\\buy_total_%s.spydata'%coin,'wb')
        pickle.dump(buy_total,pk1)
        pk1.close()
        print('\t 平仓信号计算 结束 %s \n' %time.ctime())
            
        contents_sell = '\n\n'.join([('合约类型：quarter \n平仓价格：%s \n平仓数量：%s \n委托方式：%s \n交易时间：%s'%(can_sell.iloc[i,2],round(can_sell.iloc[i,3],2),'平多' if can_sell.iloc[i,4]==3 else '平空',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))) for i in range(len(can_sell))])

        '''平仓'''
        if len(can_sell2)>0:
            for j in range(len(can_sell2)):
                while(1):
                    try:
                        high_price_limit = okcoinFuture.future_price_limit('eth_usd','quarter').get('high')
                        break
                    except:
                        print('\t 获取最高限价超时')
                        time.sleep(1)
                        continue
        
                while(1):
                    try:
                        low_price_limit = okcoinFuture.future_price_limit('eth_usd','quarter').get('low')
                        break
                    except:
                        print('\t 获取最低限价超时')
                        time.sleep(1)
                        continue
                    
                while(1):
                    try:
                        present_price = float(okcoinFuture.future_ticker('eth_usd','quarter').get('ticker').get('last'))
                        break
                    except:
                        time.sleep(2)
                        print('\t 获取合约现价超时')
                        continue
                present_price_margin_much_sell = max(present_price*0.98,low_price_limit*1.005)
                present_price_margin_empty_sell = min(present_price*1.02,high_price_limit*0.995)
                can_sell2.iloc[:,2]=[present_price_margin_much_sell if i>0 else present_price_margin_empty_sell for i in can_sell2.iloc[:,5]]
                while(1):
                    try:
                        depth=okcoinFuture.future_depth('eth_usd','quarter','10')
                        break
                    except:
                        time.sleep(1)
                        print('获取深度信息超时')
                        continue
                asks=depth.get('asks')
                asks_amount_sum=sum([asks[i][1] for i in range(len(asks))])
                bids=depth.get('bids')
                bids_amount_sum=sum([bids[i][1] for i in range(len(bids))])
                if (can_sell2.iloc[j,5]>0) & (bids_amount_sum>can_sell2.iloc[j,3]*3):
                        time.sleep(0.1)
                        
                elif (can_sell2.iloc[j,5]<0) & (asks_amount_sum>can_sell2.iloc[j,3]*3):
                     time.sleep(0.1)
                    
                else:
                     time.sleep(3)
                     
                a11=1
                while(1):
                    try:
                        if run_tate==1:
                            SendOrder_sell = okcoinFuture.future_trade(can_sell2.iloc[j,0],str(can_sell2.iloc[j,1]),str(can_sell2.iloc[j,2]),str(can_sell2.iloc[j,3]),str(int(can_sell2.iloc[j,4])),'0','10')#访问频率 5次/1秒(按币种单独计算)
                            assert json.loads(SendOrder_sell).get('result')==True
                        print('\t 第%s次平仓完毕'%j)
                        break
                    except:
                        a11+=1
                        time.sleep(1)
                        print('\t 分批平仓超时')
                        if a11<10:
                          continue
                        else:
                            break
            
        if len(can_sell1)>0:
            can_sell1.iloc[:-sell_num,3] = pd.DataFrame([np.floor( float(can_sell1.iloc[i,3])*0.2) for i in range(len(can_sell1)- sell_num)]).iloc[:,0]
            can_sell1.iloc[ sell_num*4:,3] = pd.DataFrame([ float(can_sell1.iloc[i,3])-float(can_sell1.iloc[i-sell_num,3])*4 for i in range(sell_num*4,len( can_sell1))],index=range(sell_num*4,len( can_sell1))).iloc[:,0]
            for i in range(0,len(can_sell1),sell_num): 
                can_sell10 = can_sell1[i:i+sell_num]
                can_sell10.index = range(len(can_sell10))
                #can_sell10=pd.DataFrame(np.tile( can_sell10,[5,1]))#分5次下单
                for j in range(len(can_sell10)):
                    while(1):
                        try:
                            high_price_limit = okcoinFuture.future_price_limit('eth_usd','quarter').get('high')
                            break
                        except:
                            print('\t 获取最高限价超时')
                            time.sleep(1)
                            continue
        
                    while(1):
                        try:
                            low_price_limit = okcoinFuture.future_price_limit('eth_usd','quarter').get('low')
                            break
                        except:
                            print('\t 获取最低限价超时')
                            time.sleep(1)
                            continue
                        
                    while(1):
                        try:
                            present_price = float(okcoinFuture.future_ticker('eth_usd','quarter').get('ticker').get('last'))
                            break
                        except:
                            time.sleep(1)
                            print('\t 获取合约现价超时')
                            continue
                    present_price_margin_much_sell = max(present_price*0.98,low_price_limit*1.005)
                    present_price_margin_empty_sell = min(present_price*1.02,high_price_limit*0.995)
                    can_sell10.iloc[:,2]=[present_price_margin_much_sell if i>0 else present_price_margin_empty_sell for i in can_sell10.iloc[:,5]]
                    while(1):
                        try:
                            depth=okcoinFuture.future_depth('eth_usd','quarter','10')
                            break
                        except:
                            time.sleep(1)
                            print('获取深度信息超时')
                            continue
                    asks=depth.get('asks')
                    asks_amount_sum=sum([asks[i][1] for i in range(len(asks))])
                    bids=depth.get('bids')
                    bids_amount_sum=sum([bids[i][1] for i in range(len(bids))])
                    if (can_sell10.iloc[j,5]>0) & (bids_amount_sum>can_sell10.iloc[j,3]*3):
                            time.sleep(0.1)
                            
                    elif (can_sell10.iloc[j,5]<0) & (asks_amount_sum>can_sell10.iloc[j,3]*3):
                         time.sleep(0.1)
                        
                    else:
                         time.sleep(3)
                         
                    a11=1
                    while(1):
                        try:
                            if run_tate==1:
                                SendOrder_sell= okcoinFuture.future_trade(can_sell10.iloc[j,0],str(can_sell10.iloc[j,1]),str(can_sell10.iloc[j,2]),str(can_sell10.iloc[j,3]),str(int(can_sell10.iloc[j,4])),'0','10')#访问频率 5次/1秒(按币种单独计算)
                                assert json.loads(SendOrder_sell).get('result')==True
                            print('\t 每组第%s次平仓完毕'%j)
                            break
                        except:
                            a11+=1
                            time.sleep(1)
                            print('\t 分批下单超时')
                            if a11<10:
                               continue
                            else:
                                break
                                
                count = i/sell_num
                print('\t 第%s组平仓完毕'%count) 
                time.sleep(10)
           
    else:
        if numtime>6:
           contents_sell = '0平仓' 
    
    
    if (numtime1>5) and (numtime<15) and (p2==1) and (p1==2):
        p2=2
        '''资金分配计算'''
        print('\t 资金分配计算 开始 %s' %time.ctime())
        time11 = datetime.datetime.now()
        numtime = time11.hour*100+time11.minute
        f = open(root+'\\capital_change_total_%s.spydata'%coin,'rb')
        capital_change_total = pickle.load(f)
        f.close()
        holdC = pd.DataFrame(np.zeros([0,5]))#holdC = pd.DataFrame(np.zeros([0,5]))
        holdC0 = pd.DataFrame(np.zeros([1,5]))
        present_price = close2.iloc[-1]
        pre_present_price = close2.iloc[-2]
        capital_change_total.iloc[1:,1:5]=capital_change_total.iloc[1:,1:5]*asset_rate
        Asset = capital_change_total
        
        f = open(root+'\\buy_total_%s.spydata'%coin,'rb')
        buy_total = pickle.load(f)
        f.close()
        
        if len(buy_total)<7:#len(buy_total)<8#正常
            
        
            '''if   buy_much_signal_all[-1]==1 and len(buy_total)-1<2:
                capital_distribution_coefficient = 1/50#1/40#1/30	
                capital_distribution_coefficient_initial = 1/150
            elif buy_much_signal_all[-1]==1 and len(buy_total)-1>=2:
                capital_distribution_coefficient = 1/50#1/40
                capital_distribution_coefficient_initial = 1/150
            elif buy_much_signal_all[-1]==2:
                capital_distribution_coefficient = 1/50
                capital_distribution_coefficient_initial = 1/200
            elif buy_much_signal_all[-1]==3:
                capital_distribution_coefficient = 1/60
                capital_distribution_coefficient_initial = 1/200
            elif buy_much_signal_all[-1]>3:
                capital_distribution_coefficient = 1/100
                capital_distribution_coefficient_initial = 1/200
            elif buy_much_signal_all[-1]==0:
                capital_distribution_coefficient = 1/100
                
            capital_distribution_coefficient = 1/100#linshi
                
            #buy_much_signal1仓位分配
            if len(list(*np.where( (buy_total.values[1:,1]==1) & (buy_total.values[1:,3]>0) ) ) )==0:
                capital_distribution_coefficient_pyramid_much_signal1 = 1/50#1/30
                capital_distribution_coefficient_pyramid_initial_much_signal1 = 1.5/100
            elif len(list(*np.where( (buy_total.values[1:,1]==1) & (buy_total.values[1:,3]>0) ) ) )==1:
                capital_distribution_coefficient_pyramid_much_signal1 = 1/50#1/40
                capital_distribution_coefficient_pyramid_initial_much_signal1 = 1.25/100
            elif len(list(*np.where( (buy_total.values[1:,1]==1) & (buy_total.values[1:,3]>0) ) ) )>=2:
                capital_distribution_coefficient_pyramid_much_signal1 = 1/50
                capital_distribution_coefficient_pyramid_initial_much_signal1 = 1/100
            else:
                capital_distribution_coefficient_pyramid_much_signal1 = 1/50
                capital_distribution_coefficient_pyramid_initial_much_signal1 = 1/100
            
            capital_distribution_coefficient_pyramid_much_signal1 = 1/100#linshi
            capital_distribution_coefficient_pyramid_initial_much_signal1 = 1/100#linshi'''
            
            
            capital_distribution_coefficient0 = 1/125
            if need_taobao==1:
                initial_profit=Asset.iloc[-1,4]*asset_rate/Asset0
                max_draw=Asset.iloc[-1,4]*asset_rate/max(Asset.iloc[1:,4])
            elif need_taobao==0:
                initial_profit=Asset.iloc[-1,1]*asset_rate/Asset0
                max_draw=Asset.iloc[-1,1]*asset_rate/max(Asset.iloc[1:,1])
            if Asset.iloc[-1,4]/Asset0>1.01:
                capital_distribution_coefficient0=1/max(65,(125-(initial_profit-1)*100*5)) #1/max(40,(150-(initial_profit-1)*100*10))
            if Asset.iloc[-1,4]/Asset0>1.1:
                capital_distribution_coefficient0=1/min(150,(55+(1-max_draw)*100*6)) #1/min(150,(40+(1-max_draw)*100*10))
                
            if   buy_much_signal_all[-1]==1 and len(buy_total)-1<2:
                capital_distribution_coefficient = capital_distribution_coefficient0
            elif buy_much_signal_all[-1]==1 and len(buy_total)-1>=2:
                capital_distribution_coefficient = capital_distribution_coefficient0*0.85
            elif buy_much_signal_all[-1]==2:
                capital_distribution_coefficient =capital_distribution_coefficient0*0.75
            elif buy_much_signal_all[-1]==3:
                capital_distribution_coefficient =capital_distribution_coefficient0*0.65
            elif buy_much_signal_all[-1]>3:
                capital_distribution_coefficient = 1/100
                    
            
            if buy_much_signal1[-1,:]==1:
                holdC0.iloc[0,0] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #'%Y-%m-%d %H:%M:%S'  北京时间
                holdC0.iloc[0,1] = 1 #买入方式
                holdC0.iloc[0,2] = present_price  #开仓价格
                if (Asset.iloc[-1,4]/max(Asset.iloc[1:,4])>0.9) & (Asset.iloc[-1,4]/Asset0>1.07):
                    holdC0.iloc[0,3] = Asset.iloc[-1,3]*capital_distribution_coefficient*1.2 #开仓个数 #开仓张数
                    holdC0.iloc[0,4] = Asset.iloc[-1,3]*capital_distribution_coefficient*1.2*present_price#开仓金额
                else:
                    if len(buy_total)<6:
                        holdC0.iloc[0,3] = Asset.iloc[-1,3]*1/100
                        holdC0.iloc[0,4] = Asset.iloc[-1,3]*1/100*present_price#开仓金额
                    else:
                        holdC0.iloc[0,3] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)
                        holdC0.iloc[0,4] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)*10
                holdC = holdC.append(holdC0,ignore_index=True)
                
            if buy_much_signal2[-1,:]==1:
                holdC0.iloc[0,0] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                holdC0.iloc[0,1] = 2 
                holdC0.iloc[0,2] = present_price  
                if (Asset.iloc[-1,4]/max(Asset.iloc[1:,4])>0.9) & (Asset.iloc[-1,4]/Asset0>1.07):
                    holdC0.iloc[0,3] = Asset.iloc[-1,3]*capital_distribution_coefficient
                    holdC0.iloc[0,4] = Asset.iloc[-1,3]*capital_distribution_coefficient*present_price
                else:
                    if len(buy_total)<6:
                        holdC0.iloc[0,3] = Asset.iloc[-1,3]*1/100
                        holdC0.iloc[0,4] = Asset.iloc[-1,3]*1/100*present_price
                    else:
                        holdC0.iloc[0,3] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)
                        holdC0.iloc[0,4] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)*10
                holdC = holdC.append(holdC0,ignore_index=True)
            
            if buy_much_signal3[-1,:]==2:
                holdC0.iloc[0,0] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                holdC0.iloc[0,1] = 3 
                holdC0.iloc[0,2] = present_price  
                if (Asset.iloc[-1,4]/max(Asset.iloc[1:,4])>0.9) & (Asset.iloc[-1,4]/Asset0>1.07):
                    holdC0.iloc[0,3] = Asset.iloc[-1,3]*capital_distribution_coefficient
                    holdC0.iloc[0,4] = Asset.iloc[-1,3]*capital_distribution_coefficient*present_price
                else:
                    if len(buy_total)<6:
                        holdC0.iloc[0,3] = Asset.iloc[-1,3]*1/100
                        holdC0.iloc[0,4] = Asset.iloc[-1,3]*1/100*present_price
                    else:
                        holdC0.iloc[0,3] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)
                        holdC0.iloc[0,4] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)*10
                holdC = holdC.append(holdC0,ignore_index=True)
                
            if buy_much_signal4[-1,:]==2:
                holdC0.iloc[0,0] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                holdC0.iloc[0,1] = 4 
                holdC0.iloc[0,2] = present_price  
                if (Asset.iloc[-1,4]/max(Asset.iloc[1:,4])>0.9) & (Asset.iloc[-1,4]/Asset0>1.07):
                    holdC0.iloc[0,3] = Asset.iloc[-1,3]*capital_distribution_coefficient
                    holdC0.iloc[0,4] = Asset.iloc[-1,3]*capital_distribution_coefficient*present_price
                else:
                    if len(buy_total)<6:
                        holdC0.iloc[0,3] = Asset.iloc[-1,3]*1/100
                        holdC0.iloc[0,4] = Asset.iloc[-1,3]*1/100*present_price
                    else:
                        holdC0.iloc[0,3] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)
                        holdC0.iloc[0,4] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)*10
                holdC = holdC.append(holdC0,ignore_index=True)
            
            if buy_much_signal5[-1,:]==2:
                holdC0.iloc[0,0] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                holdC0.iloc[0,1] = 5 
                holdC0.iloc[0,2] = present_price  
                if (Asset.iloc[-1,4]/max(Asset.iloc[1:,4])>0.9) & (Asset.iloc[-1,4]/Asset0>1.07):
                    holdC0.iloc[0,3] = Asset.iloc[-1,3]*capital_distribution_coefficient
                    holdC0.iloc[0,4] = Asset.iloc[-1,3]*capital_distribution_coefficient*present_price
                else:
                    if len(buy_total)<6:
                        holdC0.iloc[0,3] = Asset.iloc[-1,3]*1/100
                        holdC0.iloc[0,4] = Asset.iloc[-1,3]*1/100*present_price
                    else:
                        holdC0.iloc[0,3] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)
                        holdC0.iloc[0,4] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)*10
                holdC = holdC.append(holdC0,ignore_index=True)
                
            if buy_much_signal6[-1,:]==2:
                holdC0.iloc[0,0] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                holdC0.iloc[0,1] = 6 
                holdC0.iloc[0,2] = present_price  
                if (Asset.iloc[-1,4]/max(Asset.iloc[1:,4])>0.9) & (Asset.iloc[-1,4]/Asset0>1.07):
                    holdC0.iloc[0,3] = Asset.iloc[-1,3]*capital_distribution_coefficient
                    holdC0.iloc[0,4] = Asset.iloc[-1,3]*capital_distribution_coefficient*present_price
                else:
                    if len(buy_total)<6:
                        holdC0.iloc[0,3] = Asset.iloc[-1,3]*1/100
                        holdC0.iloc[0,4] = Asset.iloc[-1,3]*1/100*present_price
                    else:
                        holdC0.iloc[0,3] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)
                        holdC0.iloc[0,4] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)*10
                holdC = holdC.append(holdC0,ignore_index=True)
                
            if buy_much_signal7[-1,:]==2:
                holdC0.iloc[0,0] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                holdC0.iloc[0,1] = 7 
                holdC0.iloc[0,2] = present_price  
                if (Asset.iloc[-1,4]/max(Asset.iloc[1:,4])>0.9) & (Asset.iloc[-1,4]/Asset0>1.07):
                    holdC0.iloc[0,3] = Asset.iloc[-1,3]*capital_distribution_coefficient
                    holdC0.iloc[0,4] = Asset.iloc[-1,3]*capital_distribution_coefficient*present_price
                else:
                    if len(buy_total)<6:
                        holdC0.iloc[0,3] = Asset.iloc[-1,3]*1/100
                        holdC0.iloc[0,4] = Asset.iloc[-1,3]*1/100*present_price
                    else:
                        holdC0.iloc[0,3] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)
                        holdC0.iloc[0,4] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)*10
                holdC = holdC.append(holdC0,ignore_index=True)
            
            if buy_much_signal8[-1,:]==2:
                holdC0.iloc[0,0] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                holdC0.iloc[0,1] = 8 
                holdC0.iloc[0,2] = present_price  
                if (Asset.iloc[-1,4]/max(Asset.iloc[1:,4])>0.9) & (Asset.iloc[-1,4]/Asset0>1.07):
                    holdC0.iloc[0,3] = Asset.iloc[-1,3]*capital_distribution_coefficient
                    holdC0.iloc[0,4] = Asset.iloc[-1,3]*capital_distribution_coefficient*present_price
                else:
                    if len(buy_total)<6:
                        holdC0.iloc[0,3] = Asset.iloc[-1,3]*1/100
                        holdC0.iloc[0,4] = Asset.iloc[-1,3]*1/100*present_price
                    else:
                        holdC0.iloc[0,3] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)
                        holdC0.iloc[0,4] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)*10
                holdC = holdC.append(holdC0,ignore_index=True)  
            
            if buy_much_signal9[-1,:]==2:
                holdC0.iloc[0,0] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                holdC0.iloc[0,1] = 9 
                holdC0.iloc[0,2] = present_price  
                if (Asset.iloc[-1,4]/max(Asset.iloc[1:,4])>0.9) & (Asset.iloc[-1,4]/Asset0>1.07):
                    holdC0.iloc[0,3] = Asset.iloc[-1,3]*capital_distribution_coefficient
                    holdC0.iloc[0,4] = Asset.iloc[-1,3]*capital_distribution_coefficient*present_price
                else:
                    if len(buy_total)<6:
                        holdC0.iloc[0,3] = Asset.iloc[-1,3]*1/100
                        holdC0.iloc[0,4] = Asset.iloc[-1,3]*1/100*present_price
                    else:
                        holdC0.iloc[0,3] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)
                        holdC0.iloc[0,4] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)*10
                holdC = holdC.append(holdC0,ignore_index=True)
            
            if buy_much_signal10[-1,:]==2:
                holdC0.iloc[0,0] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                holdC0.iloc[0,1] = 10 
                holdC0.iloc[0,2] = present_price  
                if (Asset.iloc[-1,4]/max(Asset.iloc[1:,4])>0.9) & (Asset.iloc[-1,4]/Asset0>1.07):
                    holdC0.iloc[0,3] = Asset.iloc[-1,3]*capital_distribution_coefficient
                    holdC0.iloc[0,4] = Asset.iloc[-1,3]*capital_distribution_coefficient*present_price
                else:
                    if len(buy_total)<6:
                        holdC0.iloc[0,3] = Asset.iloc[-1,3]*1/100
                        holdC0.iloc[0,4] = Asset.iloc[-1,3]*1/100*present_price
                    else:
                        holdC0.iloc[0,3] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)
                        holdC0.iloc[0,4] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)*10
                holdC = holdC.append(holdC0,ignore_index=True)
            
            
            if buy_empty_signal1[-1,:]==1:
                holdC0.iloc[0,0] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                holdC0.iloc[0,1] = -1 
                holdC0.iloc[0,2] = present_price  
                if (Asset.iloc[-1,4]/max(Asset.iloc[1:,4])>0.9) & (Asset.iloc[-1,4]/Asset0>1.07):
                    holdC0.iloc[0,3] = Asset.iloc[-1,3]*capital_distribution_coefficient*1.2
                    holdC0.iloc[0,4] = Asset.iloc[-1,3]*capital_distribution_coefficient*1.2*present_price
                else:
                    if len(buy_total)<6:
                        holdC0.iloc[0,3] = Asset.iloc[-1,3]*1/100
                        holdC0.iloc[0,4] = Asset.iloc[-1,3]*1/100*present_price
                    else:
                        holdC0.iloc[0,3] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)
                        holdC0.iloc[0,4] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)*10
                holdC = holdC.append(holdC0,ignore_index=True)
            
            if buy_empty_signal2[-1,:]==1:
                holdC0.iloc[0,0] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                holdC0.iloc[0,1] = -2 
                holdC0.iloc[0,2] = present_price  
                if (Asset.iloc[-1,4]/max(Asset.iloc[1:,4])>0.9) & (Asset.iloc[-1,4]/Asset0>1.07):
                    holdC0.iloc[0,3] = Asset.iloc[-1,3]*capital_distribution_coefficient
                    holdC0.iloc[0,4] = Asset.iloc[-1,3]*capital_distribution_coefficient*present_price
                else:
                    if len(buy_total)<6:
                        holdC0.iloc[0,3] = Asset.iloc[-1,3]*1/100
                        holdC0.iloc[0,4] = Asset.iloc[-1,3]*1/100*present_price
                    else:
                        holdC0.iloc[0,3] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)
                        holdC0.iloc[0,4] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)*10
                holdC = holdC.append(holdC0,ignore_index=True)
                
            if buy_empty_signal3[-1,:]==2:
                holdC0.iloc[0,0] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                holdC0.iloc[0,1] = -3 
                holdC0.iloc[0,2] = present_price  
                if (Asset.iloc[-1,4]/max(Asset.iloc[1:,4])>0.9) & (Asset.iloc[-1,4]/Asset0>1.07):
                    holdC0.iloc[0,3] = Asset.iloc[-1,3]*capital_distribution_coefficient
                    holdC0.iloc[0,4] = Asset.iloc[-1,3]*capital_distribution_coefficient*present_price
                else:
                    if len(buy_total)<6:
                        holdC0.iloc[0,3] = Asset.iloc[-1,3]*1/100
                        holdC0.iloc[0,4] = Asset.iloc[-1,3]*1/100*present_price
                    else:
                        holdC0.iloc[0,3] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)
                        holdC0.iloc[0,4] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)*10
                holdC = holdC.append(holdC0,ignore_index=True)
                
            if buy_empty_signal4[-1,:]==2:
                holdC0.iloc[0,0] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                holdC0.iloc[0,1] = -4 
                holdC0.iloc[0,2] = present_price  
                if (Asset.iloc[-1,4]/max(Asset.iloc[1:,4])>0.9) & (Asset.iloc[-1,4]/Asset0>1.07):
                    holdC0.iloc[0,3] = Asset.iloc[-1,3]*capital_distribution_coefficient
                    holdC0.iloc[0,4] = Asset.iloc[-1,3]*capital_distribution_coefficient*present_price
                else:
                    if len(buy_total)<6:
                        holdC0.iloc[0,3] = Asset.iloc[-1,3]*1/100
                        holdC0.iloc[0,4] = Asset.iloc[-1,3]*1/100*present_price
                    else:
                        holdC0.iloc[0,3] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)
                        holdC0.iloc[0,4] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)*10
                holdC = holdC.append(holdC0,ignore_index=True)
                
            if buy_empty_signal5[-1,:]==2:
                holdC0.iloc[0,0] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                holdC0.iloc[0,1] = -5 
                holdC0.iloc[0,2] = present_price  
                if (Asset.iloc[-1,4]/max(Asset.iloc[1:,4])>0.9) & (Asset.iloc[-1,4]/Asset0>1.07):
                    holdC0.iloc[0,3] = Asset.iloc[-1,3]*capital_distribution_coefficient
                    holdC0.iloc[0,4] = Asset.iloc[-1,3]*capital_distribution_coefficient*present_price
                else:
                    if len(buy_total)<6:
                        holdC0.iloc[0,3] = Asset.iloc[-1,3]*1/100
                        holdC0.iloc[0,4] = Asset.iloc[-1,3]*1/100*present_price
                    else:
                        holdC0.iloc[0,3] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)
                        holdC0.iloc[0,4] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)*10
                holdC = holdC.append(holdC0,ignore_index=True)
            
            if buy_empty_signal6[-1,:]==2:
                holdC0.iloc[0,0] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                holdC0.iloc[0,1] = -6 
                holdC0.iloc[0,2] = present_price  
                if (Asset.iloc[-1,4]/max(Asset.iloc[1:,4])>0.9) & (Asset.iloc[-1,4]/Asset0>1.07):
                    holdC0.iloc[0,3] = Asset.iloc[-1,3]*capital_distribution_coefficient
                    holdC0.iloc[0,4] = Asset.iloc[-1,3]*capital_distribution_coefficient*present_price
                else:
                    if len(buy_total)<6:
                        holdC0.iloc[0,3] = Asset.iloc[-1,3]*1/100
                        holdC0.iloc[0,4] = Asset.iloc[-1,3]*1/100*present_price
                    else:
                        holdC0.iloc[0,3] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)
                        holdC0.iloc[0,4] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)*10
                holdC = holdC.append(holdC0,ignore_index=True)
                
            if buy_empty_signal7[-1,:]==2:
                holdC0.iloc[0,0] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                holdC0.iloc[0,1] = -7 
                holdC0.iloc[0,2] = present_price  
                if (Asset.iloc[-1,4]/max(Asset.iloc[1:,4])>0.9) & (Asset.iloc[-1,4]/Asset0>1.07):
                    holdC0.iloc[0,3] = Asset.iloc[-1,3]*1/40
                    holdC0.iloc[0,4] = Asset.iloc[-1,3]*1/40*present_price
                else:
                    if len(buy_total)<6:
                        holdC0.iloc[0,3] = Asset.iloc[-1,3]*1/100
                        holdC0.iloc[0,4] = Asset.iloc[-1,3]*1/100*present_price
                    else:
                        holdC0.iloc[0,3] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)
                        holdC0.iloc[0,4] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)*10
                holdC = holdC.append(holdC0,ignore_index=True)
                
            if buy_empty_signal8[-1,:]==2:
                holdC0.iloc[0,0] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                holdC0.iloc[0,1] = -8 
                holdC0.iloc[0,2] = present_price  
                if (Asset.iloc[-1,4]/max(Asset.iloc[1:,4])>0.9) & (Asset.iloc[-1,4]/Asset0>1.07):
                    holdC0.iloc[0,3] = Asset.iloc[-1,3]*capital_distribution_coefficient
                    holdC0.iloc[0,4] = Asset.iloc[-1,3]*capital_distribution_coefficient*present_price
                else:
                    if len(buy_total)<8:
                        holdC0.iloc[0,3] = Asset.iloc[-1,3]*1/100
                        holdC0.iloc[0,4] = Asset.iloc[-1,3]*1/100*present_price
                    else:
                        holdC0.iloc[0,3] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)
                        holdC0.iloc[0,4] = np.floor((Asset.iloc[-1,3]*0)*present_price /10)*10
                holdC = holdC.append(holdC0,ignore_index=True)
                
            if holdC.empty:
                holdC = holdC.append(holdC0,ignore_index=True)
        else:# holdC.empty
            holdC = holdC.append(holdC0,ignore_index=True)
            
            
        if holdC.iloc[0,1] != 0:
            contents_buy = ['合约类型：quarter \n开仓价格：%s \n开仓数量：%s \n委托方式：%s \n开仓方式：%s \n交易时间：%s'%(holdC.iloc[i,2],round(holdC.iloc[i,4],2),'开多' if holdC.iloc[i,1]>0 else '开空',holdC.iloc[i,1],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) for i in range(len(holdC))]
            contents_buy = '\n\n'.join(contents_buy)
        else:
            contents_buy = '0开仓'
        if len(buy_total)>1:
                 checktime=pd.Series(buy_total.iloc[-1,0]).apply((lambda x: datetime.datetime.fromtimestamp(time.mktime(time.strptime(x, '%Y-%m-%d %H:%M:%S')))))[0]
                 checktime1=checktime.month*10000+checktime.day*100+checktime.hour
        else:
                 checktime1=0
                 fact_time=datetime.datetime.now()
                 fact_time1=fact_time.month*10000+fact_time.day*100+fact_time.hour   
        if (holdC.iloc[0,3]>0) and  (checktime1!=fact_time1):
            pk1 = open(root+'\\buy_total_%s.spydata'%coin,'rb')
            buy_total = pickle.load(pk1)
            pk1.close()
            pk1 = open(root+'\\buy_total1_%s.spydata'%coin,'rb')
            buy_total1 = pickle.load(pk1)
            pk1.close()
            buy_total = buy_total.append( holdC,ignore_index=True)
            buy_total.index = range(len(buy_total))
            pk1 = open(root+'\\buy_total_%s.spydata'%coin,'wb')
            pickle.dump(buy_total,pk1)
            pk1.close()
            buy_total1 = buy_total1.append( holdC,ignore_index=True)
            pk1 = open(root+'\\buy_total1_%s.spydata'%coin,'wb')
            pickle.dump(buy_total1,pk1)
            pk1.close()
        print('\t 资金分配计算 结束 %s \n' %time.ctime())
        
        
        '''开仓'''
        time11 = datetime.datetime.now()
        numtime = time11.minute
        numtime1 = time11.minute*60+time11.second
        can_buy2 = pd.DataFrame(np.zeros([1,6])) #合约类型,委托价格,委托数量,订单类型，开仓方式
        if holdC.iloc[0,3] != 0 and (numtime1>0) and (numtime<15):
            #can_buy2 = pd.DataFrame([['eth_usd','quarter',holdC.iloc[i,2]*1.02 if holdC.iloc[i,1]>0 else holdC.iloc[i,2]*0.98,np.floor(holdC.iloc[i,2]*holdC.iloc[i,3]/1),1 if holdC.iloc[i,1]>0 else 2,holdC.iloc[i,1] ] for i in range(len(holdC))])
            while(1):
                try:
                    high_price_limit = okcoinFuture.future_price_limit('eth_usd','quarter').get('high')
                    break
                except:
                    print('\t 获取最高限价超时')
                    time.sleep(1)
                    continue
        
            while(1):
                try:
                    low_price_limit = okcoinFuture.future_price_limit('eth_usd','quarter').get('low')
                    break
                except:
                    print('\t 获取最低限价超时')
                    time.sleep(1)
                    continue
            can_buy2 = pd.DataFrame([['eth_usd','quarter',min(holdC.iloc[i,2]*1.02,high_price_limit*0.995) if holdC.iloc[i,1]>0 else max(holdC.iloc[i,2]*0.98,low_price_limit*1.005),np.floor(holdC.iloc[i,2]*holdC.iloc[i,3]/1),1 if holdC.iloc[i,1]>0 else 2,holdC.iloc[i,1] ] for i in range(len(holdC))])

            if np.floor(holdC.iloc[0,2]*holdC.iloc[0,3]/1)>=500: # 分批开仓  
                can_buy2 = pd.DataFrame(np.tile( can_buy2,[5,1]))#分5次下单
                can_buy2.iloc[:-len(holdC),3] = pd.DataFrame([np.floor(can_buy2.iloc[i,3]*0.2) for i in range(len(can_buy2)-len(holdC))]).iloc[:,0]
                can_buy2.iloc[-len(holdC):,3] = can_buy2.values[-len(holdC):,3]-can_buy2.values[-len(holdC)*2:-len(holdC),3]*4
            
                for i in range(len(can_buy2)): 
                    while(1):
                        try:
                            high_price_limit = okcoinFuture.future_price_limit('eth_usd','quarter').get('high')
                            break
                        except:
                            print('\t 获取最高限价超时')
                            time.sleep(1)
                            continue
        
                    while(1):
                        try:
                            low_price_limit = okcoinFuture.future_price_limit('eth_usd','quarter').get('low')
                            break
                        except:
                            print('\t 获取最低限价超时')
                            time.sleep(1)
                            continue
                    while(1):
                        try:
                            present_price = float(okcoinFuture.future_ticker('eth_usd','quarter').get('ticker').get('last'))
                            break
                        except:
                            time.sleep(1)
                            print('\t 获取合约现价超时')
                            continue
                    present_price_margin_empty_buy = max(present_price*0.98,low_price_limit*1.005)
                    present_price_margin_much_buy = min(present_price*1.02,high_price_limit*0.995)
                    can_buy2.iloc[:,2] = [present_price_margin_much_buy if i>0 else present_price_margin_empty_buy for i in can_buy2.iloc[:,5]]
                    while(1):
                        try:
                            depth=okcoinFuture.future_depth('eth_usd','quarter','10')
                            break
                        except:
                            time.sleep(1)
                            print('获取深度信息超时')
                            continue
                    asks=depth.get('asks')
                    asks_amount_sum=sum([asks[i][1] for i in range(len(asks))])
                    bids=depth.get('bids')
                    bids_amount_sum=sum([bids[i][1] for i in range(len(bids))])
                    if (can_buy2.iloc[i,5]>0) & (asks_amount_sum>can_buy2.iloc[i,3]*3):
                            time.sleep(0.1)
                            
                    elif (can_buy2.iloc[i,5]<0) & (bids_amount_sum>can_buy2.iloc[i,3]*3):
                         time.sleep(0.1)
                        
                    else:
                         time.sleep(3)
                    a11=1
                    while(1):
                        try:
                            if run_tate==1:
                                SendOrder_buy = okcoinFuture.future_trade(can_buy2.iloc[i,0],str(can_buy2.iloc[i,1]),str(can_buy2.iloc[i,2]),str(can_buy2.iloc[i,3]),str(int(can_buy2.iloc[i,4])),'0','10')#访问频率 5次/1秒(按币种单独计算)
                                assert json.loads(SendOrder_buy).get('result')==True
                            print('\t 第%s次开仓完毕'%i)
                            time.sleep(5)
                            break
                        except:
                            a11+=1
                            time.sleep(1)
                            print('\t 分批下单超时')
                            if a11<30:
                              continue
                            else:
                                break
                            
            elif np.floor(holdC.iloc[0,2]*holdC.iloc[0,3]/1)<500: # 一次性开仓
                for i in range(len(can_buy2)):
                    while(1):
                        try:
                            high_price_limit = okcoinFuture.future_price_limit('eth_usd','quarter').get('high')
                            break
                        except:
                            print('\t 获取最高限价超时')
                            time.sleep(1)
                            continue
        
                    while(1):
                        try:
                            low_price_limit = okcoinFuture.future_price_limit('eth_usd','quarter').get('low')
                            break
                        except:
                            print('\t 获取最低限价超时')
                            time.sleep(1)
                            continue
                        
                    while(1):
                        try:
                            present_price = float(okcoinFuture.future_ticker('eth_usd','quarter').get('ticker').get('last'))
                            break
                        except:
                            time.sleep(1)
                            print('\t 获取合约现价超时')
                            continue
                    present_price_margin_empty_buy = max(present_price*0.98,low_price_limit*1.005)
                    present_price_margin_much_buy = min(present_price*1.02,high_price_limit*0.995)
                    can_buy2.iloc[:,2] = [present_price_margin_much_buy if i>0 else present_price_margin_empty_buy for i in can_buy2.iloc[:,5]]
                    while(1):
                        try:
                            depth = okcoinFuture.future_depth('eth_usd','quarter','10')
                            break
                        except:
                            time.sleep(1)
                            print('获取深度信息超时')
                            continue
                    asks = depth.get('asks')
                    asks_amount_sum = sum([asks[i][1] for i in range(len(asks))])
                    bids = depth.get('bids')
                    bids_amount_sum = sum([bids[i][1] for i in range(len(bids))])
                    if (can_buy2.iloc[i,5]>0) & (asks_amount_sum>can_buy2.iloc[i,3]*3):
                        time.sleep(0.1)
                    elif (can_buy2.iloc[i,5]<0) & (bids_amount_sum>can_buy2.iloc[i,3]*3):
                        time.sleep(0.1)
                    else:
                        time.sleep(3)
                    a11=1
                    while(1):
                        try:
                            if run_tate==1:
                                SendOrder_buy = okcoinFuture.future_trade(can_buy2.iloc[i,0],str(can_buy2.iloc[i,1]),str(can_buy2.iloc[i,2]),str(can_buy2.iloc[i,3]),str(int(can_buy2.iloc[i,4])),'0','10')#访问频率 5次/1秒(按币种单独计算)
                                assert json.loads(SendOrder_buy).get('result')==True
                            break
                        except:
                            a11+=1
                            print('\t 一次性开仓超时')
                            time.sleep(1)
                            if a11<30:
                                continue
                            else:
                                break
                    
                print('\t 第%s次开仓完毕'%0)#print('\t 第%s次开仓完毕'%i)
           
        
    '''获取资金数据'''
    time13 = datetime.datetime.now()
    numtime13 = time13.minute
    if ((numtime13>4) and (numtime13<14) and (p3==1)) | (len(can_sell_market_loss_present)>0):
        p3=2
        if len(can_sell_market_loss_present)>0:
            p3=1
        print('\t 收集资金数据 开始 %s' %time.ctime())
        while(1):
            try:
                time.sleep(1)
                exchange_rate = okcoinFuture.exchange_rate().get('rate')#美元人民币汇率
                break
            except:
                print('\t 汇率获取超时')
                time.sleep(1)
                continue
            
        while(1):
            try:
                time.sleep(1)
                f_index_btc = okcoinFuture.future_index('btc_usdt').get('future_index') #OKEx合约指数 btc
                break
            except:
                print('\t 获取btc指数超时')
                time.sleep(2)
                continue
              
        while(1):
            try:
                time.sleep(1)
                f_index_etc = okcoinFuture.future_index('etc_usdt').get('future_index') #OKEx合约指数 btc
                break
            except:
                print('\t 获取etc指数超时')
                time.sleep(2)
                continue
                      
        while(1):
            try:
                time.sleep(1)
                f_index_ltc = okcoinFuture.future_index('ltc_usdt').get('future_index') #OKEx合约指数 btc
                break
            except:
                print('\t 获取ltc指数超时')
                time.sleep(2)
                continue
            
        while(1):
            try:
                time.sleep(1)
                f_index_bch = okcoinFuture.future_index('bch_usdt').get('future_index') #OKEx合约指数 btc
                break
            except:
                print('\t 获取bch指数超时')
                time.sleep(2)
                continue
            
        while(1):
            try:
                time.sleep(1)
                f_index_eth = okcoinFuture.future_index('eth_usdt').get('future_index') #OKEx合约指数 btc
                break
            except:
                print('\t 获取eth指数超时')
                time.sleep(2)
                continue
            
        while(1):
            try:
                time.sleep(1)
                f_index_eos = okcoinFuture.future_index('eos_usdt').get('future_index') #OKEx合约指数 btc
                break
            except:
                print('\t 获取eos指数超时')
                time.sleep(2)
                continue
            
        '''合约账户'''
        while(1):
            try:
                time.sleep(1)
                capital1 = json.loads(okcoinFuture.future_userinfo())
                rights_btc = capital1.get('info').get('btc').get('account_rights') #账户权益 etc数量
                rights_etc = capital1.get('info').get('etc').get('account_rights') #账户权益 etc数量
                rights_ltc = capital1.get('info').get('ltc').get('account_rights')
                rights_eth = capital1.get('info').get('eth').get('account_rights')
                rights_eos = capital1.get('info').get('eos').get('account_rights')
                rights = rights_etc*f_index_etc+rights_btc*f_index_btc+rights_ltc*f_index_ltc+rights_eth*f_index_eth+rights_eos*f_index_eos#合约账户各个币的总资金
                break
            except:
                print('\t 获取合约用户信息超时')
                time.sleep(2)
                continue
            
        '''币币账户'''   
        while(1):
            try:
                userinfo = json.loads(okcoinSpot.userinfo())
                usdt_free = userinfo.get('info').get('funds').get('free').get('usdt')#free:账户余额
                usdt_freezed = userinfo.get('info').get('funds').get('freezed').get('usdt')#freezed:账户冻结余额
                etc_free = userinfo.get('info').get('funds').get('free').get('etc')#free:账户余额
                etc_freezed = userinfo.get('info').get('funds').get('freezed').get('etc')#freezed:账户冻结余额
                btc_free = userinfo.get('info').get('funds').get('free').get('btc')#free:账户余额
                btc_freezed = userinfo.get('info').get('funds').get('freezed').get('btc')#freezed:账户冻结余额
                ltc_free = userinfo.get('info').get('funds').get('free').get('ltc')#free:账户余额
                ltc_freezed = userinfo.get('info').get('funds').get('freezed').get('ltc')#freezed:账户冻结余额
                eth_free = userinfo.get('info').get('funds').get('free').get('eth')#free:账户余额
                eth_freezed = userinfo.get('info').get('funds').get('freezed').get('eth')#freezed:账户冻结余额
                eos_free = userinfo.get('info').get('funds').get('free').get('eos')#free:账户余额
                eos_freezed = userinfo.get('info').get('funds').get('freezed').get('eos')#freezed:账户冻结余额
                rights1 = float(usdt_free)+float(usdt_freezed)+(float(etc_free)+float(etc_freezed))*f_index_etc+(float(btc_free)+float(btc_freezed))*f_index_btc+(float(ltc_free)+float(ltc_freezed))*f_index_ltc+(float(eth_free)+float(eth_freezed))*f_index_eth+(float(eos_free)+float(eos_freezed))*f_index_eos
                break
            except:
                print('\t 获取币币账户超时')
                time.sleep(2)
                continue
      
        
        '''我的钱包'''
        while(1):
            try:
                wallet = json.loads(okcoinSpot.wallet_info())
                usdt_free = wallet.get('info').get('funds').get('free').get('usdt')#free:账户余额
                usdt_holds = wallet.get('info').get('funds').get('holds').get('usdt')#holds:账户锁定余额
                etc_free = wallet.get('info').get('funds').get('free').get('etc')
                etc_holds = wallet.get('info').get('funds').get('holds').get('etc')
                btc_free = wallet.get('info').get('funds').get('free').get('btc')
                btc_holds = wallet.get('info').get('funds').get('holds').get('btc')
                ltc_free = wallet.get('info').get('funds').get('free').get('ltc')
                ltc_holds = wallet.get('info').get('funds').get('holds').get('ltc')
                eth_free = wallet.get('info').get('funds').get('free').get('eth')
                eth_holds = wallet.get('info').get('funds').get('holds').get('eth')
                eos_free = wallet.get('info').get('funds').get('free').get('eos')
                eos_holds = wallet.get('info').get('funds').get('holds').get('eos')
                rights2 = float(usdt_free)+float(usdt_holds)+(float(etc_free)+float(etc_holds))*f_index_etc+(float(btc_free)+float(btc_holds))*f_index_btc+(float(ltc_free)+float(ltc_holds))*f_index_ltc+(float(eth_free)+float(eth_holds))*f_index_eth+(float(eos_free)+float(eos_holds))*f_index_eos
                break
            except:
                print('\t 获取钱包超时')
                time.sleep(2)
                continue
    
        #各个账户的数字货币换算为美元的总金额
        right_fabi = 0
        #rights2=19661
        rights_all = rights+rights1+rights2+ right_fabi
        keep_deposit = capital1.get('info').get('eth').get('keep_deposit') #保证金
        profit_real = capital1.get('info').get('eth').get('profit_real') #已实现盈亏
        profit_unreal = capital1.get('info').get('eth').get('profit_unreal') #未实现盈亏
        risk_rate = capital1.get('info').get('eth').get('risk_rate') #保证金率
        balance = rights_all/f_index_eth+profit_real+profit_unreal-keep_deposit #账户余额 etc数量   可用
        BeijingTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # 北京时间
        capital = pd.DataFrame(np.zeros([1,7])) #"日期","总资产(币)","合约价值(保证金.币)","可用资金(币)","总资产（美元）","指数(币)","汇率"
        capital.iloc[0,:] = BeijingTime,rights_all/f_index_eth,keep_deposit,balance,rights_all,f_index_eth,exchange_rate
        capital_change_total = pickle.load(open(root+'\\capital_change_total_%s.spydata'%coin,'rb'))
        if BeijingTime[:13]==capital_change_total.iloc[-1,0][:13]:#防止重复收集
            capital_change_total.values[-1,:] = capital#pd.Series(capital)
        else:
            capital_change_total = capital_change_total.append(capital,ignore_index=True)
        pk1=open(root+'\\capital_change_total_%s.spydata'%coin,'wb')
        pickle.dump(capital_change_total,pk1)
        pk1.close()
        pk1=open(root+'\\capital_change_total1_%s.spydata'%coin,'wb')#备份
        pickle.dump(capital_change_total,pk1)
        pk1.close()
        print('\t 收集资金数据 结束 %s \n' %time.ctime())
        f = open(root+'\\buy_total_%s.spydata'%coin,'rb')#open('C:/Data_P1/buy_total_%s.spydata'%coin,'rb')
        buy_total = pickle.load(f)
        f.close()
        
        while(1):
            try:
                position_amount = json.loads(okcoinFuture.future_position('eth_usd','quarter'))
                if len(position_amount.get('holding'))>0:
                    buy_amount = position_amount.get('holding')[0].get('buy_amount')
                    sell_amount = position_amount.get('holding')[0].get('sell_amount')
                else:
                    buy_amount = 0
                    sell_amount = 0
                break
            except:
                time.sleep(1)
                continue
        '''        
        while(1):
            try:
                position_amount = json.loads(okcoinFuture.future_position('eth_usd','quarter'))
                buy_amount = position_amount.get('holding')[0].get('buy_amount')
                sell_amount = position_amount.get('holding')[0].get('sell_amount')
                break
            except:
                time.sleep(1)
                continue'''
            
        logic_buy_id = list(np.where(buy_total.iloc[1:,1]>0)[0]+1)
        logic_buy_id = [int(i) for i in logic_buy_id]
        logic_buy = int(buy_total.iloc[logic_buy_id,4].sum())
        logic_sell_id = list(np.where(buy_total.iloc[1:,1]<0)[0]+1)
        logic_sell_id = [int(i) for i in logic_sell_id]
        logic_sell = int(buy_total.iloc[logic_sell_id,4].sum())+hedge_fund#1100为套保数
        hold_cmp = ['实际持有多单张数：%s \n理论应该持有多单张数：%s \n实际持有空单张数：%s \n理论应该持有空单张数：%s \n套保张数：%s'%(buy_amount,logic_buy,sell_amount,logic_sell,hedge_fund) ]
        hold_cmp = '\n\n'.join(hold_cmp)
        delta_buy = buy_amount-logic_buy
        #delta_sell = sell_amount-logic_sell-hedge_fund#1100为套保张数，每个账号不一样
        delta_sell = sell_amount-logic_sell#1100为套保张数，每个账号不一样
        '''
        if delta_buy>5:
            while(1):
                try:
                    high_price_limit = okcoinFuture.future_price_limit('eth_usd','quarter').get('high')
                    break
                except:
                    print('\t 获取最高限价超时')
                    time.sleep(1)
                    continue

            while(1):
                try:
                    low_price_limit = okcoinFuture.future_price_limit('eth_usd','quarter').get('low')
                    break
                except:
                    print('\t 获取最低限价超时')
                    time.sleep(1)
                    continue
            
            while(1):
                try:
                    present_price = float(okcoinFuture.future_ticker('eth_usd','quarter').get('ticker').get('last'))
                    break
                except:
                    time.sleep(1)
                    print('\t 获取合约现价超时')
                    continue
                
            present_price_margin_much_sell = max(present_price*0.98,low_price_limit*1.005)
            present_price_margin_empty_sell = min(present_price*1.02,high_price_limit*0.995)
                
            a11=1          
            while(1):
                try:
                    if run_tate==1:
                        SendOrder_sell1 = okcoinFuture.future_trade('eth_usd','quarter',present_price_margin_much_sell,str(delta_buy),str(int(3)),'0','10')#访问频率 5次/1秒(按币种单独计算)
                        assert json.loads(SendOrder_sell1).get('result')==True
                    print('\t 每组第%s次平仓完毕'%j)
                    break
                except:
                    a11+=1
                    time.sleep(1)
                    print('\t 分批下单超时')
                    if a11<10:
                        continue
                    else:
                        break
                    
                 
        if delta_sell>50:
            while(1):
                try:
                    high_price_limit = okcoinFuture.future_price_limit('eth_usd','quarter').get('high')
                    break
                except:
                    print('\t 获取最高限价超时')
                    time.sleep(1)
                    continue

            while(1):
                try:
                    low_price_limit = okcoinFuture.future_price_limit('eth_usd','quarter').get('low')
                    break
                except:
                    print('\t 获取最低限价超时')
                    time.sleep(1)
                    continue
            
            while(1):
                try:
                    present_price = float(okcoinFuture.future_ticker('eth_usd','quarter').get('ticker').get('last'))
                    break
                except:
                    time.sleep(1)
                    print('\t 获取合约现价超时')
                    continue
                
            present_price_margin_much_sell = max(present_price*0.98,low_price_limit*1.005)
            present_price_margin_empty_sell = min(present_price*1.02,high_price_limit*0.995)
                
            a11=1           
            while(1):
                try:
                    if run_tate==1:
                        SendOrder_sell2 = okcoinFuture.future_trade('eth_usd','quarter',present_price_margin_empty_sell,str(delta_sell),str(int(4)),'0','10')#访问频率 5次/1秒(按币种单独计算)
                        assert json.loads(SendOrder_sell2).get('result')==True
                    print('\t 每组第%s次平仓完毕'%j)
                    break
                except:
                    a11+=1
                    time.sleep(1)
                    print('\t 分批下单超时')
                    if a11<10:
                        continue
                    else:
                        break'''
              
                
        '''SendEmails'''
        import yagmail,time
        #yag = yagmail.SMTP(user = 'xxxxxxxx@qq.com',password = pass1+word1,host = 'smtp.qq.com')
        yag = yagmail.SMTP(user,password,host = 'smtp.qq.com')
        try:
            contents_buy
        except:
            contents_buy = '0开仓'
        contents = contents_buy + '\n\n' + contents_sell+ '\n\n' + hold_cmp #a=contents_buy +'\n\n'+ contents_sell
        subject = '%s_eth 1h交易提醒'%account_name#主题
        #to = ['yyyyyyy@qq.com']
        while(1):
            try:
                yag.send(to,subject,contents)
                break
            except:
                print('发送短信超时')
                continue
        contents_buy = '0开仓'
        contents_sell = '0平仓'
