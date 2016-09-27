'''
Created on Sep 22, 2016

@author: tomd
'''

import os
import pickle

import config
import xml.etree.ElementTree as ET
from tools.functional import logfilter, logmap
from pprint import pprint


def is_epl_match(matchid):
    root = ET.parse(eventsfile(matchid)).getroot()
    return int(root.attrib['competition_id']) == config.epl_id

def save_epl_matches():
    matchids = map(lambda x: x.replace("-events.xml",""),
                   os.listdir(config.optaf21mixed))
    matchids = map(int,matchids)
    epl_mfs = logfilter(is_epl_match, matchids)
    pickle.dump(epl_mfs, open(config.epl_matches, 'wb'))

def eventsfile(matchid):
    return config.optaf21mixed + str(matchid) + "-events.xml"

def statisticsfile(matchid):
    return config.optaf9mixed + str(matchid) + "-statistics.xml"

def is_from_season(matchid, seasonid):
    root = ET.parse(eventsfile(matchid)).getroot()
    return int(root.attrib['season_id']) == seasonid

def get_seasonid(matchid):
    root = ET.parse(eventsfile(matchid)).getroot()
    return root.attrib['season_id'], root.attrib['season']

if __name__ == '__main__':
    save_epl_matches()
    #matchids =  pickle.load(open(config.epl_matches,'rb'))
    #seasons = logmap(get_seasonid,matchids)
    #pprint(set(seasons))
