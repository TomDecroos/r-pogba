'''
Created on Sep 22, 2016

@author: tomd
'''
from xg.model import getfeatures
import numpy as np

def isgoal(phase):
    goals = filter(lambda x: x['name'] == 'goal', phase.events)
    home = 1 if filter(lambda x: x['teamid'] == phase.hometeamid, goals) else 0
    away = 1 if filter(lambda x: x['teamid'] == phase.awayteamid, goals) else 0
    return home - away

def expgoal(phase,xgmodel):
    home, away = 0,0
    def is_shot(x):
        return x['name'] in ['goal','attempt saved','miss','post']
    shots = filter(is_shot, phase.events)
    if shots:
        X = np.array(map(getfeatures,shots))
        if len(shots)==1: #create
            X.reshape(1,-1)
        xgs = xgmodel.predict_proba(X)[:,1]
        home, away = 0, 0
        for xg, shot in zip(xgs,shots):
            if shot['teamid'] == phase.hometeamid:
                home += xg
            if shot['teamid'] == phase.awayteamid:
                away += xg
    return home - away

def pogba(phase):
    return 0