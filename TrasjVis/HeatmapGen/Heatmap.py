
import matplotlib.pyplot as plt
import numpy as np

def MakeHistogram(filePaths, dimensions, res, stat):
    
    
    
    xedges = []
    yedges = []   
    
    histograms = []
    maxNormValue = -1    

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
        bbox = [[min(xcolumn) - 1, max(xcolumn) +1 ], [min(ycolumn) - 1, max(ycolumn) + 1]];

        histogram, xedge, yedge = np.histogram2d(xcolumn,ycolumn, bins = res , range = bbox, weights = dataColumn)
        
        if stat == "mean":
            
            histogramCount, xedgesCount, yedgesCount = np.histogram2d(xcolumn, ycolumn, bins = res, range = bbox)
            histogramCount[histogramCount == 0] = 1

            histogram = np.divide(histogram, histogramCount)

        histogram = np.rot90(histogram)
        histograms.append(histogram)
        maxNormValue = max(maxNormValue, histogram.max())
        xedges.append(xedge)
        yedges.append(yedge)

    return histograms, xedges, yedges, maxNormValue

def MakeHeatMap(filePaths, dimensions, filepath, stat, res, screenshot = True):
    
    if len(dimensions) < 2:
        return
    

    histograms, xedges_arr, yedges_arr, normvalue = MakeHistogram(filePaths, dimensions, res, stat)

    methods = ['none', 'nearest', 'bilinear', 'bicubic', 'spline16',
               'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
               'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos','gaussian']    
    

    
    for (i, histogram) in enumerate(histograms):
        
        xedges = xedges_arr[i]
        yedges = yedges_arr[i]
        
        histogram_norm = np.divide(histogram, normvalue)         
        histo_bounds = [histogram.min(), histogram.max()]
        
        for method in methods:
            
            fig, ax = plt.subplots()

            heatmap = ax.imshow(histogram_norm, interpolation = method, extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]], filterrad = 2.0, cmap='Reds')
            cbar = plt.colorbar(heatmap, ticks = [0,0.5,1])
            cbar.ax.set_yticklabels([str(histo_bounds[0]), str((histo_bounds[0] + histo_bounds[1])/2),str(histo_bounds[1])])

            if screenshot:
                fig_path = filepath.replace(".csv","_"+method+".png")

                fig.tight_layout()

                plt.savefig(fig_path, bbox_inches = 'tight',pad_inches=0, dpi=120, format = 'png');

            else: plt.show()

            plt.close(fig)