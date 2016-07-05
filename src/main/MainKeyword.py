# -*- coding: utf-8 -*-
'''
Created on 25 avr. 2016

@author: Kévin Bienvenu
'''

import os
import time

import  Constants
import IOFunctions
from main import KeywordSelector
import pandas as pd


def main(arg):
    if arg=="compute graph pipeline":
        # COMPUTING GRAPH
        print "COMPUTING COMPLETE GRAPH PIPELINE"
        print ""
        n = 10000
        startingPhase = 0
        
        # Step 0 : creating a subset of size n
        if(startingPhase<=0):
            startTime = time.time()
            print "Step 0 : creating a subset of size n=",str(n)
            codeNAF = ""
            IOFunctions.extractSubset(codeNAF, n)
            Constants.printTime(startTime)
            print ""

        # Step 1 : computing the graph for this subset
        if(startingPhase<=1):
            startTime = time.time()
            print "Step 1 : computing the graph for this subset"
            subsetname = "graphcomplet_size_"+str(n)
            path = Constants.pathCodeNAF
            localKeywords = False
            print "   computing graph..."
            IOFunctions.extractGraphFromSubset(subsetname, path, localKeywords)
            print "   computing keywords..."
            IOFunctions.extractKeywordsFromGraph(subsetname, path)
            Constants.printTime(startTime)
            print ""

        # Step 2 : creating subset for all NAF
        if(startingPhase<=2):
            startTime = time.time()
            print "Step 2 : creating subset for all NAF"
            codeNAFs = IOFunctions.importListCodeNAF()
            compt = Constants.Compt(codeNAFs, 1, False)
            for codeNAF in codeNAFs:
                compt.updateAndPrint()
                IOFunctions.extractSubset(codeNAF, n, path = path, toPrint=True)
            Constants.printTime(startTime)
            print ""
        
        # Step 3 : computing graph for all code NAF, using keywords from Step 0-1
        if(startingPhase<=3):
            startTime = time.time()
            print "Step 3 : computing graph for all code NAF, using keywords from Step 0-1"
            compt = Constants.Compt(codeNAFs, 1, False)
            for codeNAF in codeNAFs:
                compt.updateAndPrint()
                IOFunctions.extractGraphFromSubset("subset_NAF_"+codeNAF, path)
            Constants.printTime(startTime)
            print ""
        
        # Step 4 : extracting keywords for all NAF from graphs of Step 3
        if(startingPhase<=4):
            startTime = time.time()
            print "Step 4 : extracting keywords for all NAF from graphs of Step 3"
            compt = Constants.Compt(codeNAFs, 1, False)
            for codeNAF in codeNAFs:
                compt.updateAndPrint()
                os.chdir(path)
                for directory in os.listdir("."):
                    if directory[0]=="s":
                        IOFunctions.extractKeywordsFromGraph(directory, path)
            Constants.printTime(startTime)
            print ""
        
        # Step 5 : compute complete graph using local keywords
        if(startingPhase<=5):
            startTime = time.time()
            print "Step 5 : compute complete graph using local keywords"
            subsetname = "graphcomplet"
            localKeywords = True
            IOFunctions.extractGraphFromSubset(subsetname, path, localKeywords)
            Constants.printTime(startTime)
            print ""
        
    elif arg=="main pipeline":
        # Main Pipeline
        des = [
               "Production cinématograhique et audiovisuelle",
                "Enseignement de la conduite de véhicules terrestres et de sécurité routière, école de conduite et pilotage de tous engins flottants ou aériens, formation de tous moniteurs.",
                "Gestion, propriété, administration et disposition des biens qui pourront devenir la propriété de la société par voie d'acquisition, d'échange, d'apport, de construction ou autrement.",
                "Laboratoire d'analyses de biologie médicale",
                "Restaurant rapide et traditionnel, à emporter, sur place et en livraison"
               ]
        codeNaF = ["" for _ in des]
        csvdesc = pd.DataFrame(data={"codeNaf":codeNaF, "description":des})
        print csvdesc
                   
        tab = KeywordSelector.pipeline(csvdesc, 20, True)
        for t in tab:
            print t

main("main pipeline")
