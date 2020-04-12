#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 09:31:11 2019

@author: xuan
"""

#Q1
import datetime as dt
ls=list()
for m in range(3,13):
    fst=dt.date(2019,m,1) #the first day of each month
    temp=fst 
    wkd=temp.isoweekday()
    while wkd != 5:
        temp=temp + dt.timedelta(1)
        wkd=temp.isoweekday()
    
    ex=temp + dt.timedelta(14)
    ls.append(ex)
ls

TtoM=list()
for i in ls:
    TtoM.append((i-dt.date.today())/dt.timedelta(365))

print('Time to maturity:')
for i in range(3,13):
    print('Month',i,'option:',TtoM[i-3])

    
#Q2
import csv
import datetime as dt
from collections import defaultdict
fhandle = open('stockPx.csv')
stockfile=csv.DictReader(fhandle)
stocklist=stockfile.fieldnames[1:]

M=defaultdict(float)
m=defaultdict(float)
Mdate=defaultdict(list)
mdate=defaultdict(list)
datediff=defaultdict(list)
count=0
for i in stockfile:
    i['date']=dt.datetime.strptime(i['date'],"%m/%d/%Y")
    for stock in stocklist:
        if count==0:
            M[stock]=float(i[stock])
            m[stock]=float(i[stock])
            Mdate[stock]=i['date']
            mdate[stock]=i['date']
            continue
        else:
            if float(i[stock])>M[stock]:
                M[stock]=float(i[stock])
                Mdate[stock]=i['date']
            if float(i[stock])<m[stock]:
                m[stock]=float(i[stock])
                mdate[stock]=i['date']
    count +=1

for stock in stocklist:
    datediff[stock]=Mdate[stock]-mdate[stock]
    print(stock,'max P date:', M[stock],dt.datetime.strftime(Mdate[stock],'%Y/%m/%d'))
    print(stock,'min P date:', m[stock],dt.datetime.strftime(mdate[stock],'%Y/%m/%d'))
    print(stock,'date_diff:',datediff[stock],'\n')
fhandle.close()

#giving the same seed to make sure the difference comes from shift rather than randomness in montecalor

#Q3

import random
import math

S0, tau, vol, r, d = 100, 0.5, 0.5, 0, 0
mu, sigma, disc = (r-d-0.5*vol*vol)*tau, vol*math.sqrt(tau), math.exp(-r*tau)
random.seed(1)
stock_prices = [S0*random.lognormvariate(mu,sigma) for i in range(1000000)]

def op_payoff(flag='C',K=100):
    if flag=='C':
        return lambda S: max(S-K,0)
    else:
        return lambda S: max(K-S,0)
    
import statistics
c100=statistics.mean(map(op_payoff(flag='C',K=100),stock_prices))*disc
p100=statistics.mean(map(op_payoff(flag='P',K=100),stock_prices))*disc
c110=statistics.mean(map(op_payoff(flag='C',K=110),stock_prices))*disc
p90=statistics.mean(map(op_payoff(flag='P',K=90),stock_prices))*disc

import EquityOption as EQ
c100_BS=EQ.EquityOption(CallFlag='C', Spot=S0, Strike=100, Maturity=tau, Vol=vol, DividendYield=d,RiskfreeRate=r)
p100_BS=EQ.EquityOption(CallFlag='P', Spot=S0, Strike=100, Maturity=tau, Vol=vol, DividendYield=d,RiskfreeRate=r)
c110_BS=EQ.EquityOption(CallFlag='C', Spot=S0, Strike=110, Maturity=tau, Vol=vol, DividendYield=d,RiskfreeRate=r)
p90_BS=EQ.EquityOption(CallFlag='P', Spot=S0, Strike=90, Maturity=tau, Vol=vol, DividendYield=d,RiskfreeRate=r)


S0,vol=101, 0.5
mu, sigma, disc = (r-d-0.5*vol*vol)*tau, vol*math.sqrt(tau), math.exp(-r*tau)
random.seed(1)
stock_prices = [S0*random.lognormvariate(mu,sigma) for i in range(1000000)]
c2=statistics.mean(map(op_payoff(flag='C',K=100),stock_prices))*disc
del_c100=c2-c100
p2=statistics.mean(map(op_payoff(flag='P',K=100),stock_prices))*disc
del_p100=p2-p100
c110_2=statistics.mean(map(op_payoff(flag='C',K=110),stock_prices))*disc
del_c110=c110_2-c110
p90_2=statistics.mean(map(op_payoff(flag='P',K=90),stock_prices))*disc
del_p90=p90_2-p90


S0, vol=102, 0.5
mu, sigma, disc = (r-d-0.5*vol*vol)*tau, vol*math.sqrt(tau), math.exp(-r*tau)
random.seed(1)
stock_prices = [S0*random.lognormvariate(mu,sigma) for i in range(1000000)]
c100_s102=statistics.mean(map(op_payoff(flag='C',K=100),stock_prices))*disc
ga_c100=(c100_s102-c2)-del_c100
p100_s102=statistics.mean(map(op_payoff(flag='P',K=100),stock_prices))*disc
ga_p100=(p100_s102-p2)-del_p100
c110_s102=statistics.mean(map(op_payoff(flag='C',K=110),stock_prices))*disc
ga_c110=(c110_s102-c110_2)-del_c110
p90_s102=statistics.mean(map(op_payoff(flag='P',K=90),stock_prices))*disc
ga_p90=(p90_s102-p90_2)-del_p90




S0, vol=100, 1.5
mu, sigma, disc = (r-d-0.5*vol*vol)*tau, vol*math.sqrt(tau), math.exp(-r*tau)
random.seed(1)
stock_prices = [S0*random.lognormvariate(mu,sigma) for i in range(1000000)]
c3=statistics.mean(map(op_payoff(flag='C',K=100),stock_prices))*disc
vega_c100=c3-c100
p3=statistics.mean(map(op_payoff(flag='P',K=100),stock_prices))*disc
vega_p100=p3-p100
c110_3=statistics.mean(map(op_payoff(flag='C',K=110),stock_prices))*disc
vega_c110=c110_3-c110
p90_3=statistics.mean(map(op_payoff(flag='P',K=90),stock_prices))*disc
vega_p90=p90_3-p90





print('Monte-Carlo:\nat the money call price: ',c100,'\nat the\
 money put price: ',p100,'\ncall(K=110) price: ',c110,'\nput(K=90) price: ',p90,\
 '\nat the money call delta: ',del_c100,'\nat the money put delta: ',del_p100,\
 '\ncal(K=110) delta: ',del_c110,'\nput(K=90) delta: ',del_p90,'\nat the money \
 call vega: ',vega_c100,'\nat the money put vega: ',vega_p100,'\ncall(K=110)\
 vega: ',vega_c110,'\nput(K=90) vega: ',vega_p90,'\nat the money call gamma: ',ga_c100,\
 '\nat the money put gamma: ',ga_p100,'\ncall(K=110) gamma: ',ga_c110,\
 '\nput(90) gamma: ',ga_p90)
print('\n')
print('Analytical solution:\nat the money call price: ',c100_BS.BS(),'\nat the\
 money put price: ',p100_BS.BS(),'\ncall(K=110) price: ',c110_BS.BS(),'\nput(K=90) \
 price: ',p90_BS.BS(),'\nat the money call delta: ',c100_BS.Delta(),\
 '\nat the money put delta: ',p100_BS.Delta(),'\ncall(K=110) delta: ',c110_BS.Delta(),\
 '\nput(K=90) delta: ',p90_BS.Delta(),'\nat the money call vega: ',c100_BS.Vega(),\
 '\nat the money put vega: ',p100_BS.Vega(),'\ncall(K=110) vega: ',c110_BS.Vega(),\
 '\nput(K=90) vega: ',p90_BS.Vega(),'\nat the money call gamma: ',c100_BS.Gamma(),\
 '\nat the money put gamma: ',p100_BS.Gamma(),'\ncall(K=110) gamma: ',c110_BS.Gamma(),\
 '\nput(90) gamma: ',p90_BS.Gamma())

























