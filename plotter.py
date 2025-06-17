import numpy as np 
import matplotlib.pyplot as plt
from constants import * 

def distribution_plotter(max_values_dict, image_path = DEFAULT_IMAGE_PATH):
    count = 1 
    n = len(max_values_dict)
    plt.figure(figsize = IMAGE_FIGSIZE)
    for key in max_values_dict:
        plt.subplot(n,1,count)
        plt.title(key + ' Max Value')
        plt.hist(max_values_dict[key], color ='darkorange', bins  = 20)
        count += 1 
    plt.tight_layout()
    plt.savefig(image_path)
    