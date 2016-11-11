# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 17:25:22 2016

@author: ZJun
"""


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
                print 'tuple'
                print text
                return 1
            else:
                return 0
        else:
            if fw in text2words:
                print text
                return 1
            else:
                0
                
                
                