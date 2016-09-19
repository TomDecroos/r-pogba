'''
Created on Sep 19, 2016

@author: tomd
'''
import sys

def logmap(f,xs):
    print "mapping %s to %d objects" %(f.__name__,len(xs))
    n = len(xs)
    step = 0.01*n
    threshold = 0
    perc = 0
    sys.stdout.write("\r%d%%" % 0)
    sys.stdout.flush()
    results = list()
    err_cnt = 0
    for i,x in zip(range(1,n+1),xs):
        try:
            results.append(f(x))
        except KeyboardInterrupt as e:
            raise e
        except:
            err_cnt += 1
        while i >= threshold:
            threshold += step
            perc += 1
            sys.stdout.write("\r%d%% errors: %d" % (perc,err_cnt))
            sys.stdout.flush()
    print ""
    return results
    