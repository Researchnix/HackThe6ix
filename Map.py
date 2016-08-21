#
#  Map.py
#  HackThe6ix
#
#  Created by Jeffrey, Maliha, Justin  and Lennart on 2016-08-06.
#  Copyright 2016 Researchnix. All rights reserved.
#

import Street

class Map:
    intersections = []
    streets = []


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
    # The resulst should by assumption exist and be unique!!
    def findStreet(self, start, finish):
        t = [start, finish]
        for s in self.streets:
            if s[:2] == t or s[:2] == t[::-1]:
                return self.streets.index(s)
