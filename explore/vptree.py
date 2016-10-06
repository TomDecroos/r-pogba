'''
Created on Oct 3, 2016

@author: tomd
'''

import config

from core.phase import getmatchphases, getallphases
from db.qry import getmatchids
from tools.dbhelper import Connection
from tools.functional import logmap
from tools.timefn import Timer
from pogba.vptree import VPTree, get_nearest_neighbors
from pogba.dtw import dtwphase
from explore.phase import comparephases
import pickle



if __name__ == '__main__':
    with Connection(config.epl2012db) as c:
        ids = getmatchids(c)
        with Timer("getting phases"):
            phases = getallphases(c, ids[78:100])
    print "n: %d" % len(phases)
    with open(config.phasetree,'rb') as fh,Timer("loading tree"):
        tree = pickle.load(fh)
    with Timer("finding neighbours"):
        k = 50
        q = phases[50]
        nn = get_nearest_neighbors(tree,q,k=k)
    for i in range(0,k):
        comparephases(q,nn[i][1])