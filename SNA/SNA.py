# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 14:04:45 2016

@author: ZJun
"""

import numpy as np
import re
import itertools
import networkx as nx
from PowLaw import *   
import pandas as pd
from GetData import getData
# https://pypi.python.org/pypi/louvain/
import community
import matplotlib.pyplot as plt

def Import_Obj(File):    
    import pickle
    File_Name = File+'.pkl'
    pkl_file = open(File_Name, 'rb')
    return  pickle.load(pkl_file)

Data = getData(with_geo_tag=True)

IdNameDict = Import_Obj('./Data/IdNameDict')
    

def addUserName(Data):
    user_name = [IdNameDict[Id] for Id in Data.uid]
    Data['user_name'] = user_name
    
    

def addPlace(Data):
    Place = []
    for loc in Data.location_name:
        try:
            Place.append(loc.split(',')[1])
        except:
            Place.append(np.nan)
    Data['Place'] = Place
    

def extractAt(text):
    pattern=r'@([\w.-]+)'
    at_names = re.findall(pattern, text)
    at_names = [str.lower(name) for name in at_names]
    return at_names

    
def addRelation(Data):
    friends_list = [extractAt(text) for text in Data.text]
    Data['friends_list'] = friends_list
    
def getFriendsPair(Data,removeDuplicate = True):
    friends_pair = []
    for ego,friend in zip(Data.user_name,Data.friends_list):
        friends_pair += itertools.product([ego],friend)
    if removeDuplicate == True:        
        friends_pair_list = list(set(friends_pair))
        return friends_pair_list
    else:
        return friends_pair

def getRelation(Data):
    addUserName(Data)
    addRelation(Data)
    Relation = getFriendsPair(Data,removeDuplicate = True)
    return Relation
    
        
def generateNetwork(Relation,direct):
    if direct == False :    
        G = nx.Graph()
        G.add_edges_from(Relation)
        return G
    else:
        DG=nx.DiGraph()
        DG.add_edges_from(Relation)
        return DG
    
    
    

def getNetwork(Data,direct):
    Relation = getRelation(Data)
    G = generateNetwork(Relation,direct)
    return G
    
   
def communityDetection(DG,n,with_arrow = False,with_label = False):
    
    G = DG.to_undirected()
    Community_Nodes_List = []
    plt.rc('figure',figsize=(12,10))
    #first compute the best partition
    partition = community.best_partition(G) # Nodes With Community tag
    from collections import Counter
    Main = [a[0] for a in Sort_Dict(Counter(partition.values()))[:n]] # Top n Community's Tag
    ZipPartition = partition.items()
    SubNodes = [a[0] for a in ZipPartition if a[1] in Main] # NodesList belong to Top Community
    
    if with_arrow == False:        
        SubG = nx.subgraph(G,SubNodes)
    else:
        SubG = nx.subgraph(DG,SubNodes)
        
    #pos = nx.spectral_layout(SubG)
    #pos = nx.spring_layout(SubG)
    #pos = nx.shell_layout(SubG)
    pos = nx.fruchterman_reingold_layout(SubG)
    if with_label == True:        
        nx.draw(SubG,pos,node_size = 1,alpha =0.1,with_labels=True)
    #drawing
    count = -1

    color = ['b','g','r','c','m','y','k','w']
    for com in set(partition.values()) :
        if com in Main:
            
            count = count + 1
            list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
            Community_Nodes_List.append(list_nodes)
            nx.draw_networkx_nodes(SubG,pos, list_nodes, node_size = 25,
                                        node_color = color[count],alpha =0.5,with_labels=True)
            
    plt.legend(range(1,n+1))
    nx.draw_networkx_edges(SubG,pos,arrows=True,alpha=0.2)
    plt.show()
    return Community_Nodes_List
    

def doPowLaw(G):    
    G_UnDi = G.to_undirected()
    degree = nx.degree_histogram(G_UnDi)
    Gamma = PowLawFit(degree[1:],Draw = 1)
    return Gamma


def drawGraph(G):
    plt.rc('figure' ,figsize = (15,15))
    nx.draw_networkx(G, pos=nx.spring_layout(G), arrows=True, with_labels=False, node_size=1,node_color='r')


def Sort_Dict(Diction):
    L = list(Diction.items())
    Sort_L = sorted(L,key = lambda x:x[1] , reverse= True)
    return Sort_L

def getCoreSubNetwork(G,start,end,direct):    
    if direct not in ['No','In','Out']:
        print 'Undefined direct'
        pass
    else:        
        if direct == 'No':
            G_UnDi = G.to_undirected()
            D = nx.degree(G_UnDi)
            SD = Sort_Dict(D)
            Sample_Nodes = [a[0] for a in SD[start:end]]
            SubG = nx.subgraph(G_UnDi,Sample_Nodes)
            return SubG
        if direct == 'In':
            D = G.in_degree()
            SD = Sort_Dict(D)
            Sample_Nodes = [a[0] for a in SD[start:end]]
            SubG = nx.subgraph(G,Sample_Nodes)
            return SubG
        if direct == 'Out':
            D = G.out_degree()
            SD = Sort_Dict(D)
            Sample_Nodes = [a[0] for a in SD[start:end]]
            SubG = nx.subgraph(G,Sample_Nodes)
            return SubG
    
def test():
    G = getNetwork(Data,True)
    doPowLaw(G)
    SubG = getCoreSubNetwork(G,500,2000)
    N = communityDetection(SubG,3)