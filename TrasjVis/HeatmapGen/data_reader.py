
import numpy as np

def GetData(path):

  data = np.genfromtxt(path, dtype = None, delimiter = ",", names = True)
  modeln = data["model.n"]
  taskn = data["task"]
  
  #addCol = 

  