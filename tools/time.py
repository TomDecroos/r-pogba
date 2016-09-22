'''
Created on Sep 22, 2016

@author: tomd
'''
def mintosec(minute, second=0):
    return int(60 * minute + second)

def sectomin(seconds):
    return int(seconds/60), int(seconds %60)
 
def floattodigital(minute):
    return sectomin(mintosec(minute))

def eventsec(e):
    return mintosec(e['minute'],e['second'])