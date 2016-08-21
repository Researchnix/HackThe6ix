#
#  main.py
#  HackThe6ix
#
#  Created by Jeffrey, Maliha, Justin  and Lennart on 2016-08-06.
#  Copyright 2016 Researchnix. All rights reserved.
#

import sys
import time

import Master



if __name__ == "__main__":
    t = time.time()

    mas = Master.Master()
    #mas.loadData()
    mas.printState()
    mas.blocked.append((0,3))
    for i in range(17):
        mas.timeStep()
        mas.printCars()
        if i == 6:
            mas.blocked.remove((0,3))

    print "ROUTE CLAC STUFF"
    mas.calculateRoutes()




    print "\n\nDone in " + str(time.time() - t) + " s"
