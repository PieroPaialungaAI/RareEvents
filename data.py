import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
from constants import * 

class Data:
    def __init__(self, data_path = DEFAULT_DATA_PATH, data_file = DEFAULT_DATA_FILE):
        self.data_path = data_path
        self.data_file = data_file
        self.raw_data = self.load_data_path()

    
    def load_data_path(self):
        return pd.read_csv(self.data_path+self.data_file)
    

    def isolate_city(self, city):
        self.processed_data = self.raw_data[[city, 'datetime']]
        return self.processed_data
    
