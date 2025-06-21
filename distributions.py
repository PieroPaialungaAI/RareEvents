import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import weibull_min, weibull_max, genextreme, norm, probplot, skew, gumbel_r, gumbel_l
class Distribution():
    def __init__(self, dist_type, data):
        self.dist_type = dist_type
        self.data = data
        

    def distribution_builder(self):
        if self.dist_type == 'gev':
            dist = genextreme
            params = dist.fit(self.data)
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
            if min_or_max == 'min':
                dist = gumbel_l
                dist_name = 'gumbel_max'
            else:
                dist_name = 'gumbel_min'
                dist = gumbel_r

            params = dist.fit(self.data)
        self.dist = dist
        self.params = params
        res = {'dist_type':dist_name, 'param':params, 'dist':dist}
        self.distribution = res
        return res


    def score_distribution(self):
        data = np.asarray(self.data)
        data = data[~np.isnan(data)]
        data = data[np.isfinite(data)]

        n = len(data)
        k = len(self.params)

        log_likelihood = np.sum(self.dist.logpdf(data, *self.params))
        aic = 2 * k - 2 * log_likelihood
        bic = k * np.log(n) - 2 * log_likelihood

        return {
            'log_likelihood': log_likelihood,
            'aic': aic,
            'bic': bic
        }



    def choose_tail(self):
        data = np.asarray(self.data)
        data = data[~np.isnan(data)]  # Clean NaNs
        data = data[np.isfinite(data)]  # Clean infs
        
        if len(data) < 3:
            raise ValueError("Insufficient data to compute skewness.")
        
        data_skew = skew(data)

        if data_skew >= 0:
            return "max"
        elif data_skew < 0:
            return "min"


