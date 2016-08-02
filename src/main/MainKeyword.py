# -*- coding: utf-8 -*-
'''
Created on 25 avr. 2016

@author: Kévin Bienvenu
'''

import time

import UtilsConstants, IOFunctions, KeywordSelector


def main(arg):
    if arg=="compute graph pipeline":
        # pipeline graph
        KeywordSelector.pipelineGraph(n=200)
        
    elif arg=="main pipeline":
        # Main Pipeline
#         entreprises = IOFunctions.extractSubset("", 5)  
        entreprises = [["0111Z","Le dénoyautage de pruneaux. Achat et revente de produits alimentaires. Achat et revente de jouets bijoux de fantaisie décorations et accessoires de mode achat et revente de vêtements."]]
        KeywordSelector.pipeline(entreprises, 20)
        

    elif arg=="test pipeline":
        KeywordSelector.pipelineTest()


# KeywordSelector.cleanKeyword()




# main("main pipeline")
t = time.time()
main("test pipeline")
UtilsConstants.printTime(t)
# main("compute graph pipeline")

# KeywordSelector.deleteKeyword(["promotion",
#                                 "gestion"])



