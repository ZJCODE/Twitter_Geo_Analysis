# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 18:01:33 2016

@author: ZJun
"""

from GetData import LoadData
import numpy as np
import pandas as pd
from datetime import timedelta
from twitter_function import MapLocation,AddJudgeFlu

Data = LoadData()

def GetActuallDayInWeek():
    pass
    

def GetTwitterInPlaceLoc(Data,place = None ,location = None):
    '''
    return timeseries
    '''
    if place != None:        
        Data = Data[Data.District == place]
    if location != None:
        Data['Location'] = [MapLocation(l,place) for l in Data.Location]
        Data = Data[Data.Location == location]

    ts = pd.Series(np.ones(len(Data)),index=Data.created_at.values)
    week_ts = ts.resample('W-SUN',how='sum')
    weeks = [d.date() - timedelta(6) for d in week_ts.index]
    ts_twitter_in_place_loc = pd.Series(week_ts.values,index= weeks)
    return ts_twitter_in_place_loc


def GetFluRelatedTwitterInPlaceLoc(Data,place,location):
    '''
    return timeseries
    '''
    if place != None:        
        Data = Data[Data.District == place]
    if location != None:
        Data['Location'] = [MapLocation(l,place) for l in Data.Location]
        Data = Data[Data.Location == location]
    
    Data = AddJudgeFlu(Data)
    
    print 'Flu Added'
    ts = pd.Series(Data.Judge.values,index=Data.created_at.values)
    week_ts = ts.resample('W-SUN',how='sum')
    weeks = [d.date() - timedelta(6) for d in week_ts.index]
    ts_flu_related_twitter_in_place_loc = pd.Series(week_ts.values,index= weeks)
    return ts_flu_related_twitter_in_place_loc

'''
tt = GetFluRelatedTwitterInPlaceLoc(Data,'Queensland','Brisbane')
t = GetTwitterInPlaceLoc(Data,'Queensland','Brisbane')    
t.plot()
(a*20).plot()
#(tt*2000).plot()    
'''

    
def GetMoveInPlace(Move,place):
    '''
    specific location's place
    '''
    if place == None:
        MoveInWhere = Move
    else:        
        MoveInWhere = [a for a in Move if (place in a[1] and place in a[2])]
    users = [a[0] for a in MoveInWhere]
    pairs = [(MapLocation(a[1].split(',')[0],place),MapLocation(a[2].split(',')[0],place)) for a in MoveInWhere]
    DfMove = pd.DataFrame({'user':users,'pairs':pairs})
    DfMove['same'] = [0 if l[0]==l[1] else 1 for l in DfMove.pairs]
    DfMove = DfMove[DfMove.same == 1][['pairs','user']]
    return DfMove

def GetMoveDestinationInPlaceLoc(week_move,place,location):
    '''
    return timeseries
    '''   
    weeks = sorted(week_move.keys())
    count = []
    for w in weeks:
        move = week_move[w]
        move_in_place = GetMoveInPlace(move,place)
        destination = [i[1] for i in move_in_place.pairs]
        count.append(destination.count(location))
    ts = pd.Series(count,index = weeks)
    return ts
        

    

def GetFluRelatedMoveDestinationInPlaceLoc(place,location):
    '''
    return timeseries
    '''
    pass