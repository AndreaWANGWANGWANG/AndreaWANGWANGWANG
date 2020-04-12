#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 08:58:52 2019

@author: xuan
"""


import math
class EquityOption:
    RiskfreeRate=0.01
    
    def __init__(self, CallFlag='C', Spot=100, Strike=100, Maturity=10, Vol=0.5, DividendYield=0, **kwargs):
        self.CallFlag=CallFlag
        self.Spot=Spot
        self.Strike=Strike
        self.Maturity=Maturity
        self.Vol=Vol
        self.DividendYield=DividendYield
        for i in kwargs.keys():
            self.__dict__[i] = kwargs[i]
            
    @classmethod   
    def setRiskfreeRate(cls,Rfr):
        EquityOption.RiskfreeRate = Rfr
        
    @staticmethod
    def N(x):
        return 0.5*(1+math.erf(x/math.sqrt(2)))
    
    def d1(self):
        return (math.log(self.Spot/self.Strike,math.e)+(EquityOption.RiskfreeRate-\
            self.DividendYield+self.Vol**2/2)*self.Maturity)/(self.Vol*math.sqrt(self.Maturity))
        
    def d2(self):
        return self.d1()-self.Vol*math.sqrt(self.Maturity)
    
    def BS(self):
        return self.Spot*math.e**(-self.DividendYield*self.Maturity)\
        *EquityOption.N(self.d1())-self.Strike*math.e**(-self.RiskfreeRate*self.Maturity)*EquityOption.N(self.d2()) \
        if self.CallFlag=='C' else self.Strike*math.e**(-self.RiskfreeRate*\
        self.Maturity)*EquityOption.N(-self.d2())-self.Spot*math.e**\
        (-self.DividendYield*self.Maturity)*EquityOption.N(-self.d1())
        
    def __str__(self):
        return 'Risk-free Rate: {}\nOption Type: {}\nSpot Price: {}\nStrike: {}\nMaturity: {}\
    \nVolatility: {}\nDividend Yield: {}\nDelta: {}\nGamma: {}\nVega: {}\
    \nTheta: {}\nOption Price: {}'.format(self.RiskfreeRate,self.CallFlag, self.Spot, \
    self.Strike,self.Maturity,self.Vol,self.DividendYield,self.Delta(),self.Gamma(),\
    self.Vega(),self.Theta(),self.BS())
    
    def __imul__(self, stock_split):
        self.Spot /=stock_split
        self.Strike /=stock_split
     
    def Delta(self):
        return math.e**(-self.DividendYield*self.Maturity)*EquityOption.N(self.d1()) if self.CallFlag=='C'\
               else math.e**(-self.DividendYield*self.Maturity)*(self.N(self.d1())-1)
               
    def Gamma(self):
        return math.e**(-self.DividendYield*self.Maturity)/(self.Spot*self.Vol\
               *math.sqrt(self.Maturity))*1/(math.sqrt(2*math.pi))*math.e**\
                       (-self.d1()*self.d1()/2)
                       
    def Vega(self):
        return self.Spot*math.e**(-self.DividendYield*self.Maturity)\
               *math.sqrt(self.Maturity)*1/(math.sqrt(2*math.pi))*math.e**\
                       (-self.d1()*self.d1()/2)
                       
    def Theta(self):
        return 1/365*(-(self.Spot*self.Vol*math.e**(-self.DividendYield*\
               self.Maturity)/(2*math.sqrt(self.Maturity))*1/math.sqrt(2*math.pi)\
               *math.e**(-self.d1()*self.d1()/2))-self.RiskfreeRate*self.Strike\
               *math.e**(-self.RiskfreeRate*self.Maturity)*self.N(self.d2())+\
               self.DividendYield*self.Spot*math.e**(-self.DividendYield*self.Maturity)\
               *self.N(self.d1())) if self.CallFlag=='C' else \
               1/365*(-(self.Spot*self.Vol*math.e**(-self.DividendYield*\
               self.Maturity)/(2*math.sqrt(self.Maturity))*1/math.sqrt(2*math.pi)\
               *math.e**(-self.d1()*self.d1()/2))+self.RiskfreeRate*self.Strike\
               *math.e**(-self.RiskfreeRate*self.Maturity)*self.N(-self.d2())-\
               self.DividendYield*self.Spot*math.e**(-self.DividendYield*self.Maturity)\
               *self.N(-self.d1()))
    def Bisect(self,op,a,b):
        KeepVol=self.Vol
        self.Vol=a
        BSa=self.BS()
        self.Vol=b
        BSb=self.BS()
        if BSa-op==0: return a
        elif BSb-op==0: return b
        elif (BSa-op)*(BSb-op)>0 : return 'Implied volatility is not in [a,b].'
        else:
            while 1:
                self.Vol=a
                BSa=self.BS()
                self.Vol=b
                BSb=self.BS()
                c=(a+b)/2
                self.Vol=c
                BSc=self.BS()
                if abs(c-a)<=0.0001: break
                elif (BSa-op)*(BSc-op)<0: 
                    b=c
                else:
                    a=c
        self.Vol=KeepVol #reset Vol
        return c

    
    def NewtonRaphson(self,op,x0):
        KeepVol=self.Vol
        for i in range(1000):
            self.Vol=x0
            h=op-self.BS()
            if (abs(h)<=0.0001):
                return x0
            x0=x0+h/self.Vega()
        self.Vol=KeepVol


        
    
test=EquityOption()
fhandle = open('Option_Output','w')
s='Risk-free Rate: {}\nOption Type: {}\nSpot Price: {}\nStrike: {}\nMaturity: {}\
    \nVolatility: {}\nDividend Yield: {}\nDelta: {}\nGamma: {}\nVega: {}\
    \nTheta: {}\nOption Price: {}\n'.format(test.RiskfreeRate,test.CallFlag, test.Spot, \
    test.Strike,test.Maturity,test.Vol,test.DividendYield,test.Delta(),test.Gamma(),\
    test.Vega(),test.Theta(),test.BS())
fhandle.write(s)
bi=test.Bisect(op=59.2104,a=0.42,b=0.6)
ne=test.NewtonRaphson(op=59.2104,x0=0.6)
fhandle.write('Implied Volatility(Market Price = 59.2104)\nBisect: {}\
              \nNewton-Raphson: {}'.format(bi,ne))
fhandle.close()






























