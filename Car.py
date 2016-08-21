#
#  Car.py
#  HackThe6ix
#
#  Created by Jeffrey, Maliha, Justin  and Lennart on 2016-08-06.
#  Copyright 2016 Researchnix. All rights reserved.
#

class Car:
    # The current position of the car is a pair with the street index and the position
    # on the street
    #street = 0
    #pos = 0
    curPos = (0,0)
    nextIntersection = 0
    name = ""
    # Index of starting intersection and desired intersection to travel to
    start = 0
    destination = 0
    # The route is a list of intersections which the 
    # car is going to take
    coarseRoute = []
    fineRoute = []
    
    destinationReached = False

    def __init__(self, street, posOnStreet, name):
        #self.street = street
        #self.pos = posOnStreet
        self.curPos = (street, posOnStreet)
        self.name = name

    def setDest(self, dest):
        self.destination = dest

    def nextPos(self):
        return self.fineRoute[0]

