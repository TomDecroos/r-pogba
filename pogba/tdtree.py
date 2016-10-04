'''
Created on Oct 4, 2016

@author: tomd
'''
from sklearn.neighbors.unsupervised import NearestNeighbors
from pprint import pprint
import numpy as np
from pogba.dtw import dtwphase
from tools.functional import snd, fst
import math

class TDTree(object):
    
    def __init__(self,phases):
        self.phases = phases
        lb_kim = map(getlbkim, self.phases)
        self.kimtree = NearestNeighbors(p=2)
        self.kimtree.fit(lb_kim)
    
    def getnn(self,phase,k=5):
        q = np.array(getlbkim(phase)).reshape((1,-1))
        (inds,) = self.kimtree.kneighbors(q, n_neighbors=k, return_distance=False)
        
        nns = [self.phases[index] for index in inds]
        maxdtw = max([dtwphase(phase, nn) for nn in nns])
        
        (inds,) = self.kimtree.radius_neighbors(q, radius=math.sqrt(maxdtw),
                                                return_distance = False)
        print len(inds)
        nns = [self.phases[index] for index in inds]
        nns = sorted([(dtwphase(phase, nn), nn) for nn in nns], key = fst)
        
        return nns[0:k]
        

def getlbkim(phase):
    x,y = phase.correctedcoords()
    return list(get4S(x)) + list(get4S(y))


def get4S(x):
    return x[0],x[-1],min(x),max(x)
        

