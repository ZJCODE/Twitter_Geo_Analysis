# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 11:25:56 2016

@author: ZJun
"""

from GetData import getData,AddPos
import pandas as pd
from datetime import timedelta
import numpy as np

from twitter_function import Save_Obj,AddUserName,AddDate,JudegFlu,AddJudgeFlu,MapLocation


Data = getData()
def CountWeekly(Data,place,loc,flu=True):
    Data = AddPos(Data)
    AddJudgeFlu(Data)
    Data = Data[Data.District == place]
    Data['Location'] = [MapLocation(l,place) for l in Data.Location]
    Data = Data[Data.Location == loc]
    if flu == True:
       TS= pd.Series(Data.Judge.values,index=Data.created_at.values)
    else:
        TS= pd.Series(np.ones(len(Data)),index=Data.created_at.values)
    week_ts = TS.resample('W-SUN',how='sum')
    weeks = [d.date() - timedelta(6) for d in week_ts.index]
    count = week_ts.values
    count_weekly_dict = dict(zip(weeks,count))
    return count_weekly_dict
        
    
