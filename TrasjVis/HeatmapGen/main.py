import sys
import os.path
import numpy as np

import Heatmap
import kdegen

def indexOf(list, value, start = 0):
    try:
        return list.index(value, start)
    except ValueError:
        return -1

def indexOf(list, value, start = 0, end = -1):
    try:
        
        idx = list.index(value, start)
        if end > -1 and idx > end:
            idx = -1

        return idx

    except ValueError:
        return -1

def findArg(list, arg):
    idx  = indexOf(list,arg)
        
    res = []
    if idx >-1:
         
        i = idx+1
        cont  = i < len(list)
        while cont:
            res.append(list[i])
            i = i+1
            cont = i < len(list)
            if cont:
                cont = cont and "-" not in list[i]
    return res

def main(args):
    
    NumArgs = len(args)
    if NumArgs <= 1:
        return    

    filePaths = []
   
    
    folderPathL = findArg(args, "-open")

    folderPath = ""
    if len(folderPathL) > 0:
        folderPath = folderPathL[0]

    for filePath in os.listdir(folderPath):
        if filePath.endswith(".csv"):
            filePaths.append(folderPath + "/" + filePath) 


    listCols = findArg(args, "-vis")
    
    screenshot = indexOf(args, "-screenshot") > -1
    
    dpi = 120
    dpiL = findArg(args, "-dpi")
    if len(dpiL) > 0:
        dpi = int(dpiL[0])

    #visIdx = indexOf(args,"-vis",0)
    #screenshot = indexOf(args,"-screenshot",0) >= 0

    #listCols = []
    #i  = visIdx + 1;

    #resolution = [1,1]
    #stat = "count"

    #while args[i] != "-vis" and args[i] != "-open" and args[i] != "-res" and args[i] != "-stat" and args[i] != "-screenshot" and i < NumArgs:
        
    #    listCols.append(args[i])

    #    i = i+1;
    #    if i >= NumArgs:
    #        break

    resolution = [0,0]
    resolutionL = findArg(args,"-res")
    if len(resolutionL) > 0:
        resolution = [int(resolutionL[0]), int(resolutionL[1])]
        
    stat = "sum"
    statL = findArg(args,"-stat")
    if len(statL) > 0:
        stat = statL[0]

    gamma = 1
    gammaL = findArg(args,"-gamma")
    if len(gammaL[0]):
        gamma = float(gammaL[0])
    

    #Heatmap.MakeHeatMap(filePaths, listCols, filePath, stat, resolution, screenshot)
    kdegen.MakeHeatMapKDE(filePaths, listCols, stat, resolution, screenshot, dpi, gamma)
    

if __name__ == "__main__":
   main(sys.argv)
