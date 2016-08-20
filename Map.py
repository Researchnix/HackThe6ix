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
