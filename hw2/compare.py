# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 21:12:36 2014

@author: austin
"""

def compareInput(x,y):
    if x > y:
        return 1
    elif x < y:
        return -1
    else:
        return 0
        
print compareInput (int(raw_input("Input your first number to compare: ")), int(raw_input("Input your second number to compare: ")))

