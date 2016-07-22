# -*- coding: utf-8 -*-
'''
Created on 12 mai 2016

@author: Kévin Bienvenu
'''

import codecs
from operator import itemgetter
import os, time

from nltk.corpus import stopwords
import nltk.stem.snowball
import unidecode, re

import numpy as np
import numpy.linalg as lg


user = os.path.dirname(os.path.abspath(__file__)).split("\\")[2]
tabpath = os.path.dirname(os.path.abspath(__file__)).split("\\")
path = "C:/"
for tab in tabpath[1:tabpath.index("src")]:
    path = os.path.join(path, tab)

pathAgreg = os.path.join("C:/","Users",user,"Google Drive","Camelia Tech","Donnees entreprise","Agregation B Reputation")
pathSubset = os.path.join(path,"subsets")
pathCodeNAF = os.path.join(path,"preprocessingData","codeNAF")
pathClassifiers = os.path.join(path,"preprocessingData","classifiers")
pathConstants = os.path.join(path,"preprocessingData","constants")

os.chdir(os.path.join(path,"preprocessingData"))
    

''' Auxiliary functions and classes'''

class Compt():
    ''' class which implements the compt object, 
    which main purpose is printing progress
    '''
    def __init__(self, completefile, p=10, printAlone=True):
        self.i = 0
        self.total = len(completefile)
        self.percent = p
        self.deltaPercent = p
        self.printAlone = printAlone

    def updateAndPrint(self):
        self.i+=1
        if 100.0*self.i/self.total >= self.percent:
            print self.percent,"%",
            self.percent+=self.deltaPercent
            if (self.deltaPercent==1 and self.percent%10==1) \
                or (self.deltaPercent==0.1 and ((int)(self.percent*10))%10==0) \
                or (self.i==self.total) \
                or not self.printAlone:
                    print ""
                                
def printTime(startTime):
    totalTime = (time.time()-startTime)
    hours = (int)(totalTime/3600)
    minutes = (int)((totalTime-3600*hours)/60)  
    seconds = (int)(totalTime%60)
    print "time : ",hours,':',minutes,':',seconds
                  
def saveDict(dic,filename,sep="-"):
    with codecs.open(filename,'w','utf-8') as fichier:
        for item in dic.items():
            try:
                int(item[0])
                fichier.write(str(item[0]))
            except:
                fichier.write(item[0])
            fichier.write(sep)
            try:
                int(item[1])
                fichier.write(str(item[1]))
            except:
                fichier.write(item[1])
            fichier.write("\n")

def importDict(filename,sep="-"):
    dic = {}
    with codecs.open(filename,'r','utf-8') as fichier:
        for line in fichier:
            tab = line[:-1].split(sep)
            s = tab[0]
            for i in range(1,len(tab)-1):
                s+=tab[i]
            dic[s] = tab[-1]
            try:
                dic[s] = float(dic[s])
            except:
                pass
    return dic
   
def printSortedDic(dic, nprint=0):      
    '''
    function that print a dic sorted according to its values
    if the parameter nprint in given and non zero, print only the nprint greatest values
    -- IN:
    dic : dic which values must be int or float (dic{object:float})
    nprint : number of values to print (int) default=0
    -- OUT:
    the function returns nothing
    '''
    l = dic.items()
    l.sort(key=itemgetter(1),reverse=True)
    imax = nprint
    if imax==0:
        imax = len(l)
    if len(l)>0:
        m = max([len(li[0]) for li in l])+1
    for i in range(min(imax,len(l))):
        print "    ",l[i][0],
        for _ in range(m-len(l[i][0])):
            print "",
        print l[i][1]
       
''' Auxiliary text processing functions'''

def preprocessString(srctxt):
    '''
    function transforming str and unicode to string without accent
    or special characters, writable in ASCII
    '''
    try:
        srctxt = unicode(srctxt,"utf8")
    except:
        pass
    return unidecode.unidecode(srctxt).lower()

def tokenizeAndStemmerize(srctxt, 
                keepComa = False, 
                french_stopwords = set(stopwords.words('french')),
                stem = nltk.stem.snowball.FrenchStemmer(),
                method = "stem"):
    '''
    NLP function that transform a string into an array of stemerized tokens
    The punctionaction, stopwords and numbers are also removed as long as words shorter than 3 characters
    -- IN:
    srctxt : the string text to process (string)
    keepComa : boolean that settles if the process should keep comas/points during the process (boolean) default=false
    french_stopwords : set of french stop_words
    stem : stemmerizer
    -- OUT:
    stems : array of stemerized tokens (array[token]) 
    '''
    srctxt = preprocessString(srctxt)
    srctxt = re.sub(r" \(([a-z]| )*\)","",srctxt)
    srctxt = re.sub(r"-"," ",srctxt)
    tokens = nltk.word_tokenize(srctxt,'french')
    tokens = [token for token in tokens if (keepComa==True and (token=="." or token==",")) \
                                            or (len(token)>1 and token not in french_stopwords)]
    stems = []
    for token in tokens:
        try:
            # removing numbers
            float(token)
        except:
            if token[0:2]=="d'" or token[0:2]=="l'":
                token = token[2:]
            if len(token)>2:
                if method=="stem":
                    stems.append(stem.stem(token)) 
                else:
                    stems.append(token)
            if len(token)==1 and keepComa==True:
                stems.append(token)        
    return stems
        
''' Creating and saving constants parameters '''
            
def loadConstants():
    os.chdir(pathConstants)
    parametersStep01 = importDict("parametersStep01.txt", "_")
    parametersMatchStep01 = importDict("parametersMatchStep01.txt", "_")
    parametersStep03 = importDict("parametersStep03.txt", "_")
    parametersStep04 = importDict("parametersStep04.txt", "_")
    blacklistStep04 = {}
    with codecs.open("blacklistStep04.txt","r","utf-8") as fichier:
        for line in fichier:
            i = -2
            if len(line)>1:
                tokens = tokenizeAndStemmerize(line[:i])
                if len(tokens)>0:
                    blacklistStep04[line[:i]] = tokens
                else:
                    continue
    return parametersStep01, parametersMatchStep01, parametersStep03, parametersStep04, blacklistStep04

# Normalisation step 01 function

def normalisationStep01():
    valMax = (parametersStep01['freqSlugAlpha']*165+parametersStep01['freqSlugGamma']/165+parametersStep01['coefProxi'])*(parametersStep01['placePremierTier']*parametersStep01["placeMot0"])*(parametersStep01['nbCommaGamma'])/2.0
    valMaxUnique = (parametersStep01['freqSlugAlpha']*165+parametersStep01['freqSlugGamma']/165+parametersStep01['coefProxi']/2)*(parametersStep01['placePremierTier']*parametersStep01["placeMot0"])*(parametersStep01['nbCommaGamma'])/2.0
    a = np.array([[valMax**3,valMax**2,valMax],[3*valMax**2,2*valMax, 1],[6*valMax,2,0]])
    b = np.array([1,0,0])
    normalisationParam = lg.solve(a,b)
    return lambda x : min(1.0,normalisationParam[-3]*x**3+normalisationParam[-2]*x*x+normalisationParam[-1]*x), valMaxUnique

blacklistStep04 = {}
parametersStep01, parametersMatchStep01, parametersStep03, parametersStep04, blacklistStep04 = loadConstants()
normalisationFunction, valMaxUnique = normalisationStep01()     

def saveConstants():
    os.chdir(pathConstants)
    saveDict(parametersStep01, "parametersStep01.txt", "_")
    saveDict(parametersMatchStep01, "parametersMatchStep01.txt", "_")
    saveDict(parametersStep03, "parametersStep03.txt", "_")
    saveDict(parametersStep04, "parametersStep04.txt", "_")