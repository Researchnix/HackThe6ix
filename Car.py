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
    street = 0
    pos = 0
    nextIntersection = 0
    name = ""
    # Index of desired intersection to travel to
    destination = 0
    # The route is a list of intersections which the 
    # car is going to take
    route = []

    def __init__(self, street, posOnStreet, name):
        self.street = street
        self.pos = posOnStreet
        self.name = name

    def setDest(self, dest):
        self.destination = dest

