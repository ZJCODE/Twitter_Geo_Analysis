# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 13:16:13 2016

@author: ZJun
"""

import pandas as pd
import numpy as np
from Net import GenerateNetwork,GenerateNetworkWithWeight,DrawGraph,GetCoreSubNetwork,CommunityDetection
from collections import Counter
import  matplotlib.pyplot as plt
from twitter_function import Import_Obj,Save_Obj,Sort_Dict,GenerateDate,MapLocation




def GetMoveInWhere(Move,place):
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
    DfMove = DfMove[DfMove.same == 1]
    return DfMove

def FliterFlu(week_move,week_user_flu_state,place=None):
    
    weeks = sorted(week_move.keys())
    flu_pair = []
    actual_day_list = []
    for w in weeks:
        move = week_move[w]
        MoveSomeWhere = GetMoveInWhere(move,place)
        flu_state = week_user_flu_state[w]
        flu_users = flu_state[0]
        actual_day_list.append(flu_state[1])
        Judge = [1 if user in flu_users else 0 for user in MoveSomeWhere.user]
        #Judge = [1 for user in MoveSomeWhere.user]
        MoveSomeWhere['Judge'] = Judge
        flu_related_data = MoveSomeWhere[MoveSomeWhere.Judge==1]
        flu_pair.append(flu_related_data.pairs.values)
        week_flu_pair = dict(zip(weeks,flu_pair))
    return week_flu_pair,actual_day_list

def CountToWhere(week_flu_pair):
    count_destination_list=[]
    weeks = sorted(week_flu_pair.keys())
    for w in weeks:
        pair = week_flu_pair[w]
        destination = [d[1] for d in pair]
        count_destination = Counter(destination)
        count_destination_list.append(count_destination)
    week_count_destination = dict(zip(weeks,count_destination_list))    
    return week_count_destination
    


 
week_move = Import_Obj('./Data/week_move')
week_user_flu_state = Import_Obj('./Data/week_user_flu_state')
Queensland_Flu = pd.read_csv('./Data/Queensland2015.csv')
week_flu_pair,actual_day_list = FliterFlu(week_move,week_user_flu_state,'Queensland')

def AnalysisCompare(Queensland_Flu,week_flu_pair,actual_day_list,loc,n,r):
    '''
    loc = ['Cairns', 'Townsville', 'Mackay', 'Fitzroy', 'Wide Bay',
   'Sunshine Coast', 'Brisbane', 'Darling Downs', 'Moreton',
   'Gold Coast']
    '''
    m = CountToWhere(week_flu_pair)
    weeks = sorted(week_flu_pair.keys())
    
    l=[]
    #ll=[]
    for w in weeks:
        l.append(m[w][loc])
        #ll.append(cw[w])
        
    l = np.array(l)*1.0/np.array(actual_day_list)
    #ll = np.array(ll)*1.0/np.array(actual_day_list)

        
    p = Queensland_Flu[loc].values    
    
    plt.plot(np.r_[np.zeros(n),l[:19]]*r+35,'.-')
    plt.plot(p[2:21],'*-')
    #plt.plot(np.r_[np.zeros(0),ll[:19]]*r+40,'r-')
    #plt.xlim([1.5,20.5])
    plt.legend(['l','p','ll'])
    


    
'''
def TestWeekMovePattern(y=2015,m=1,d=13):    
    week_move = Import_Obj('./Data/week_move')
    relation = []
    G = GenerateNetwork(relation,direct = True)
    SubG = GetCoreSubNetwork(G,0,100,'No')
    n,e = CommunityDetection(SubG,3,with_label=True,with_arrow=True)
    ExportEdgesToGephi(e)
    ExportNodeCategoryToGephi(n)


WG = GenerateNetworkWithWeight(edge_with_weight,direct=True)    
WG.in_degree(WG.nodes()[20],weight='weight')


def ExportEdgesToGephi(relation):    
    R = pd.DataFrame(relation,columns=['Source','Target'])
    R.to_csv('edges.csv',index=False)
    
def ExportNodeCategoryToGephi(nodes_category):    
    nodes_category.to_csv('node_category.csv',index=False)
'''

    
    
    
