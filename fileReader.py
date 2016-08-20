#
#  FileReader.py
#  HackThe6ix
#
#  Created by Jeffrey, Maliha, Justin  and Lennart on 2016-08-06.
#  Copyright 2016 Researchnix. All rights reserved.
#

class FileReader:
    """ Class to read in files that contain the map information """
    
    def loadIntersections(self, filename):
        x, y = loadtxt(filename, unpack=True)
