#
#  Master.py
#  HackThe6ix
#
#  Created by Jeffrey, Maliha and Lennart on 2016-08-20.
#  Copyright 2016 Researchnix. All rights reserved.
#

import sys
from random import *

import Map
import Car
import RoutePlanner

# the main traffic coordinator
class Master:
    ''' constants'''
    maxRunTime = 10000
    verbose = True

    ''' time stepping '''
    m = Map.Map()       # Map...
    cars = []           # List of cars on the map
    navi = RoutePlanner.RoutePlanner()      # Navigation device
    # Position from which you can't progress to the next one
    blocked = [] 
    # trafficLights is a dictionary containing a dictionary with keys Red and Green returning a list of Red and Green files

    ''' traffic lights'''
    trafficLights = {}
    # Give each intersection the state of either 
    # 1X always green
    # 2X always green, maybe later randomly red due to pedestrians crossing 
    # 3X TODO
    # 4X horizontal, vertical, hleft, vleft
    # or RED, meaning everything is red
    # all GREEN is an unusual state...
    interState = {}

    # Evaluation helpers
    evaluation = {}
    numberOfCars = 2
    travelLength = {}




### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### INITIALIZATION ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #




    def __init__(self):
        self.initialize()
    

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
        #car1 = Car.Car(5, 30, "Porsche   ")
        #car2 = Car.Car(19, 18, "Volkswagen")
        #car3 = Car.Car(27, 11, "A")
        #car4 = Car.Car(11, 5, "B")
        #car5 = Car.Car(30, 12, "C")
        #car6 = Car.Car(8, 26, "D")
        #car7 = Car.Car(11, 27, "E")
        #self.cars.append(car1)
        #self.cars.append(car2)
        #self.cars.append(car3)
        #self.cars.append(car4)
        #self.cars.append(car5)
        #self.cars.append(car6)
        #self.cars.append(car7)
        self.initializeRandomCars(20)
        # Calculate all the routes of the cars
        self.calculateRoutes()
        # Prepare the evaluation of the efficiency
        self.numberOfCars = len(self.cars)
        for c in self.cars:
            self.travelLength[c.name] = len(c.fineRoute)
        # Initialize blocked positions
        # A) by cars
        for c in self.cars:
            self.blocked.append(c.curPos)
        print '... done!'

    def initializeRandomCars(self, n):
        everywhere = self.m.intersections.keys()
        available = self.m.intersections.keys()
        for x in range(n):
            start  = available[randint(0,len(available)-1)]
            finish  = everywhere[randint(0,len(everywhere)-1)]
            name = "car" + str(x)
            if not start == finish:
                self.cars.append( Car.Car(start, finish, name) )
            available.remove(start)

        

    def initializeInterState(self):
        # make everything TL that has 2 roards or less GREEN
        for i in self.m.intersections:
            if self.m.character[i] <= 2:
                self.interState[i] = "GREEN"
            else:
                self.interState[i] = "RED"
        self.updateInterState()

    def initializeTrafficLights(self):
        for i in self.m.intersections:
            state = {}
            state['Green'] = []
            state['Red'] = self.m.incoming[i]
            self.trafficLights[i] = state

    def loadIntersections(self):
        f = open('inter_gen.txt', 'r')
        for line in f:
            line = line.split()
            self.m.addIntersection(int(line[0]), 250 + float(line[1]), 250 + float(line[2]))
        f.close()



### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### MAKING DATA AVAILABLE ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #


    #def getInitializionData(self):





### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### LOADING DATA ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #

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
        #f = open('dist.txt', 'r')
        #for line in f:
        #    line = line.split()
            #self.m.setDist(int(line[0]), int(line[1]), int(line[2]))
        #f.close()
        ''' Trick: every dist = 10 '''
        for x in self.m.streets:
            x[-1] = 10





### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### OUTPUT METHODS ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #

    def printCars(self):
        for c in self.cars:
            print c.name + " on " + str(c.curPos) + " with route " + str(c.fineRoute[:5])

    def printState(self):
        print '\nThe current state of the program is'
        print '\n### intersections: '
        print self.m.intersections
        print '### streets: '
        print self.m.streets
        print '### incoming: '
        print self.m.incoming
        print '### character: '
        print self.m.character
        print '### traffic lights: '
        print self.trafficLights
        print '### Intersection states: '
        print self.interState
        print '### cars: '
        self.printCars()
        print '\n'






### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ROUTE CALCULATION ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #

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







### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### STEPPING FUNCTIONS ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #

    # Do as many as maxRunTime steps to try to get every car to its destination
    def run(self, total):
        #print "\n\n"
        #print "######################################################################"
        #print "TIME STEPPING STARTS HERE"
        #print "######################################################################"
        #print "\n\n"
        #########################
        # Insert the model here #
        #########################
        #self.useModel1(8, total)
        self.useModel2(11, 11, total)
        if len(self.cars) == 0:
            sys.exit("All cars reached their destination")
        self.timeStep()
        if self.verbose:
            self.printCars()
            print self.interState
        # Check if any car reached its destination
        for c in self.cars[::-1]:
            if c.destinationReached:
                self.evaluation[c.name] = total
                self.blocked.remove(c.curPos)
                self.cars.remove(c)
        #print "\n\n"
        #print "######################################################################"
        #print "All cars are done ... or the time is up "
        #print "Evaluation of the time it took each car " + str(self.evaluation)
        #print "Total time a car was using fuel = " + str(sum(self.evaluation.values()))
        #print "Relative inefficiency =  " + str(sum(self.evaluation.values()) / self.numberOfCars)
        #print "\n\n"
        #diff = [self.evaluation.values()[c] -self.travelLength.values()[c] for c in range(len(self.evaluation))]
        #print "Time a car was standing still =" + str(diff)
        #print "Overall time a car was waiting for a traffic light = " + str(sum(diff))

    def canProgress(self, car):
        return not (car.nextPos() in self.blocked)


    # One time step in which every car that can potentially progress progresses.
    def timeStep(self):
        for c in self.cars:
            if not c.destinationReached:
                if self.canProgress(c):
                    # We have a ghosting problem, due to time, ignore the error...
                    # This error appears exactly when the traffic lights free an
                    # intersection that is still occupied by a car. Hence when the car 
                    # moves on, it can't free its last position that's already free
                    if c.curPos in self.blocked:
                        # clear the spot that the car was on
                        self.blocked.remove(c.curPos)
                    c.oldPos = c.curPos
                    c.curPos = c.fineRoute.pop(0)             # move car forward by one unit
                    self.blocked.append(c.curPos)   # call dips on the current position
                    c.needsUpdate = True
                    if len(c.fineRoute) == 0:
                        c.destinationReached = True
        





### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### TRAFFIC LIGHT FUNCTIONs### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #

    def updateBlocked(self):
        for i in self.m.intersections.keys():
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
                self.trafficLights[i]['Green'] = []
                self.trafficLights[i]['Red'] = self.m.incoming[i]
            if self.interState[i] == 'GREEN':
                self.trafficLights[i]['Red'] = []
                self.trafficLights[i]['Green'] = self.m.incoming[i]
            if self.interState[i] == 'horizontal': # len(incoming[i]) = 4 required
                reds = []
                greens = []
                nghs = self.m.incoming[i]
                reds.append(nghs[0])
                reds.append(nghs[2])
                greens.append(nghs[1])
                greens.append(nghs[3])
                self.trafficLights[i]['Red'] = reds
                self.trafficLights[i]['Green'] = greens
            if self.interState[i] == 'vertical':     # len(incoming[i]) = 4 required
                reds = []
                greens = []
                nghs = self.m.incoming[i]
                reds.append(nghs[1])
                reds.append(nghs[3])
                greens.append(nghs[0])
                greens.append(nghs[2])
                self.trafficLights[i]['Red'] = reds
                self.trafficLights[i]['Green'] = greens
            if self.interState[i] == 'hleft':        # len(incoming[i]) = 4 required
                pass
            if self.interState[i] == 'vleft':         # len(incoming[i]) = 4 required
                pass
        self.updateBlocked()

    def changeInterState(self, inter, mode):
        self.interState[inter] = mode
        self.updateInterState()

    #Flips state from horizontal to vertical and vice versa
    def flipInterState(self, inter):
        if self.interState[inter] == 'horizontal':
            self.interState[inter] = 'vertical'
        else:       # default for RED or GREEN
            self.interState[inter] = 'horizontal'
        self.updateInterState()
        


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### TRAFFIC MODELS ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##### #

    # Model 1 sets every intersection for some interval par to horizontal and then reversed
    def useModel1(self, par, curTime):
        # One line solution, haha !!
        signal = [int(float(i)/par) % 2 for i in range(self.maxRunTime)]
        if signal[curTime] == 0:
            for i in self.m.fourFoldInter:
                self.changeInterState(i, 'horizontal')
        else:
            for i in self.m.fourFoldInter:
                self.changeInterState(i, 'vertical')

    # Random Model flips every par1 interval par2 of the fourFoldInter
    def useModel2(self, par1, par2, curTime):
        signal = [0 for y in range(self.maxRunTime)]
        for i in range(self.maxRunTime):
            if i%par1 == 0:
                signal[i] = 1

        if signal[curTime] == 1:
            for x in range(par2):
                i = randint(0,len(self.m.fourFoldInter)-1)
                self.flipInterState(self.m.fourFoldInter[i])
