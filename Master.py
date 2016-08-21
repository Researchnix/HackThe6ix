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
    # Give each intersection the state of either 
    # 1X always green
    # 2X always green, maybe later randomly red due to pedestrians crossing 
    # 3X TODO
    # 4X horizontal, vertical, hleft, vleft
    # or RED, meaning everything is red
    interState = {}

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
        self.initializeInterState()

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

    def initializeInterState(self):
        for i in self.m.intersections:
            self.interState[i] = "RED"
        print "POS 1"
        print self.interState

    def initializeTrafficLights(self):
        for i in self.m.intersections:
            state = {}
            state['Green'] = []
            state['Red'] = self.m.incoming[i]
            self.trafficLights[i] = state

    def loadIntersections(self):
        f = open('inter.txt', 'r')
        for line in f:
            line = line.split()
            self.m.addIntersection(int(line[0]))
        f.close()

    def loadStreets(self):
        # First add streets in right orientation
        # Format of ori.txt is
        # to from1 from2 from3 ...
        f = open('ori.txt', 'r')
        for line in f:
            line = line.split()
            to = int(line.pop(0))
            for remaining in line:
                self.m.addStreet(int(remaining), to, 0)
        f.close()
        # Now load the lengths from dist.txt
        f = open('dist.txt', 'r')
        for line in f:
            line = line.split()
            self.m.setDist(int(line[0]), int(line[1]), int(line[2]))
        f.close()

    def printCars(self):
        for c in self.cars:
            print c.name + " on " + str(c.curPos) + " with route " + str(c.fineRoute)

    def printState(self):
        print '\nThe current state of the program is'
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
        print '### Intersection states: '
        print self.interState
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
            

    # To change the sign of a traffic light use this format
    # (inter = intersection_index, street = street_index of incoming street)
    def turnGreen(self, inter, street):
        self.trafficLights[inter]['Red'].remove(street)
        self.trafficLights[inter]['Green'].append(street)
        self.updateBlocked()

    def turnRed(self, inter, street):
        self.trafficLights[inter]['Green'].remove(street)
        self.trafficLights[inter]['Red'].append(street)
        self.updateBlocked()

    def updateInterState(self):
        for i in self.interState.keys():
            if self.interState[i] == 'RED':
                for s in self.m.incoming[i]:
                    self.turnRed(i, s)
            if self.interState[i] == 'GREEN':
                for s in self.m.incoming[i]:
                    self.turnGreen(i, s)
            if self.interState[i] == 'horizontal': # len(incoming[i]) = 4 required
                nghs = self.m.incoming[i]
                self.turnGreen(i, nghs[0])
                self.turnRed(i, nghs[1])
                self.turnGreen(i, nghs[2])
                self.turnRed(i, nghs[3])
            if self.interState[i] == 'vertical':     # len(incoming[i]) = 4 required
                nghs = self.m.incoming[i]
                self.turnGreen(i, nghs[1])
                self.turnRed(i, nghs[0])
                self.turnGreen(i, nghs[3])
                self.turnRed(i, nghs[2])
            if self.interState[i] == 'hleft':        # len(incoming[i]) = 4 required
                pass
            if self.interState[i] == 'vleft':         # len(incoming[i]) = 4 required
                pass
