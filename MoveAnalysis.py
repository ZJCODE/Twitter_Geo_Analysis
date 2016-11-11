# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 13:16:13 2016

@author: ZJun
"""

import pandas as pd
from Net import GenerateNetwork,GenerateNetworkWithWeight,DrawGraph,GetCoreSubNetwork,CommunityDetection
from collections import Counter

def Import_Obj(File):    
    import pickle
    File_Name = File+'.pkl'
    pkl_file = open(File_Name, 'rb')
    return  pickle.load(pkl_file)
    

def Save_Obj(Obj,File_Name):    
    import pickle
    File = File_Name + '.pkl'
    output = open(File, 'wb')
    pickle.dump(Obj, output)
    output.close()    

def Sort_Dict(Diction):
    L = list(Diction.items())
    Sort_L = sorted(L,key = lambda x:x[1] , reverse= True)
    return Sort_L

def GenerateDate(year,month,day):
    return pd.datetime(year,month,day).date()



def ExportEdgesToGephi(relation):    
    R = pd.DataFrame(relation,columns=['Source','Target'])
    R.to_csv('edges.csv',index=False)
    
def ExportNodeCategoryToGephi(nodes_category):    
    nodes_category.to_csv('node_category.csv',index=False)



def GetMoveInWhere(Move,place):
    '''
    specific location's place
    '''
    MoveInWhere = [a for a in Move if (place in a[1] and place in a[2])]
    users = [a[0] for a in MoveInWhere]
    pairs = [[a[1],a[2]] for a in MoveInWhere]
    DfMove = pd.DataFrame({'user':users,'pairs':pairs})
    return DfMove



def FliterFlu(week_move,week_user_flu_state,where):
    
    weeks = sorted(week_move.keys())
    flu_pair = []
    actual_day_list = []
    for w in weeks:
        move = week_move[w]
        MoveSomeWhere = GetMoveInWhere(move,where)
        flu_state = week_user_flu_state[w]
        flu_users = flu_state[0]
        actual_day_list.append(flu_state[1])
        Judge = [1 if user in flu_users else 0 for user in MoveSomeWhere.user]
        MoveSomeWhere['Judge'] = Judge
        flu_related_data = MoveSomeWhere[MoveSomeWhere.Judge==1]
        flu_pair.append(flu_related_data.pairs.values)
    return dict(zip(weeks,flu_pair)),actual_day_list
   

a,days = FliterFlu(week_move,week_user_flu_state,'Queensland')
l = np.array([len(m) for m in a.values()])    
actual_l = l*1.0/np.array(days)
plt.plot(weeks,actual_l)
    
def TestWeekMovePattern(y=2015,m=1,d=13):    
    week_move = Import_Obj('./Data/week_move')
    relation = []
    G = GenerateNetwork(relation,direct = True)
    SubG = GetCoreSubNetwork(G,0,100,'No')
    n,e = CommunityDetection(SubG,3,with_label=True,with_arrow=True)
    ExportEdgesToGephi(e)
    ExportNodeCategoryToGephi(n)

'''
WG = GenerateNetworkWithWeight(edge_with_weight,direct=True)    
WG.in_degree(WG.nodes()[20],weight='weight')
'''


    
    
    
