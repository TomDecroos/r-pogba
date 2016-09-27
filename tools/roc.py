'''
Created on Sep 27, 2016

@author: tomd
'''
import matplotlib.pyplot as plt
from sklearn.metrics.ranking import roc_curve

def plot_roc_curve(y_true,y_pred):
    a,b,_thresholds = roc_curve(y_true,y_pred)
    plt.plot(a,b,c="green",label="model 1")
    plt.legend(loc=4)
    plt.show()
    