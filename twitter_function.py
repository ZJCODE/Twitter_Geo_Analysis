

def AddDate(Data):
    d = [d.date() for d in Data.created_at]
    Data['date'] = d

def AddUserName(Data):
    id_name_dict = Import_Obj('./Data/IdNameDict')
    user_name = [id_name_dict[Id] for Id in Data.uid]
    Data['user_name'] = user_name
    

def JudegFlu(text):  # Need to be improved
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
            #print fw
            if WordsIn(fw,text2words):
                #print 'tuple'
                #print text
                return 1
            else:
                pass
        else:
            #print fw
            if fw in text2words:
                #print text
                return 1
            else:
                pass
    return 0

                
def AddJudgeFlu(Data):
    J = [JudegFlu(text) for text in Data.text]
    Data['Judge'] = J    
    return Data


def GenerateDate(year,month,day):
    import pandas as pd
    return pd.datetime(year,month,day).date()

def MapLocation(location,place):
    if place == 'Queensland':
        hhs_loc = ['Cairns', 'Townsville', 'Mackay', 'Fitzroy', 'Wide Bay',
           'Sunshine Coast', 'Brisbane', 'Darling Downs', 'Moreton',
           'Gold Coast']
        
        if location.startswith('Brisbane'):
            location = 'Brisbane'
        if location.startswith('Moreton'):
            location = 'Moreton'
        
        if location not in hhs_loc:
            return None
        else:        
            return location
    else:
        return location


def Import_Obj(File):    
    import pickle
    File_Name = File+'.pkl'
    pkl_file = open(File_Name, 'rb')
    return  pickle.load(pkl_file)


def Sort_Dict(Dictionary):
    L = list(Dictionary.items())
    Sort_L = sorted(L,key = lambda x:x[1] , reverse= True)
    return Sort_L


def Save_Obj(Obj,File_Name):    
    import pickle
    File = File_Name + '.pkl'
    output = open(File, 'wb')
    pickle.dump(Obj, output)
    output.close()


def Normalize(x):
    x = np.array(x)
    return (x-x.mean())*1.0 / x.std()    


def Sort_Dict_key(Dictionary):
    L = list(Dictionary.items())
    Sort_L = sorted(L,key = lambda x:x[0] , reverse= False)
    return Sort_L
