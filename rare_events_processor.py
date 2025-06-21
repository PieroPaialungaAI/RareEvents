import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
from constants import * 
from plotter import * 
from distributions import * 

class RareEventsToolbox():
    def __init__(self, data):
        self.data = data 
        datetime = self.data['datetime']
        self.unique_days = set(datetime.dt.date)
        self.unique_months = set(zip(datetime.dt.year, datetime.dt.month))
        self.unique_years = set(datetime.dt.year)
        self.distribution_fit = {}

    def extract_block_max(self, key = 'day'):
        if key == 'day':
            max_value = np.zeros(len(self.unique_days))
            count = 0
            for day in self.unique_days:
                isolated_segment = self.data[self.data['date'] == day]
                max_value[count] = np.array(isolated_segment['y']).max()
                count += 1
        elif key == 'month':
            max_value = np.zeros(len(self.unique_months))
            count = 0
            for element in self.unique_months:
                year, month = element[0], element[1]
                isolated_segment =  self.data[(self.data['month'] == month) & (self.data['year'] == year)]
                max_value[count] = np.array(isolated_segment['y']).max()
                count += 1 
        else:
            max_value = np.zeros(len(self.unique_years))
            count = 0
            for year in self.unique_years:
                isolated_segment =  self.data[self.data['year'] == year]
                max_value[count] = np.array(isolated_segment['y']).max()
                count += 1 
        return max_value
    

    def extract_max_values(self, keys = KEYS):
        self.max_values_dict = {k : [] for k in keys}
        for k in keys:
            self.max_values_dict[k] = self.extract_block_max(key = k)
        return self.max_values_dict
    
    def plot_distributions(self):
        distribution_plotter(self.max_values_dict)


    def fit_max_distribution(self, dist_type, keys = KEYS):
        for k in keys:
            dist = Distribution(dist_type = dist_type, data = self.max_values_dict[k])
            distribution_fit = dist.distribution_builder()
            if dist_type not in self.distribution_fit:
                self.distribution_fit[dist_type] = {}
            self.distribution_fit[dist_type][k] = distribution_fit
            self.distribution_fit[dist_type][k]['metrics'] = dist.score_distribution()
        return self.distribution_fit


    def plot_fitted_distribution(self, key, dist_type):
        if dist_type not in self.distribution_fit or key not in self.distribution_fit[dist_type]:
            raise ValueError(f"No fitted distribution found for {dist_type} with key {key}.")

        fit_info = self.distribution_fit[dist_type][key]
        data = self.max_values_dict[key]
        dist_name = fit_info['dist_type']
        params = fit_info['param']
        dist = fit_info['dist']

        # Create x-values for PDF
        x = np.linspace(min(data), max(data), 1000)
        pdf = dist.pdf(x, *params)

        # Plot
        plt.figure(figsize=(8, 5))
        plt.hist(data, bins=30, density=True, alpha=0.6, label='Empirical Data')
        plt.plot(x, pdf, 'r-', label=f'Fitted {dist_name.upper()}')
        plt.title(f'{dist_name.upper()} Fit for {key.capitalize()} Maxima')
        plt.xlabel('Value')
        plt.ylabel('Density')
        plt.legend()
        plt.grid(True)
        plt.show()


    