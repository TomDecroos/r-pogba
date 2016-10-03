'''
Created on 15 Feb 2016

@author: pierre-rouanet
https://github.com/pierre-rouanet/dtw/blob/master/dtw.py
'''
from numpy import zeros, inf


def dtw(x, y, dist):
    """
    Computes Dynamic Time Warping (DTW) of two sequences.
    """
    r, c = len(x), len(y)
    D0 = zeros((r + 1, c + 1))
    D0[0, 1:] = inf
    D0[1:, 0] = inf
    D1 = D0[1:, 1:] # view
    for i in range(r):
        for j in range(c):
            D1[i, j] = dist(x[i], y[j])
    for i in range(r):
        for j in range(c):
            D1[i, j] += min(D0[i, j], D0[i, j+1], D0[i+1, j])
    return float(D1[-1, -1])/ (r*c)

def dtweuclid(x,y):
    return dtw(x,y,lambda x,y:(x-y)*(x-y))
def dtwmanhattan(x,y):
    return dtw(x,y,lambda x,y:abs(x-y))

def dtwphase(phase1,phase2,dtwfn=dtweuclid):
    x1,y1 = phase1.correctedcoords()
    x2,y2 = phase2.correctedcoords()
    result = dtwfn(x1,x2) + dtwfn(y1,y2)
    return result