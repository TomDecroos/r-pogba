'''
Created on Sep 19, 2016

@author: tomd
'''
import sys


def logmap(f, xs):
    n = len(xs)
    print "mapping %s to %d objects" % (f.__name__, n)
    sys.stdout.write("\r%d/%d" % (0, len(xs)))
    sys.stdout.flush()
    results = list()
    err_cnt = 0
    for i, x in enumerate(xs):
        try:
            results.append(f(x))
        except KeyboardInterrupt as e:
            raise e
        except:
            err_cnt += 1
        sys.stdout.write("\r%d/%d errors: %d" % (i + 1, n, err_cnt))
        sys.stdout.flush()
    print ""
    return results


def errmap(f, xs, threshold=1):
    results = list()
    err_cnt = 0
    for x in xs:
        try:
            results.append(f(x))
        except KeyboardInterrupt as e:
            raise e
        except:
            err_cnt += 1
    err_perc = float(err_cnt) / len(xs)
    if err_perc > threshold:
        raise Exception("Too many mapping errors: %2.1f%%"
                        % (err_perc * 100))
    return results


def logfilter(f, xs):
    n = len(xs)
    print "filtering %d objects using %s" % (n, f.__name__)
    sys.stdout.write("\r%d/%d" % (0, n))
    sys.stdout.flush()
    results = list()
    err_cnt = 0
    accept_cnt = 0
    reject_cnt = 0
    for i, x in enumerate(xs):
        try:
            if f(x):
                results.append(x)
                accept_cnt += 1
            else:
                reject_cnt += 1
        except KeyboardInterrupt as e:
            raise e
        except:
            err_cnt += 1
        sys.stdout.write("\r%d/%d errors: %d accept: %d reject: %d"
                         % (i + 1, n, err_cnt, accept_cnt, reject_cnt))
        sys.stdout.flush()
    print ""
    return results


def errfilter(f, xs, threshold=1):
    results = list()
    err_cnt = 0
    for x in xs:
        try:
            if f(x):
                results.append(x)
        except KeyboardInterrupt as e:
            raise e
        except:
            err_cnt += 1
    err_perc = float(err_cnt) / len(xs)
    if err_perc > threshold:
        raise Exception("Too many filtering errors: %2.1f%%"
                        % (err_perc * 100))
    return results
