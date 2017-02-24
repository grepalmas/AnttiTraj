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
    
    ksize = None
    ksizeL = findArg(args, "-ksize")
    if len(ksizeL) > 0:
        ksize = float(ksizeL[0])

    color1 = [1,0,0,0]
    color1L = findArg(args, "-color1")
    if len(color1L) >= 4:
        for i in range(4):
            color1[i] = float(color1L[i])

    color2 = [1,0,0,1]
    color2L = findArg(args, "-color2")
    if len(color2L) >= 4:
        for i in range(4):
            color2[i] = float(color2L[i])

    filter = "catrom"
    filterL = findArg(args, "-imgfilter")
    if len(filterL) > 0:
        filter = filterL[0]

    showcont = indexOf(args, "-showcontours") > -1

    flipx = indexOf(args, "-flipx") > -1
    flipy = indexOf(args, "-flipy") > -1

    #Heatmap.MakeHeatMap(filePaths, listCols, filePath, stat, resolution, screenshot)
    kdegen.MakeHeatMapKDE(filePaths, listCols, stat, resolution, ksize, color1, color2, filter , screenshot, dpi, gamma, showcont, flipx, flipy)
    

if __name__ == "__main__":
   main(sys.argv)
