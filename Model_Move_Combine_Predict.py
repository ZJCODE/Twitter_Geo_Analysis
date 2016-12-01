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

'''
Queensland_Flu = pd.read_csv('./Data/Queensland2015.csv')
from datetime import timedelta
def GetRealFlu(Queensland_Flu,location=None):
    first_week = pd.datetime(2015,1,5).date()
    t = [first_week]
    if location != None:        
        x = Queensland_Flu[location].values
    else:
        x = Queensland_Flu.ix[:,1:].sum(1).values
    for i in range(1,len(x)):
        t.append(first_week + timedelta(i*7))
    ts = pd.Series(x,index = t[:len(x)])
    return ts

real_flu = GetRealFlu(Queensland_Flu,Places[0]).values
index = GetRealFlu(Queensland_Flu,Places[0]).index
for p in Places[1:]:
    real_flu = np.c_[real_flu,GetRealFlu(Queensland_Flu,p).values]
                     
df_real_flu = pd.DataFrame(real_flu,columns=Places,index = index)
'''    
    




#TimeRange = [pd.datetime(2015,5,25).date(),pd.datetime(2015,10,12).date()]
TimeRange = [pd.datetime(2015,3,9).date(),pd.datetime(2015,10,12).date()]
            
              
#where_to_where_ =  GetPartOfTimeSeries(df_where_to_where,TimeRange)
#actual_days_in_week_  = GetPartOfTimeSeries(actual_days_in_week,TimeRange)
real_flu_ = GetPartOfTimeSeries(df_real_flu,TimeRange)[Places]

Times = real_flu_.index

# use each's move 


# (twitter_move_loc / twitter_all_loc * population_loc) * (real_flu_num_loc / population_loc)
# = (twitter_move_loc / twitter_all_loc  * real_flu_num_loc 

def norm(l):
    l = np.array(l)
    return (l-min(l))/(max(l)-min(l))     
     
     
plt.rc('figure',figsize = (16,20))


coef = []
for idx,place in enumerate(Places):
    
    twitter_move_loc_all = df_where_to_where.values[0][place][Places]*0
    for w2w in df_where_to_where.values:
        twitter_move_loc_all += w2w[place][Places]
    twitter_all_loc = df_twitter_in_place_loc.sum()
        
    
    y = real_flu_[place][1:].values
    x1 = real_flu_[place][:-1].values
    x2 = []
    for t in Times[:-1]:    
        #twitter_move_loc_t = df_where_to_where[t][place][population_2015.keys()]
        #twitter_all_loc_t = df_twitter_in_place_loc.loc[t]
        real_flu_num_loc_t = real_flu_.loc[t]
        #x2.append(sum(twitter_move_loc_t / twitter_all_loc_t * real_flu_num_loc_t))
        x2.append(sum(twitter_move_loc_all / twitter_all_loc * real_flu_num_loc_t))
    
    x2 = np.array(x2)
    from sklearn.linear_model import LinearRegression
    
    model = LinearRegression()
    model2 = LinearRegression()
    model3 = LinearRegression()
        
    X = np.c_[x1,x2]
    
    model.fit(X,y)
    model2.fit(x1[:,np.newaxis],y)
    model3.fit(x2[:,np.newaxis],y)
    
    
    r1 = model.score(X,y)
    r2 = model2.score(x1[:,np.newaxis],y)
    r3 = model3.score(x2[:,np.newaxis],y)
    
    
    
    y_pred = model.predict(X)
    y_pred_2 = model2.predict(x1[:,np.newaxis])
    y_pred_3 = model3.predict(x2[:,np.newaxis])
    
    

    
    plt.subplot(321+idx)
    
    y = pd.Series(y,index = Times[1:])
    y_pred = pd.Series(y_pred,index = Times[1:])
    y_pred_2 = pd.Series(y_pred_2,index = Times[1:])
    y_pred_3 = pd.Series(y_pred_3,index = Times[1:])
    
    
    plt.plot(y,'s',alpha=0.5)
    plt.plot(y_pred_3,'-',alpha=0.8)
    plt.legend(['real','y_pred_3'])
    plt.title(place+' | Population: '+str(population_2015[place]) 
    + ', R^2: ' + str(round(r3,3))
    )
    
    
    '''
    plt.plot(y,'s',alpha=0.5)
    plt.plot(y_pred,'-',alpha=0.6)
    plt.plot(y_pred_2,'-',alpha=0.8)
    plt.plot(y_pred_3,'-',alpha=0.8)

    

    plt.legend(['real','y_pred','y_pred_2','y_pred_3'])
    plt.title(place+' | Population: '+str(population_2015[place]) 
    + ' | R_1 : ' +str(round(r1,3)) 
    + ', R_2: ' + str(round(r2,3))
    + ', R_3: ' + str(round(r3,3))
    )
    
    coef.append(np.r_[model3.coef_,model3.intercept_])
    coef_dict = dict(zip(Places,coef))
    '''
    
    
# Model 


coef = [[1.12,3],[1.1,1],[1.1,3],[1.1,4],[1.1,5],[1.1,2]][:n]
coef2 = [[1.3,2],[1.3,2],[1.3,2],[1.3,2],[1.3,2],[1.3,2]][:n]
coef_dict = dict(zip(Places,coef))
coef_dict2 = dict(zip(Places,coef2))

Pred = np.c_[real_flu_.loc[Times[0]].values]

Pred2 = np.c_[real_flu_.loc[Times[0]].values]


all_where_to_where = df_where_to_where.values[0]*0 

for w2w in df_where_to_where.values:
    all_where_to_where += w2w

all_where_to_where.loc['Brisbane'] = all_where_to_where.loc['Brisbane']*0.9
all_where_to_where['Brisbane'] = all_where_to_where['Brisbane']*0.9
    
twitter_all_loc = df_twitter_in_place_loc.sum()

for i in range(len(Times)-1):
    place_flu = []
    place_flu2 = []
    for place in Places:

        twitter_move_loc_all = all_where_to_where[place][Places]
        
        #twitter_move_loc_all['Brisbane'] = twitter_move_loc_all['Brisbane']
        
        flu = pd.Series(Pred[:,i],index = Places)
        x1 = flu[place]
        x2 = sum(twitter_move_loc_all / twitter_all_loc * flu)
        #y_1 = np.dot([x1,x2,1],coef_dict[place])
        y_1 = np.dot([x1,x2],coef_dict[place])
        
        flu2 = pd.Series(Pred2[:,i],index = Places)
        x1_2 = flu2[place]
        y_2 = np.dot([x1_2,1],coef_dict2[place])
        #y_1 = np.dot([x1,x2,1],np.array([1,9,0]))
        
        place_flu.append(y_1)
        place_flu2.append(y_2)
    #place_flu = [i - np.random.randint(0,i*0.4) for i in place_flu]
    def sigmoid(x):
        return 0.5/(1+0.006*np.exp((len(Times)-3)-x))
        
    def sigmoid_(x):
        return 1/(1+np.exp(-x/25.0))-0.5
    p=sigmoid(i)
    #p = sigmoid_(i)
    place_flu = [a - a*p for a in place_flu]
    
    place_flu2 = [a - a*p for a in place_flu2]
    
    Pred = np.c_[Pred,place_flu]
    
    Pred2 = np.c_[Pred2,place_flu2] 
    
df_Pred = pd.DataFrame(Pred.T,columns=Places,index=Times)

df_Pred2 = pd.DataFrame(Pred2.T,columns=Places,index=Times)

real_flu_ = real_flu_[Places]
df_Pred = df_Pred[Places].applymap(lambda x: int(x))
df_Pred2 = df_Pred2[Places].applymap(lambda x: int(x))



#plt.plot([sigmoid(i) for i in range(30)])

plt.figure()
plt.rc('figure',figsize = (12,7))

plt.plot(real_flu_,'s-',alpha=0.6)
plt.plot(df_Pred,'p-.',alpha=0.6)
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


def Draw_P_Mat(P):
    plt.rc('figure',figsize=(len(P.columns)*1.8,len(P.index)*1.8))
    plt.matshow(P, cmap=plt.get_cmap("jet"),alpha=0.9)
    pos = np.arange(len(P.columns))
    plt.xticks(pos, P.columns)
    pos = np.arange(len(P.index))
    plt.yticks(pos, P.index)
    plt.colorbar()