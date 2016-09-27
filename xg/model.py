'''
Created on Sep 26, 2016

@author: tomd
'''
from tools.dbhelper import Connection
import config
from pprint import pprint
from tools.geometry import Point
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from tools.functional import logmap
import numpy as np
import pickle
from sklearn.metrics.ranking import roc_auc_score

goalhome = Point(0,0.5)
goalaway = Point(1,0.5)

def getshots(c):
    qry = """select event.rowid, *
    from event natural join eventtype
    where name = "goal"
    or name = "miss"
    or name = "post"
    or name = "attempt saved"
    """
    rows = c.execute(qry).fetchall()
    return rows

def getfeatures(shot):
    p = Point(shot['x'], shot['y'])
    v1 = p.vector(goalhome)
    v2 = p.vector(goalaway)
    v = min([v1,v2],key=lambda x: x.abs())
    return [v.abs(),abs(v.angle())]

def savexgmodel(c, fh):
    shots = getshots(c)
    X = np.array(map(getfeatures, shots))
    y = np.array(map(lambda x: x['name']=="goal", shots))
    model = LogisticRegression()
    model.fit(X,y)
    pickle.dump(model, fh)

def testxgmodel(c, fh):
    shots = getshots(c)
    X = np.array(map(getfeatures, shots))
    y = np.array(map(lambda x: x['name']=="goal", shots))
    model = pickle.load(fh)
    y_pre = model.predict_proba(X)[:,1]
    print "ROC AUC: %.3f" % roc_auc_score(y,y_pre)

if __name__ =='__main__':
    with Connection(config.epl2012db) as c:
        with open(config.xgmodel,'wb') as fh:
            savexgmodel(c, fh)
        with open(config.xgmodel,'rb') as fh:
            testxgmodel(c, fh)