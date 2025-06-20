import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import weibull_min, genextreme, norm, probplot

class Distribution():
    def __init__(self, dist_type):
        