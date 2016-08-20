#
#  Master.py
#  HackThe6ix
#
#  Created by Jeffrey, Maliha, Justin  and Lennart on 2016-08-06.
#  Copyright 2016 Researchnix. All rights reserved.
#

import Map

# the main traffic coordinator
class Master:

    def test(self):
        m = Map.Map()
        m.addIntersection('a')
        m.addIntersection('b')
        m.addIntersection('c')

        m.addStreet(0,1,10)
        m.addStreet(1,2,10)

        print '\nintersections: '
        print m.intersections
        print '\n'
        print '\nstreets: '
        print m.streets
        print '\n'

