'''
Created on Sep 22, 2016

@author: tomd
'''
import time

def mintosec(minute, second=0):
    return int(60 * minute + second)

def sectomin(seconds):
    return int(seconds/60), int(seconds %60)
 
def floattodigital(minute):
    return sectomin(mintosec(minute))

def eventsec(e):
    return mintosec(e['minute'],e['second'])



class Timer:
    def __init__(self,msg="code"):
        self.msg = msg
        
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.interval = self.end - self.start
        print "%s : %.2fs" %(self.msg, self.interval)
        
if __name__ == '__main__':
    with Timer():
        sum(range(1,100000000))