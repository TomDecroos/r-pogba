'''
Created on Oct 4, 2016

@author: tomd
'''
from tools.dbhelper import Connection
import config
from db.qry import getmatchids
from core.phase import getallphases
from tools.timefn import Timer
from pogba.tdtree import TDTree
from explore.phase import comparephases
from pogba.vptree import VPTree, get_nearest_neighbors
from pogba.dtw import dtwphase


def tdvsvp(phases, phase, k):
    with Timer("building td tree"):
        tdtree = TDTree(phases)
    with Timer("finding td nn"):
        tdnn = tdtree.getnn(phase, k)
    
    print "total td dist :", sum([dtwphase(phase, p) for d,p in tdnn])
    
    with Timer("building vp tree"):
        vptree = VPTree(phases, dtwphase)
    with Timer("finding vp nn"):
        vpnn = get_nearest_neighbors(vptree, phase, k)
    
    print "total vp dist :", sum([dtwphase(phase, p) for d,p in vpnn])

def exploretd(phases,phase, k):
    with Timer("building tree"):
        tree = TDTree(phases)
    with Timer("finding neighbours"):
        nns = tree.getnn(phase,k)
    for dist,nn in nns:
        comparephases(phase, nn)
        
if __name__ == '__main__':
    with Connection(config.epl2012db) as c:
        ids = getmatchids(c)
        with Timer("getting phases"):
            phases = getallphases(c, ids, relevant=True)
            print "nb of phases: ", len(phases)
        #exploretd(phases, phases[50], 100)
        tdvsvp(phases, phases[50], 100)
        
