import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import weibull_min, weibull_max, genextreme, norm, probplot, skew, gumbel_r, gumbel_l
class Distribution():
    def __init__(self, dist_type, data):
        self.dist_type = dist_type
        self.data = data
        

    def distribution_builder(self):
        if self.dist_type == 'gev':
            params = genextreme.fit(self.data)
            dist_name = self.dist_type
        elif self.dist_type == 'weibull':
            min_or_max = self.choose_tail()
            dist_name = 'weibull_' + min_or_max
            if min_or_max == 'max':
                dist = weibull_max
            elif min_or_max == 'min':
                dist = weibull_min
            params = dist.fit(self.data)
        elif self.dist_type == 'gumbel':
            min_or_max = self.choose_tail()
            dist_name = 'gumbel_' + min_or_max
            if min_or_max == 'max':
                dist = gumbel_r
            else:
                dist = gumbel_l
            params = dist.fit(self.data)
        res = {'dist_type':dist_name, 'param':params}
        self.distribution = res
        return res



    def choose_tail(self):
        data = np.asarray(self.data)
        data = data[~np.isnan(data)]  # Clean NaNs
        data = data[np.isfinite(data)]  # Clean infs
        
        if len(data) < 3:
            raise ValueError("Insufficient data to compute skewness.")
        
        data_skew = skew(data)

        if data_skew >= 0:
            return "min"
        elif data_skew < 0:
            return "max"


