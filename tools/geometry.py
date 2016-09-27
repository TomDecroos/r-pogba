'''
Created on Sep 27, 2016

@author: tomd
'''
from math import sqrt, atan2
class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def vector(self,p):
        return Vector(p.x-self.x,p.y-self.y)

class Vector(Point):
    def abs(self):
        return sqrt(self.x*self.x + self.y*self.y)
    def angle(self):
        return atan2(self.y,self.x)
    def dot(self,v):
        return self.x*v.x +self.y*v.y