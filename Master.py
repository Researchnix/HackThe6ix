#
#  Master.py
#  HackThe6ix
#
#  Created by Jeffrey, Maliha, Justin  and Lennart on 2016-08-06.
#  Copyright 2016 Researchnix. All rights reserved.
#

import Map
import Car
import RoutePlanner

# the main traffic coordinator
class Master:
    m = Map.Map()       # Map...
    cars = []           # List of cars on the map
    navi = RoutePlanner.RoutePlanner()
    # Position from which you can't progress to the next one
    blocked = []

    def __init__(self):
        self.initialize()

    def loadIntersections(self):
        f = open('Intersections.txt', 'r')
        for line in f:
            line = line.split()
            self.m.addIntersection(line[-1])
        f.close()

    def loadStreets(self):
        f = open('Streets.txt', 'r')
        for line in f:
            line = line.split()
            self.m.addStreet(int(line[1]), int(line[2]), int(line[3]))
        f.close()

    def canProgress(self, car):
        return True

    def nextPosition(self, car):
        result = []
        return result

    def timeStep(self):
        for c in self.cars:
            if self.canProgress(c):
                pass
    
    def initialize(self):
        print "Initializing the data"

        # Load the intersections first
        self.loadIntersections()

        # Load the streets
        self.loadStreets()

        # Car1
        car1 = Car.Car(0,0, "Porsche")
        car1.FineRoute
        self.cars.append(car1)


        # Car2
        #car2 = Car.Car(1,4, "Volkswagen")
        #self.cars.append(car2)

        # RoutePlanner
        self.navi.setMap(self.m)

        
    def printState(self):
        print '\n### intersections: '
        print self.m.intersections
        print '### streets: '
        print self.m.streets
        print '### cars: '
        self.printCars()
        print '\n'

    def printCars(self):
        for c in self.cars:
            #print c.name + " on " + str(c.street) + " at " + str(c.pos)
            print c.name + " on " + str(c.curPos)
