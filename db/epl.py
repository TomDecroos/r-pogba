'''
Created on Sep 22, 2016

@author: tomd
'''

import os
import pickle

import config
import xml.etree.ElementTree as ET
from tools.functional import logfilter


def is_epl_match(matchfile):
    root = ET.parse(matchfile).getroot()
    return int(root.attrib['competition_id']) == config.epl_id


def save_epl_matches():
    matchfiles = [config.optaf21 + m for m in os.listdir(config.optaf21)]
    epl_mfs = logfilter(is_epl_match, matchfiles)
    pickle.dump(epl_mfs, open(config.epl_matches, 'wb'))

if __name__ == '__main__':
    save_epl_matches()