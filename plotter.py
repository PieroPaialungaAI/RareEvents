import numpy as np 
import matplotlib.pyplot as plt
from constants import * 
from scipy.stats import genextreme, norm
import pandas as pd


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


def qq_plotter(osm, osr, dist_name, key):
    plt.figure(figsize=(6, 6))
    plt.scatter(osr, osm, label='Empirical vs. Theoretical Quantiles', alpha=0.7)
    min_val, max_val = min(osr.min(), osm.min()), max(osr.max(), osm.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', label='Ideal Fit Line')
    plt.xlabel('Theoretical Quantiles')
    plt.ylabel('Empirical Quantiles')
    plt.title(f'Q–Q Plot: {dist_name.upper()} Fit for {key.capitalize()} Maxima')
    plt.legend()
    plt.grid(True)
    plt.show()


def timeseries_plotter(data, city):
    y = np.array(data[city])
    x = np.array(pd.to_datetime(data['datetime']))
    plt.figure(figsize=(10, 4))
    plt.plot(x, y, color = 'navy')
    plt.title(f'Time Series for city = {city}')
    plt.xlabel('Time')
    plt.ylabel('Temperature (K)')
    plt.grid(True)
    plt.show()


def timeseries_dist_plotter(data, city):
    x = np.array(data[city].dropna())
    
    # Fit a Gaussian to the data
    mu, std = norm.fit(x)
    
    # Create range for the PDF
    xmin, xmax = min(x), max(x)
    x_range = np.linspace(xmin, xmax, 1000)
    pdf = norm.pdf(x_range, mu, std)

    # Plot histogram with density=True (normalized)
    plt.figure(figsize=(10, 4))
    plt.hist(x, bins=50, color='lightgray', edgecolor='black', density=True, alpha=0.6, label='Histogram')

    # Plot the fitted Gaussian
    plt.plot(x_range, pdf, 'r-', lw=2, label=f'Gaussian Fit\nμ={mu:.2f}, σ={std:.2f}')

    # Aesthetic adjustments
    plt.title(f'Fitted Distribution for {city}')
    plt.xlabel('Temperature (K)')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    