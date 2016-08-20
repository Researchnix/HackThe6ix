#
#  Street.py
#  HackThe6ix
#
#  Created by Jeffrey, Maliha, Justin  and Lennart on 2016-08-06.
#  Copyright 2016 Researchnix. All rights reserved.
#

class Street:
    # Every street is connection two interstections in a DIRECTED way
    From = 0
    To = 0
    # Length of street, increments are set to 1 so far
    length = 0



    def __init__(self, From, To, length):
        self.From = From
        self.To= To
        self.length= length
