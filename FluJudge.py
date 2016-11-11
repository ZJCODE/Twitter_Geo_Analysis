# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 17:25:22 2016

@author: ZJun
"""
import psycopg2 as db
import pandas as pd
import numpy as np

def GetDataText():
    
    conn = db.connect("host=localhost dbname=aussie_twitter user=postgres password=dbzjun client_encoding='utf-8'")
    # conn.set_character_set('utf8')
    cur = conn.cursor()         
    SELECT_QUERY="""
    SELECT uid,text,created_at
    FROM aussie_tweets 
    ORDER BY created_at
    """
    try:
        cur.execute(SELECT_QUERY)
        rows = cur.fetchall()
        X = np.array(rows)
    except db.Error, e:
        print "Error ocurred: %s " % e.args[0]
        print e     
    data_text = pd.DataFrame(X,columns=['uid','text','created_at'])
    return data_text

def Import_Obj(File):    
    import pickle
    File_Name = File+'.pkl'
    pkl_file = open(File_Name, 'rb')
    return  pickle.load(pkl_file)
    

def AddUserName(Data):
    id_name_dict = Import_Obj('./Data/IdNameDict')
    user_name = [id_name_dict[Id] for Id in Data.uid]
    Data['user_name'] = user_name
    
def AddDate(Data):
    d = [d.date() for d in Data.created_at]
    Data['date'] = d

def JudegFlu(text):
    '''
    input one text
    return 0 : not flu related ,1 : flu related
    '''
    text =text.lower()    

    def WordsIn(words,sentence):
        for w in words:
            if w in sentence:
                pass
            else:
                return False
        return True
    
    flu_words = ['influenza','flu','fever',
    'cough',('sore' ,'throat'),('catch','cold'),('sick','cold'),('week','cold'),
    'infect',('cold','ill'),('cold','illness'),('viruses','cold'),('vaccine','cold'),
    ('cold','hospital'),('cold','headache'),('runny','nose'),('cold','medicine'),
    ('cold','infections')]
    text2words = text.strip().split(' ')
    for fw in flu_words:
        if isinstance(fw,tuple):
            if WordsIn(fw,text2words):
                #print 'tuple'
                #print text
                return 1
            else:
                return 0
        else:
            if fw in text2words:
                #print text
                return 1
            else:
                0
                
def AddJudgeFlu(Data):
    Judge = [JudegFlu(text) for text in Data.text]
    Data['Judge'] = Judge    

data_text = GetDataText()


def UserFluStataByTime(data_text,way = 'week'):    
    AddDate(data_text)
    AddUserName(data_text)
    AddJudgeFlu(data_text)
    from datetime import timedelta
    data_text = data_text.sort_values(['date','user_name'])
    if way == 'week':
        days = sorted(list(set(data_text.date))) 
        min_day =  min(days)
        if min_day.weekday() == 0:
            date_start = min_day
        else:            
            date_start = min_day + timedelta(7-min_day.weekday())
        day_7 = timedelta(7)
        date_end = date_start + day_7
        t = [date_start + timedelta(1)]
        flu_user = []
        actual_day = [] # how many days in that week
        for i in range((max(days) - min(days)).days/7):
            print str(i+1) + ' Week Finished'
            data = data_text[(data_text.date > date_start)&(data_text.date <= date_end)]
            actual_day.append(len(set(data.date)))
            flu_data = data[data.Judge == 1]
            flu_user.append(list(set(flu_data.user_name)))
            t.append(date_start + timedelta(1))
            date_start = date_end
            date_end = date_start + day_7
        flu_user_and_days = zip(flu_user,actual_day)
        return dict(zip(t,flu_user_and_days))
        
    elif way == 'day':
        days = sorted(list(set(data_text.date)))
        flu_user = []
        for day in days:
            data = data_text[data_text.date == day]
            flu_data = data[data.Judge == 1]
            flu_user.append(list(set(flu_data.user_name)))
            print str(day) + ' Finished '
        return dict(zip(days,flu_user))
            
    elif way == 'month':
        t = range(1,9)
        flu_user = []
        actual_day = [] # how many days in that month
        data_text['month'] = [date.month for date in data_text.date]
        for month in t:
            data = data_text[data_text.month == month]
            actual_day.append(len(set(data.date)))
            flu_data = data[data.Judge == 1]
            flu_user.append(list(set(flu_data.user_name)))
            print str(month) + ' Month Finished'
        flu_user_and_days = zip(flu_user,actual_day)
        return dict(zip(t,flu_user_and_days))    
    else:
        print 'Input Error Way'
        
        