#
#  Map.py
#  HackThe6ix
#
#  Created by Jeffrey, Maliha  and Lennart on 2016-08-06.
#  Copyright 2016 Researchnix. All rights reserved.
#

import Street

class Map:
    intersections = []
    streets = []
    incoming = {}      # dic from intersections to incoming streets to this intersection
    character = {}     # number of incoming streets for each crossing
    fourFoldInter = [] # all intersections with character 4


    # the index could also be a label
    def addIntersection(self, index):
        self.intersections.append(index) 

    # the index could also be a label
    # two different ways of handling streets
    # with and without extra objects
    def addStreet(self, From, To, length):
        s = [From, To, length]
        self.streets.append(s)
        '''
        s = Street.Street(From, To, length)
        self.streets.append(s)
        '''


    # Find the right street connecting two intersections
    # The resulst should by assumption exist and be unique
    # up to direction
    def findStreet(self, start, finish):
        t = [start, finish]
        for s in self.streets:
            if s[:2] == t:
                return self.streets.index(s)
        print "NO SUCH STREET EXIST!!!!!"

    def calcIncomingStreets(self):
        for i in self.intersections:
            result = []
            for s in self.streets:
                if s[1] == i:
                    result.append(self.streets.index(s))
            self.incoming[i] = result
            self.character[i] = len(result)
        self.fourFoldInter = [i for i in self.intersections if self.character[i] == 4]

    def lastPos(self, street):
        length = self.streets[street][2]
        return (street,length)

    def setDist(self, node1, node2, l):
        s1 = self.findStreet(node1, node2)
        s2 = self.findStreet(node2, node1)
        self.streets[s1][2] = l
        self.streets[s2][2] = l
        
