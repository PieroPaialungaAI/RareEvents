import numpy as np 
import matplotlib.pyplot as plt
from constants import * 
from scipy.stats import genextreme


def distribution_plotter(max_values_dict, image_path = DEFAULT_IMAGE_PATH):
    count = 1 
    n = len(max_values_dict)
    plt.figure(figsize = IMAGE_FIGSIZE)
    for key in max_values_dict:
        plt.subplot(n,1,count)
        plt.title(key + ' Max Value')
        plt.hist(max_values_dict[key], color ='darkorange', bins  = BIN_NUMBER)
        count += 1 
    plt.tight_layout()
    plt.savefig(image_path)
    


def gev_plotter(data, c, loc, scale, bins=BIN_NUMBER):
    """
    Plot the histogram of data and the fitted GEV PDF.

    Parameters:
    - data: array-like, the observed data (e.g., yearly maxima)
    - c: shape parameter from GEV fit
    - loc: location parameter from GEV fit
    - scale: scale parameter from GEV fit
    - bins: number of bins for the histogram
    """
    x = - np.linspace(min(data), max(data), 10_000)
    pdf = genextreme.pdf(x, c, loc=loc, scale=scale)

    plt.figure(figsize=IMAGE_FIGSIZE)
    plt.hist(-data, bins= bins, density=True, alpha=0.6, color='gray', label='Empirical histogram')
    plt.plot(x, pdf, 'r-', lw=2, label='GEV fit')
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.title('GEV Fit to Maximum Value Distribution')
    plt.legend()
    plt.grid(True)
    plt.show()