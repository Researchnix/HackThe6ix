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

    trafficHandler = Master.Master()

    print "\n\nDone in " + str(time.time() - t) + " s"
