# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 22:01:06 2016

@author: ZJun
"""

from GetData import LoadData
from twitter_function import Import_Obj
import pandas as pd
import numpy as np
from GetFactors import GetTwitterInPlaceLoc,GetFluRelatedTwitterInPlaceLoc,GetMoveDestinationInPlaceLoc,GetFluRelatedMoveDestinationInPlaceLoc

week_move = Import_Obj('./Data/week_move')
week_user_flu_state = Import_Obj('./Data/week_user_flu_state')
Queensland_Flu = pd.read_csv('./Data/Queensland2015.csv')

Data = LoadData()

flu_related_twitter_in_place_loc = GetFluRelatedTwitterInPlaceLoc(Data,'Queensland','Brisbane')
twitter_in_place_loc = GetTwitterInPlaceLoc(Data,'Queensland','Brisbane')
move_destination_in_place_loc = GetMoveDestinationInPlaceLoc(week_move,'Queensland','Brisbane')    
flu_related_move_destination_in_place_loc = GetFluRelatedMoveDestinationInPlaceLoc(week_move,week_user_flu_state,'Queensland','Brisbane')

