# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 20:37:30 2014

@author: austin
"""

def drawGrid(r,c):
    wallLength = 0
    
    topLine = "+ - - - - -"
    boxWall = "|          "
    
    for rowCounter in range(0, r):
        for collumnCounter in range(0, c):
            print topLine,
        print "+"
        while(wallLength < 4):
            for collumnCounter in range(0, c):
                print boxWall,
            print "|"
            wallLength = wallLength + 1
        wallLength = 0
        
    for collumnCounter in range(0, c):
        print topLine,
    print "+"
            
rows = int(raw_input("input the numbers of rows: "))
collumns = int(raw_input("input the numbers of collumns: "))

drawGrid(rows,collumns)

                