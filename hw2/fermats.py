# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 21:04:25 2014

@author: austin
"""

def testFermat(a,b,c,n):
    if (n>2):
        if(a**n + b**n != c**n):
            print "Nope, that doesn't work"
        else:
            print "Holy Smokes, Fermat was wrong!"
    else:
        print "Did you read the theorem? n must be greater than 2!"
        
a = int(raw_input("Input a: "))
b = int(raw_input("Input b: "))
c = int(raw_input("Input c: "))
n = int(raw_input("Input n: "))

testFermat(a,b,c,n)