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

    def __init__(self):
        self.initialize()

    def loadData(self):
        print "loading data"
        # Load the intersections first
        f = open('Intersections.txt', 'r')
        for line in f:
            line = line.split()
            self.m.addIntersection(line[-1])


    def timeStep(self):
        pass
    
    def initialize(self):
        print "Initializing the data"
        '''
        # Intersections
        self.m.addIntersection('a')
        self.m.addIntersection('b')
        self.m.addIntersection('c')
        '''

        # Streets
        self.m.addStreet(0,1,10)
        self.m.addStreet(1,2,10)

        # Car1
        car1 = Car.Car(0,0, "Porsche")
        self.cars.append(car1)

        # Car2
        #car2 = Car.Car(1,0, "Volkswagen")
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
            print c.name + " on " + str(c.street) + " at " + str(c.pos)
