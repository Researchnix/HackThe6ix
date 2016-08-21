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
    graph = {}
    def setMap(self, m):
        self.m = m
        for node in m.streets:
            if node[0] not in self.graph:
               self.graph[node[0]] = {node[1]: node[2]}
            else:
                self.graph[node[0]][node[1]] = node[2]
            if node[1] not in self.graph:
                self.graph[node[1]] = {node[0]: node[2]}
            else:
                self.graph[node[1]][node[0]] = node[2]
    
    # This function returns the list of intersections
    # that leads from start to finish on the map m
    def calcCoarseRoute(self, start, finish):
        distances = {}
        predecessors = {}
        to_assess = self.graph.keys()
        for node in self.graph:
            distances[node] = float('inf')
            predecessors[node] = None
        sp_set = []
        distances[start] = 0
        while len(sp_set) < len(to_assess):
            still_in = {node: distances[node] for node in [node for node in to_assess if node not in sp_set]}
            closest = min(still_in, key=distances.get)
            sp_set.append(closest)
            for node in self.graph[closest]:
                if distances[node] > distances[closest] + self.graph[closest][node]:
                    distances[node] = distances[closest] + self.graph[closest][node]
                    predecessors[node] = closest
        path = [finish]
        while start not in path:
            path.append(predecessors[path[-1]])
        result = path[::-1]
        return result


    # This function calculates the fine route dependent
    # on the previously computed coarse route
    def calcFineRoute(self, coarse):
        fine = []
        # Iterate over every way point except the last one
        # and add the fine points of every street connecting
        # the way point with its successor by the fine route
        for w in range(len(coarse) - 1) :
            street = self.m.findStreet(coarse[w], coarse[w+1])
            length = self.m.streets[street][-1]
            # doe the fine route
            for i in range(length):
                fine.append((street, i + 1))
        return fine




        




