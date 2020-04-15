#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 12:54:15 2019

@author: xuan
"""

import numpy as np
import math
from statistics import mean
arr=np.genfromtxt('adj_close_hist.csv',delimiter=',')
arr=arr[1:,1:] #price array
for i in range(1,len(arr)):
    for j in range(len(arr[0])):
        if math.isnan(arr[i][j]):
            arr[i][j]=arr[i-1][j] #fill missing values with previous price
            
#short term strategies
p1=np.zeros((len(arr),len(arr[0]))) #position array
funds1=list([1000000]*8)  #suppose the initial fund for each stock is 1m
turn1=[0]*8
hold1=[0 for i in range(8)]
r1=[[] for i in range(8)]
for j in range(len(arr[0])):
    for i in range(4,len(arr)):        
        if p1[i][j]>0:
            temp=p1[i][j]*arr[i][j]/funds1[j]-1
            r1[j].append(temp)
        if i < len(arr)-1:
            s = 0
            for k in range(5):
                s += arr[i-k][j]
            sma=s/5
        
            if arr[i][j]>=sma:
                if p1[i][j]==0: 
                    p1[i+1][j]=math.floor(funds1[j]/arr[i][j])
                else:
                    p1[i+1][j] = p1[i][j] #if price>sma, hold
                    funds1[j]=p1[i][j]*arr[i][j]
                hold1[j] += 1
            else:
                p1[i+1][j] = 0 # if price<sma, sell all shares of that stock
                if p1[i][j]>0:
                    turn1[j] += 1
                    funds1[j]=p1[i][j]*arr[i][j]
                    
avg_hold1=[hold1[i]/(len(arr)/252) for i in range(8)]
avg_turn1=[turn1[i]/(len(arr)/252) for i in range(8)]
annual_r1=[mean(r1[i])*252 for i in range(8)]
annual_vol1=[np.std(r1[i])*252 for i in range(8)]

        
#medium term
p2=np.zeros((len(arr),len(arr[0]))) 
funds2=list([1000000]*8)
turn2=list([0]*8)
hold2=list([0]*8)
r2=[[] for i in range(8)]
for j in range(len(arr[0])):
    for i in range(49,len(arr)):
        if p2[i][j]>0:
            temp=p2[i][j]*arr[i][j]/funds2[j]-1
            r2[j].append(temp)
        if i<len(arr)-1:
            s15 = 0
            for k in range(0,15):
                s15 += arr[i-k][j]
            sma15=s15/15
            s50 = 0
            for k in range(0,50):
                s50 += arr[i-k][j]
            sma50=s50/50
        
            if sma15>=sma50: 
                if p2[i][j]==0: 
                    p2[i+1][j]=math.floor(funds2[j]/arr[i][j])
                else:
                    p2[i+1][j] = p2[i][j] #if sma15>sma50, hold
                    funds2[j]=p2[i][j]*arr[i][j]
                hold2[j] += 1
            else:
                p2[i+1][j] = 0 # if sma15<sma50, sell all shares of that stock
                if p2[i][j]>0:
                    turn2[j] += 1
                    funds2[j]=p2[i][j]*arr[i][j]
avg_hold2=[hold2[i]/(len(arr)/252) for i in range(8)]
avg_turn2=[turn2[i]/(len(arr)/252) for i in range(8)]
annual_r2=[mean(r2[i])*252 for i in range(8)]
annual_vol2=[np.std(r2[i])*252 for i in range(8)]



#long term
p3=np.zeros((len(arr),len(arr[0]))) 
funds3=list([1000000]*8)
turn3=list([0]*8)
hold3=list([0]*8)
r3=[[] for i in range(8)]

for j in range(len(arr[0])):
    for i in range(199,len(arr)):
        if p3[i][j]>0:
            temp=p3[i][j]*arr[i][j]/funds3[j]-1
            r3[j].append(temp)
        if i<len(arr)-1:
            s200 = 0
            for k in range(0,200):
                s200 += arr[i-k][j]
            sma200=s200/200
            s50 = 0
            for k in range(0,50):
                s50 += arr[i-k][j]
            sma50=s50/50
        
            if sma50>=sma200: 
                if p3[i][j]==0: 
                    p3[i+1][j]=math.floor(funds3[j]/arr[i][j])
                else:
                    p3[i+1][j] = p3[i][j] #if sma50>sma200, hold
                    funds3[j]=p3[i][j]*arr[i][j]
                hold3[j] += 1
            else:
                p3[i+1][j] = 0 # if sma50<sma200, sell all shares of that stock
                if p3[i][j]>0:
                    turn3[j] += 1
                    funds3[j]=p3[i][j]*arr[i][j]
    
avg_hold3=[hold3[i]/(len(arr)/252) for i in range(8)]
avg_turn3=[turn3[i]/(len(arr)/252) for i in range(8)]
annual_r3=[mean(r3[i])*252 for i in range(8)]
annual_vol3=[np.std(r3[i])*252 for i in range(8)]


fh=open('output.txt','w')
fh.write("short term:\n")
s='Average position turn-over per annum per stock:\n{}\n\nAverage position holding\
 period per annum per stock:\n{}\n\nAverage annualized return per stock:\n{}\
 \n\nAverage annualized return volatility per stock:\n{}'.format(avg_turn1,avg_hold1,annual_r1,annual_vol1)
fh.write(s)

fh.write("\n\n\nmedium term:\n")
s='Average position turn-over per annum per stock:\n{}\n\nAverage position holding\
 period per annum per stock:\n{}\n\nAverage annualized return per stock:\n{}\
 \n\nAverage annualized return volatility per stock:\n{}'.format(avg_turn2,avg_hold2,annual_r2,annual_vol2)
fh.write(s)
fh.write("\n\n\nlong term:\n")
s='Average position turn-over per annum per stock:\n{}\n\nAverage position holding\
 period per annum per stock:\n{}\n\nAverage annualized return per stock:\n{}\
 \n\nAverage annualized return volatility per stock:\n{}'.format(avg_turn3,avg_hold3,annual_r3,annual_vol3)
fh.write(s)
fh.close()














