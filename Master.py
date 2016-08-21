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
import RandomGenerator

# the main traffic coordinator
class Master:
    m = Map.Map()       # Map...
    random = RandomGenerator.RandomGenerator()
    cars = []           # List of cars on the map
    navi = RoutePlanner.RoutePlanner()
    # Position from which you can't progress to the next one
    blocked = []
    # redLights is a dictionary indicating which incoming streets are blocked
    trafficLights = {}

    def __init__(self):
        self.initialize()
    
    """ """ """ """ """ """
    """ """ """ """ """ """
    """  LOADING STUFF  """
    """ """ """ """ """ """
    """ """ """ """ """ """

    def initialize(self):
        print "Initializing the Master with a map from text files and one car"

        # Load the intersections first
        self.loadIntersections()
        # Load the streets
        self.loadStreets()
        # Initialize the navi
        self.navi.setMap(self.m)
        # Initialize incomingStreets in the map
        self.m.calcIncomingStreets()
        # Initialize all traffic lights to red :D
        self.initializeTrafficLights()
        self.updateBlocked()

        # Initialize so far only one car
        # start, destination, name
        car1 = Car.Car(0, 6, "Porsche   ")
        car2 = Car.Car(1, 5, "Volkswagen")
        self.cars.append(car1)
        self.cars.append(car2)
        # Calculate all the routes of the cars
        self.calculateRoutes()
        
        # Initialize blocked positions
        # A) by cars
        for c in self.cars:
            self.blocked.append(c.curPos)


        print '... done!'

    def initializeTrafficLights(self):
        for i in self.m.intersections:
            state = {}
            state['Green'] = []
            state['Red'] = self.m.incoming[i]
            self.trafficLights[i] = state

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
        for c in self.cars:
            print c.name + " on " + str(c.curPos) + " with route " + str(c.fineRoute)

    def printState(self):
        print '\n The current state of the program is'
        print '\n### intersections: '
        print self.m.intersections
        print '### streets: '
        print self.m.streets
        print '### incoming: '
        print self.m.incoming
        print '### characteristics: '
        print self.m.character
        print '### traffic lights: '
        print self.trafficLights
        print '### cars: '
        self.printCars()
        print '\n'






    """ """ """ """ """ """
    """ """ """ """ """ """
    """ ROUTE CALCULATION """
    """ """ """ """ """ """
    """ """ """ """ """ """

    def calculateRoutes(self):
        # Give every car a coarse route
        for c in self.cars:
            c.coarseRoute = self.navi.calcCoarseRoute(c.start, c.destination)
        #for c in self.cars:
        #    print c.name + '   coarse   ' + str(c.coarseRoute)
        # Give every car a fine route based on its coarse route
        # move this function to Routeplanner later
        for c in self.cars:
            c.fineRoute = self.navi.calcFineRoute(c.coarseRoute)
        #for c in self.cars:
        #    print c.name + '   fine   ' + str(c.fineRoute)
        
        # Update general car information
        # That is, find initial direction of travel from coarse route,
        # update nextIntersection and calculate therewith the street
        # and curPos the car should be on.
        for c in self.cars:
            c.nextIntersection = c.coarseRoute[1]
            street = self.m.findStreet(c.start, c.nextIntersection)
            c.curPos = (street, 0)







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
        

    """ """ """ """ """ """
    """ """ """ """ """ """
    """ TRAFFIC LIGHTS  """
    """ """ """ """ """ """
    """ """ """ """ """ """
    def updateBlocked(self):
        for i in self.m.intersections:
            # We need to remove all blocks from this intersections that are in Green
            # and add all the ones that are in Red
            for g in self.trafficLights[i]['Green']:
                street = self.m.lastPos(g)
                if street in self.blocked:
                    # Remove (g, last elem of g)
                    self.blocked.remove(street)
            for r in self.trafficLights[i]['Red']:
                street = self.m.lastPos(r)
                if street  not in self.blocked:
                    # Add (r, last elem of r)
                    self.blocked.append(street)
            

    def turnGreen(self, inter, street):
        self.trafficLights[inter]['Red'].remove(street)
        self.trafficLights[inter]['Green'].append(street)
        self.updateBlocked()

    def turnRed(self, inter, street):
        self.trafficLights[inter]['Green'].remove(street)
        self.trafficLights[inter]['Red'].append(street)
        self.updateBlocked()
