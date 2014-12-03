#!/usr/bin/env python
import sys, struct, time, os, shlex, select
import numpy as np
from curses import ascii
from time import sleep
from pymavlink import mavutil
from dialects.v10 import mavlinkv10 as mavlink
import mav_formation as formation
from argparse import ArgumentParser
import multithreadingv2 as multi
import parm as pa

pa.vicon_test = True
multi.get_vicon.start()

try :
        while True :
                pass
except KeyboardInterrupt:
        print