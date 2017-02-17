
import numpy as np

def GetData(path):

  data = np.genfromtxt(path, dtype = None, delimiter = ",", names = True)
  return data;
  
  #addCol = 

  