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

    # Initialize the Master and check its state
    mas = Master.Master()
    mas.printState()


    # Do a time step
    for i in range(30):
        mas.timeStep()
        mas.printCars()
        if i == 10:
            mas.changeInterState(2, 'horizontal')
        if i == 20:
            mas.changeInterState(2, 'vertical')



    print "\n\nDone in " + str(time.time() - t) + " s"
