import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
from constants import * 

class Data:
    def __init__(self, data_path = DEFAULT_DATA_PATH, data_file = DEFAULT_DATA_FILE):
        self.data_path = data_path
        self.data_file = data_file
        self.raw_data = self.load_data_path()

    def all_cities(self):
        all_columns = set(self.raw_data.columns.tolist())
        all_columns.remove('datetime')
        all_columns = list(all_columns)
        self.cities = all_columns
        return self.cities

    
    def load_data_path(self):
        return pd.read_csv(self.data_path+self.data_file)
    

    def isolate_city(self, city):
        self.processed_data = self.raw_data[[city, 'datetime']]
        self.city = city
        return self.processed_data
    

    def clean_and_preprocess(self):
        self.processed_data = self.processed_data.dropna()
        self.processed_data['datetime'] = pd.to_datetime(self.processed_data['datetime'])
        self.processed_data = self.processed_data.rename(columns = {self.city: 'y'})
        self.processed_data['date'] = self.processed_data['datetime'].dt.date
        self.processed_data['month'] = self.processed_data['datetime'].dt.month
        self.processed_data['year'] = self.processed_data['datetime'].dt.year
        return self.processed_data
    


