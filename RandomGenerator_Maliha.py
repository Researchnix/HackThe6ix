#
#  RandomGenerator.py
#  HackThe6ix
#
#  Created by Jeffrey, Maliha, Justin  and Lennart on 2016-08-06.
#  Copyright 2016 Researchnix. All rights reserved.
#

import random

class RandomGenerator:
    intersections = []
    streets = []

    #generate a list of intersections 
    def generateIntersections(self, numIntersections):
        return range(numIntersections)

    #generate a list of streets
    #numStreets must be >= numIntersections in order for all intersections to be connected 
    def generateStreets(self, numIntersections, numStreets, maxLength):
        visitedIntersections = []
        streetCounter = 0

        while len(visitedIntersections) != numIntersections:
            start = random.randint(0, numIntersections-1)
            if start not in visitedIntersections:
                visitedIntersections.append(start)
            end = random.randint(0, numIntersections-1)
            if end == start:
                while end == start:
                    end = random.randint(0, numIntersections-1)
            if end not in visitedIntersections:
                visitedIntersections.append(end)

            self.streets.append([start, end, random.randint(1, maxLength)])
            streetCounter += 1

        if streetCounter == numStreets:
            return self.streets
        else:
            while streetCounter != numStreets:
                start = random.randint(0, numIntersections-1)
                end = random.randint(0, numIntersections-1)          
                if end == start:
                    while end == start:
                        end = random.randint(0, numIntersections-1)

                self.streets.append([start, end, random.randint(1, maxLength)])
                streetCounter += 1
            return self.streets
