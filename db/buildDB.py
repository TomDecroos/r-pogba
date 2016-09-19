'''
Created on Sep 19, 2016

@author: tomd
'''
import xml.etree.ElementTree as ET
import os
from db.tools import logmap

def extract_competition(root):
    return root.attrib['competition'],root.attrib['competition_id']
def test():
    import time
    import sys

    for i in range(100):
        time.sleep(0.1)
        print "\r %d" % i
        print
        #sys.stdout.write("\r%d%%" % i)
        #sys.stdout.flush()
if __name__ == '__main__':
    import config
    all_matches = logmap(lambda x: config.optaf21 + x,os.listdir(config.optaf21))
    f = lambda x: extract_competition(ET.parse(x).getroot())
    #logmap(lambda x: time.sleep(0.001),range(1,1000))
    print set(logmap(f,all_matches))