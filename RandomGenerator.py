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
    filename1 = "inter_gen.txt"
    filename2 = "ori_gen.txt"



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
        # Write the intersections to the file
        self.deleteFile(self.filename1)
        f = open(self.filename1, 'a')
        for elem in self.result:
            newelem = map(int, map(abs, elem))
            newnewelem = map(str, newelem)
            line = " ".join(newnewelem) + "\n"
            f.write(line)
        f.close()

        # Write the orientation to ori_gen.txt
        self.deleteFile(self.filename2)
        f = open(self.filename2, 'a')
        nodes = [e[0] for e in self.result]
        # Mix them up
        mixed = nodes
        orientations = [mixed[:]]
        for a in range(3):
            for i in range(len(mixed)):
                j = i
                while j == i:
                    j = randint(0,len(mixed) - 1)
                mixed = self.transposition(mixed, i, j)
            print mixed
            orientations.append(mixed[:])
        #for elem in self.trans(orientations):
            
        f.close()




    def transposition(self, lisT, i, j):
        wait = lisT[i]
        lisT[i] = lisT[j]
        lisT[j] = wait
        return lisT


    def trans(self, l):
        rl = len(l[0]) # column length
        result = []
        for i in range(rl):
            newRow = []
            for row in l:
                newRow.append(row[i])
            result.append(newRow)
        return result





    def deleteFile(self, filename):
        try:
            os.remove(filename)
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
