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
    
    def initialize(self):
        print "Initializing the data"

        # Load the intersections first
        self.loadIntersections()

        # Load the streets
        self.loadStreets()

        # Car1
        car1 = Car.Car(0,0, "Porsche")
        car1.start = 0
        car1.destination = 6




        self.blocked.append((0,0))
        for i in range(1,5):
            car1.fineRoute.append((0,i))
        for i in range(1,5):
            car1.fineRoute.append((1,i))
        self.cars.append(car1)


        # Car2
        #car2 = Car.Car(1,4, "Volkswagen")
        #self.cars.append(car2)

        # RoutePlanner
        self.navi.setMap(self.m)

    """ """ """ """ """ """
    """ """ """ """ """ """
    """  LOADING STUFF  """
    """ """ """ """ """ """
    """ """ """ """ """ """

    def loadIntersections(self):
        f = open('Intersections.txt', 'r')
        for line in f:
            line = line.split()
            self.m.addIntersection(int(line[-1]))
        f.close()

    def loadStreets(self):
        f = open('Streets.txt', 'r')
        for line in f:
            line = line.split()
            self.m.addStreet(int(line[1]), int(line[2]), int(line[3]))
            self.m.addStreet(int(line[2]), int(line[1]), int(line[3]))
        f.close()

    def printCars(self):
        print '### cars: '
        self.printCars()

    def printState(self):
        print '\n### intersections: '
        print self.m.intersections
        print '### streets: '
        print self.m.streets
        self.printCars()
        print '\n'






    """ """ """ """ """ """
    """ """ """ """ """ """
    """ ROUTE CALCULATION """
    """ """ """ """ """ """
    """ """ """ """ """ """

    def calculateRoutes(self):
        # Give every car a coarse route
        #for c in self.cars:
        #    c.coarseRoute = self.navi.calcCoarseRoute(c.start, c.destination)

        self.cars[0].coarseRoute = [0,2]

        for c in self.cars:
            print c.name + '   coarse   ' + str(c.coarseRoute)

        # Give every car a fine route based on its coarse route
        # move this function to Routeplanner later
        for c in self.cars:
            c.fineRoute = self.calcFineRoute(c.coarseRoute)

        for c in self.cars:
            print c.name + '   fine   ' + str(c.fineRoute)


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




        









    """ """ """ """ """ """
    """ """ """ """ """ """
    """ STEPPING STUFF """
    """ """ """ """ """ """
    """ """ """ """ """ """

    def canProgress(self, car):
        return not (car.nextPos() in self.blocked)

    def timeStep(self):
        for c in self.cars:
            if not c.destinationReached:
                if self.canProgress(c):
                    self.blocked.remove(c.curPos)   # clear the spot that the car was on
                    c.curPos = c.fineRoute.pop(0)             # move car forward by one unit
                    self.blocked.append(c.curPos)   # call dips on the current position
                    if len(c.fineRoute) == 0:
                        c.destinationReached = True
        

    def printCars(self):
        for c in self.cars:
            #print c.name + " on " + str(c.street) + " at " + str(c.pos)
            print c.name + " on " + str(c.curPos) + " with route " + str(c.fineRoute)
