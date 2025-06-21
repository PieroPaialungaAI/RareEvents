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
    

    def fit_max_distribution(self, dist_type, keys = KEYS):
        for k in keys:
            dist = Distribution(dist_type = dist_type, data = self.max_values_dict[k])
            distribution_fit = dist.distribution_builder()
            self.distribution_fit[dist_type] = distribution_fit
        return self.distribution_fit

    
    def plot_fitted_distributions(self, key = 'day'):
        gev_plotter(self.max_values_dict[key], self.max_values_fit[key]['c'], self.max_values_fit[key]['loc'],
                    self.max_values_fit[key]['scale'])
        


    def plot_distributions(self):
        distribution_plotter(self.max_values_dict)


    