import custom_stats
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import colorConverter

import statsmodels.api as sm
from scipy import stats

import os;

def MakeKDE(filePaths, dimensions, res, stat, kernelsize):

    densities = []
    maxNormValue = -1    

    extents_x = []
    extents_y = []

    bandwidth_param = kernelsize

    if len(dimensions) < 2:
        return

    for filePath in filePaths:
        
        data = np.genfromtxt(filePath, dtype = None, delimiter = ",", names = True)
        xcolumn = data[dimensions[0]]
        ycolumn = data[dimensions[1]]    

        dataColumn = np.array([])
        if len(dimensions) > 2:
            dataColumn = data[dimensions[2]]
        else:
            dataColumn = np.ones(len(xcolumn))

        #bbox = [[min(xcolumn) - 1, min(ycolumn) -1 ], [max(xcolumn) + 1, max(ycolumn) + 1]];
        #bbox = [[min(xcolumn) - 1, max(xcolumn) +1 ], [min(ycolumn) - 1, max(ycolumn) + 1]];
        
        X, Y = np.mgrid[xcolumn.min():xcolumn.max():res[0]*1j, ycolumn.min():ycolumn.max():res[1]*1j]
        
        positions = np.vstack([X.ravel(), Y.ravel()])
        #positions = np.vstack([xcolumn, ycolumn])

        kde_res = custom_stats.gaussian_kde([xcolumn, ycolumn], weights = dataColumn, bw_method = bandwidth_param)
        #kde_res = stats.gaussian_kde([xcolumn, ycolumn], bw_method = bandwidth_param)
        
        kde_values = kde_res(positions)
        
        extents_x.append([xcolumn.min(),xcolumn.max()])
        extents_y.append([ycolumn.min(),ycolumn.max()])

        if stat == "mean":
            
            kde_resCount = custom_stats.gaussian_kde([xcolumn, ycolumn], bw_method = bandwidth_param)
            kde_Countvalues = kde_resCount(positions)
            kde_Countvalues[kde_Countvalues == 0] = 1
            kde_values = np.divide(kde_values, kde_Countvalues)
            
        maxNormValue = max(maxNormValue, kde_values.max())
        kde_values = np.reshape(kde_values.T, X.shape)
        kde_values = np.rot90(kde_values)
        #kde_values = np.flipud(kde_values)
        #kde_values = np.reshape(kde_values.T, (len(xcolumn),len(ycolumn)))

        densities.append(kde_values)

    return densities, extents_x, extents_y, maxNormValue

def GetColorMap(color1, color2):

    cmap = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',[color1, color2],256)
    cmap._init()
    return cmap

#def MakeKDE2(filePaths, dimensions, res, stat):

#    densities = []
#    maxNormValue = -1    

#    extents_x = []
#    extents_y = []

#    bandwidth_param = 0.3

#    if len(dimensions) < 2:
#        return

#    for filePath in filePaths:
        
#        data = np.genfromtxt(filePath, dtype = None, delimiter = ",", names = True)
#        xcolumn = data[dimensions[0]]
#        ycolumn = data[dimensions[1]]    

#        dataColumn = np.array([])
#        if len(dimensions) > 2:
#            dataColumn = data[dimensions[2]]
#        else:
#            dataColumn = np.ones(len(xcolumn))

#        #bbox = [[min(xcolumn) - 1, min(ycolumn) -1 ], [max(xcolumn) + 1, max(ycolumn) + 1]];
#        #bbox = [[min(xcolumn) - 1, max(xcolumn) +1 ], [min(ycolumn) - 1, max(ycolumn) + 1]];
        
#        kdeFunc = sm.nonparametric.KDEMultivariate(data=[xcolumn,ycolumn], var_type='cc', bw='normal_reference')
#        kdeFunc.cdf(weights = dataColumn)
#        kdeValues = kdeFunc.density

#        if stat == "mean":
            
#            kdeFuncCount = sm.nonparametric.KDEMultivariate(data=[xcolumn,ycolumn], var_type='cc', bw='normal_reference')
#            kdeFuncCount.fit()
#            #kde_resCount = stats.gaussian_kde([xcolumn, ycolumn], bw_method = bandwidth_param)
#            kde_Countvalues = kdeFuncCount.density
#            kde_values = np.divide(kde_values, kde_Countvalues)
#            kde_values[kde_values == np.nan] = 0
        

#        maxNormValue = max(maxNormValue, kde_values.max())
#        #kde_values = np.flipud(kde_values)
#        #kde_values = np.reshape(kde_values.T, (len(xcolumn),len(ycolumn)))

#        densities.append(kde_values)

    #return densities, extents_x, extents_y, maxNormValue

def MakeHeatMapKDE(filePaths, dimensions, stat, res, kernelsize, color1, color2, filter, screenshot = True, dpi_arg = 120, gamma = 1.0):
    
    if len(dimensions) < 2:
        return
    

    densities, extents_x, extents_y, normvalue = MakeKDE(filePaths, dimensions, res, stat, kernelsize)

    #methods = ['none', 'nearest', 'bilinear', 'bicubic', 'spline16',
    #           'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
    #           'catrom', 'bessel', 'mitchell', 'sinc', 'lanczos','gaussian']    
    methods = ['catrom']    
    
    
    
    for (i, density) in enumerate(densities):
        
        picData = np.array([])        

        uiPicPath = filePaths[i].replace(".csv",".png")
        if os.path.isfile(uiPicPath):
            picData = plt.imread(uiPicPath)
            

        density_gamma = np.power(density, 1.0/gamma)
        norm_gamma = pow(normvalue, 1.0/gamma)    

        density_norm = np.divide(density_gamma, norm_gamma)         
        #density_bounds = [density.min(), density.max()]
        
        color_map = GetColorMap(color1,color2)

        fig, ax = plt.subplots()

        if len(picData) > 0:
            ax.imshow(picData, interpolation = "none", extent=[extents_x[i][0],extents_x[i][-1], extents_y[i][0],extents_y[i][-1]])
        heatmap = ax.imshow(density_norm, interpolation = filter, extent=[extents_x[i][0],extents_x[i][-1], extents_y[i][0],extents_y[i][-1]], filterrad = 2.0, cmap=color_map)
        
        #cbar = plt.colorbar(heatmap, ticks = [0,0.5,1])
        #cbar.ax.set_yticklabels([str(density_bounds[0]), str((density_bounds[0] + density_bounds[1])/2),str(density_bounds[1])])

        if screenshot:
            fig_path = filePaths[i].replace(".csv","_"+filter+".png")

            fig.tight_layout()

            plt.savefig(fig_path, bbox_inches = 'tight',pad_inches=0, dpi=dpi_arg, format = 'png');

        else: plt.show()

        plt.close(fig)