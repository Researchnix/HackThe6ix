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
	for node in m.streets:
		if node[0] not in graph:
			graph[node[0]] = {node[1]: node[2]}
		if node[1] not in graph:
			graph[node[1]] = {node[0]: node[2]}
		else:
			graph[node[0]][node[1]] = node[2]
			graph[node[1]][node[0]] = node[2]
    
    def setMap(self, m):
        self.m = m
        
    # This function returns the list of intersections
    # that leads from start to finish on the map m
    def calcCoarseRoute(self, start, finish):
        distances = {}
		predecessors = {}
		to_assess = graph.keys()
		for node in graph:
			distances[node] = float('inf')
			predecessors[node] = None
		sp_set = []
		distances[start] = 0
		while len(sp_set) < len(to_assess):
			still_in = {node: distances[node] for node in [node for node in to_assess if node not in sp_set]}
			closest = min(still_in, key = distances.get)
			sp_set.append(closest)
			for node in graph[closest]:
				if distances[node] > distances[closest] + graph[closest][node]:
					distances[node] = distances[closest] + graph[closest][node]
					predecessors[node] = closest
		path = [finish]
		while start not in path:
			path.append(predecessors[path[-1]])
		result = path[::-1]
		return result

    # This function calculates the fine route dependent
    # on the previously computed coarse route
    def calcFineRoute(self, coarse):
        result = []
        return result
