#!/usr/bin/python

import struct, time, threading
from time import sleep
from dialects.v10 import mavlinkv10 as mavlink
import mav_formation as formation
import numpy as np
import parm as pa

class myThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print "Starting " + self.name
        watchdog()
        print "Exiting " + self.name


def watchdog() :
        while True :
                if ( pa.tictoc ) :
                        pa.time = int(round(time.time() * 1000))
                        pa.tictoc = not(pa.tictoc)

                pa.dt = int(round(time.time() * 1000)) - pa.time

                if (pa.dt > pa.timeout) :
                        shutdown(mavlink.QUAD_FORMATION_ID_ALL)
                        print "\nVICON TIMEOUT"


def shutdown(target_system) :
        formation.quad_arm_disarm(pa.xbee,target_system, False)

watchdog = myThread(1, "WATCHDOG\n")
watchdog.daemon = True