'''
Created on Oct 6, 2016

@author: tomd
'''
import matplotlib.pyplot as plt
import config
from tools.dbhelper import Connection
from db.qry import getmatchids
from core.phase import getmatchphases
import pickle
from core.rating import pogba, isgoal, expgoal
from explore.phase import plotphase
from tools.timefn import Timer
from pogba.vptree import VPTree
from tools.functional import logmap
    
def console(c):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-matchnb", nargs="?", type=int, default=0)
    parser.add_argument("-k", nargs="?", type=int, default=50)
    parser.add_argument('-plot', action = 'store_const', const=True,
                        default= False)
    parser.add_argument('-event', nargs ="?")
    parser.add_argument('-isgoal', action = 'store_const', const=True,
                        default= False)
    parser.add_argument('-expgoal', action = 'store_const', const=True,
                        default= False)
    parser.add_argument('-pogba', action = 'store_const', const=True,
                        default= False)
    parser.add_argument('-sum', action = 'store_const', const=True,
                        default= False)
    args = parser.parse_args()
    
    with Timer("loading phases"):
        ids = getmatchids(c)
        phases = getmatchphases(c,ids[args.matchnb],relevant=True)
    if args.pogba:
        with open(config.phasetree,'rb') as fh, Timer('loading phasetree'):
            phasetree = pickle.load(fh)
    if args.expgoal:
        with open(config.xgmodel,'rb') as fh, Timer('loading xgmodel'):
            xgmodel = pickle.load(fh)
    if args.pogba:
        if args.expgoal:
            def ratefn(x):
                return pogba(x,phasetree,args.k,lambda x: expgoal(x,xgmodel))
        else:
            def ratefn(x):
                return pogba(x,phasetree,args.k,isgoal)
    elif args.isgoal:
        ratefn = isgoal
    elif args.expgoal:
        def ratefn(x):
            return expgoal(x,xgmodel)
    else:
        raise Exception("no ratefunction specified")
    
    if args.event:
        phases = filter(lambda x: x.hasevent(args.event), phases)
    
    if args.sum:
        print "total rating: %.5f" % sum(map(abs,logmap(ratefn,phases)))
    else:
        for phase in phases:
            print 'rating:', ratefn(phase)
            if args.plot:
                fig,ax = plt.subplots()
                plotphase(ax,phase)
                plt.show()
            
if __name__ == '__main__':
    with Connection(config.epl2012db) as c:
        console(c)
