#
#  RandomGenerator.py
#  HackThe6ix
#
#  Created by Jeffrey, Maliha and Lennart on 2016-08-20.
#  Copyright 2016 Researchnix. All rights reserved.
#

from math import *
from random import *
import os

class RandomGenerator:
    x_max = 500
    y_max = 500
    origin = [0, 0]
    radiusStep = 10
    approxDist = 10
    sigma = 3
    result = []
    filename = "inter_gen.txt"



    def generateInter(self, n):
        self.result.append([0] + self.origin)
        
        # Go outwards along circles of radius step * 
        # radiusStep while ... and add intersections
        totalCounter = 1
        radiusCounter = 1
        while len(self.result) < n:
            curRad = radiusCounter * self.radiusStep

            # Put the first point on this circle
            zeroAngle = radians(randint(0,360))
            nextEntry = [totalCounter] + self.xyFromPolar(curRad, zeroAngle)
            self.result.append(nextEntry)
            totalCounter += 1



            # Add intersections on this circle while there is "space left"
            spaceLeft = True
            maxAngle = zeroAngle
            while spaceLeft == True:
                plusMinus = uniform(- self.sigma, self.sigma)
                length = self.approxDist + plusMinus
                angle = self.angDist(curRad, length)        # in rad
                maxAngle = (maxAngle + angle) % 2 * pi
                xy = self.xyFromPolar(curRad, maxAngle)
                self.result.append([totalCounter] + xy)

                
                spaceLeft = self.isSpaceLeft(curRad, zeroAngle, maxAngle)
                totalCounter += 1
            radiusCounter += 1

    def writeToFile(self):
        self.deleteFile()
        f = open(self.filename, 'a')
        for elem in self.result:
            newelem = map(int, map(abs, elem))
            newnewelem = map(str, newelem)
            line = " ".join(newnewelem) + "\n"
            f.write(line)
        f.close()




    def deleteFile(self):
        try:
            os.remove(self.filename)
        except OSError:
            pass



    # phi in radian !!!
    def xyFromPolar(self, r, phi):
        return [r * cos(phi), r *  sin(phi)]

    # Distance of two points on a circle dep on radian
    def radDist(self, r, phi):
        return phi * r


    # Distance of two points on a circle in polar angle
    def angDist(self, r, l):
        return l / r

    # Determine whether another point fits on the circle
    def isSpaceLeft(self, r, phi0, phi1):
        angleDiff = abs(phi1 - phi0) % 360
        return self.radDist(r, angleDiff) > (self.approxDist - self.sigma)
