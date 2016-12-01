#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 18:32:15 2016

@author: ZJun
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from twitter_function import Import_Obj,GenerateDate,hinton,GetPartOfTimeSeries,Sort_Dict


n=6

population_2015 = dict(zip(['Cairns','Townsville','Mackay','Sunshine Coast','Brisbane','Gold Coast'],
                           [147993,180333,85455,302122,2209453,624918]))

     
P = Sort_Dict(population_2015)
Places = [i[0] for i in P][:n]

df_where_to_where = Import_Obj('./DF_Result/df_where_to_where')
actual_days_in_week = Import_Obj('./Data/actual_days_in_week')
df_real_flu = Import_Obj('./DF_Result/df_real_flu')[Places]
df_twitter_in_place_loc = Import_Obj('./DF_Result/df_twitter_in_place_loc')[Places]




TimeRange = [pd.datetime(2015,3,9).date(),pd.datetime(2015,10,12).date()]
            

real_flu_ = GetPartOfTimeSeries(df_real_flu,TimeRange)[Places]

Times = real_flu_.index


all_where_to_where = df_where_to_where.values[0]*0 

for w2w in df_where_to_where.values:
    all_where_to_where += w2w

all_where_to_where.loc['Brisbane'] = all_where_to_where.loc['Brisbane']  # out
all_where_to_where['Brisbane'] = all_where_to_where['Brisbane']   # in 
    
twitter_all_loc = df_twitter_in_place_loc.sum()

# Model 

def Model(real_flu_,coef_dict,Times):
    Pred = np.c_[real_flu_.loc[Times[0]].values]
    for i in range(len(Times)-1):
        place_flu = []
        for place in Places:
            twitter_move_loc_all = all_where_to_where[place][Places]
            flu = pd.Series(Pred[:,i],index = Places)
            x1 = flu[place]
            x2 = sum(twitter_move_loc_all / twitter_all_loc * flu)
            y_1 = np.dot([x1,x2],coef_dict[place])   
            place_flu.append(y_1)
            
        def sigmoid(x):
            #return 0.5/(1+0.006*np.exp((len(Times)-3)-x))
            return 0.5/(1+0.006*np.exp((len(Times)-2)-x))
            
        p=sigmoid(i)
        place_flu = [a - a*p for a in place_flu] 
        Pred = np.c_[Pred,place_flu]
        
    df_Pred = pd.DataFrame(Pred.T,columns=Places,index=Times)
    df_Pred = df_Pred[Places].applymap(lambda x: int(x))
    return df_Pred



'''

a = np.arange(1,1.1,0.05)
b = np.arange(2,5)

from itertools import product
q = product(a,b,a,b,a,b,a,b,a,b,a,b)

e=10e10

for i in range(np.power(3,12)):    
    c = q.next()
    coef = [[c[0],c[1]],[c[2],c[3]],[c[4],c[5]],[c[6],c[7]],[c[8],c[9]],[c[10],c[11]]]
    coef = coef[:n]
    coef_dict = dict(zip(Places,coef))
    df_Pred = Model(real_flu_,coef_dict,Times)
    error = ((df_Pred - real_flu_)*(df_Pred - real_flu_)).sum().sum()
    if error < e:
        e = error
        coef_chose = coef
    print 'Processed '+str(i) + 'th , e = ' +str(e)
    
print coef_chose
        

#Processed 531440th , e = 1932720
#[[1.1000000000000001, 3], [1.0, 2], [1.0, 3], [1.1000000000000001, 2], [1.0, 2], [1.1000000000000001, 2]]
'''

coef = [[1.1000000000000001, 3], [1.0, 2], [1.0, 3], [1.1000000000000001, 2], [1.0, 2], [1.1000000000000001, 2]]
coef_dict = dict(zip(Places,coef))
df_Pred = Model(real_flu_,coef_dict,Times)




#plt.plot([sigmoid(i) for i in range(30)])

#df_Pred = Model(real_flu_,coef_dict,Times)

plt.figure()
plt.rc('figure',figsize = (15,8))

Places = Places[:]

plt.plot(real_flu_[Places],'s-',alpha=0.6)
plt.plot(df_Pred[Places],'p-.',alpha=0.6)
plt.legend(Places+Places , loc = 'upper left')
#plt.plot(df_Pred2,'*-.',alpha=0.5)
#plt.legend(Places+Places+Places , loc = 'upper left')

'''

plt.plot(real_flu_/real_flu_.max(),'-')
plt.plot(df_Pred/df_Pred.max(),'s-.',alpha=0.5)
plt.plot(df_Pred2/df_Pred2.max(),'p-.',alpha=0.5)
plt.legend(Places+Places+Places , loc = 'upper left')


df_Pred.applymap(lambda x : np.log(x)).plot()
df_Pred2.applymap(lambda x : np.log(x)).plot()


plt.plot(real_flu_)
plt.plot(df_Pred/Ratio,'-.')
plt.legend(Places+Places , loc = 'upper left')
'''
