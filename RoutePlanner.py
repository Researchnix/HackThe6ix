#
#  RoutePlanner.py
#  HackThe6ix
#
#  Created by Jeffrey, Maliha, Justin  and Lennart on 2016-08-06.
#  Copyright 2016 Researchnix. All rights reserved.
#

import Map

class RoutePlanner:
    """ Class that find the route that each car should take """
    m = Map.Map()
    
    def setMap(self, m):
        self.m = m
        
    # This function returns the list of intersections
    # that leads from start to finish on the map m
    def findRoute(self, start, finish):
        result = []
        return result
