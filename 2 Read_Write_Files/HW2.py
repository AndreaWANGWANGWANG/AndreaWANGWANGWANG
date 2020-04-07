#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 05:46:17 2019

@author: xuan
"""

f = open("/Users/xuan/Desktop/AAPL.csv",'r')
head=f.readline().rstrip().split(',')
records = []
while 1:
    record = f.readline().rstrip()
    if not record:
        break
    record = record.split(',')
    for i in range(2,7):
        record[i]=float(format(float(record[i]),'.2f'))
    records.append(record)
head.append('daysRange')
for i in range(len(records)):
    records[i].append(float(format(records[i][3]-records[i][4],'.2f')))

aapl_sorted = sorted(records, key= lambda x: x[7])
close_on_high = list(filter(lambda x: abs(x[3]-x[5])<=0.01,records))
low_vol_rec = list(filter(lambda x: x[7]/x[2]<=0.01,records))
low_vol_days = []
for i in range(len(low_vol_rec)):
    low_vol_days.append(low_vol_rec[i][0])
f.close()

fw=open("/Users/xuan/Desktop/output.txt",'a')
fw.write('first and last 5 records\n')
fw.write(str(aapl_sorted[0:5]))
fw.write(str(aapl_sorted[-5:]))
fw.write('\nlose_on_high\n')
fw.write(str(close_on_high))
fw.write('\nlow_vol_days\n')
fw.write(str(low_vol_days))
fw.close()














