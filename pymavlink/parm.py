#!/usr/bin/env python
import sys, struct, time, os, shlex, select
from argparse import ArgumentParser
from pymavlink import mavutil
import mav_formation as formation
import numpy as np

parser = ArgumentParser(description=__doc__)

parser.add_argument("-b", required=False, type=int, help="master port baud rate", default=57600)
parser.add_argument("-d1", required=True, help="serial device 1")
parser.add_argument("-d2", required=False, help="serial device 2")
parser.add_argument("--source-system", required=False, dest='SOURCE_SYSTEM', type=int,
                  default=255, help='MAVLink source system for this GCS')

args = parser.parse_args()

# create a mavlink serial instance
xbee = mavutil.mavlink_connection(args.d1, baud=args.b, source_system=args.SOURCE_SYSTEM, dialect="mavlinkv10")

if args.d2 is not None :
        xbee2 = mavutil.mavlink_connection(args.d2, baud=args.b, source_system=args.SOURCE_SYSTEM, dialect="mavlinkv10")
        two_in_air = True
else :
        two_in_air = False

target_system = 0
QUAD_CMD = 0
transmit = False
first_run = True
initialised = False
last_run = int(round(time.time() * 1000))
vicon_test = False
index_old = 0
timeout,time,dt = 2000,0,0
tictoc = False


index = 0
x = np.zeros((3,), dtype=np.float)
y = np.zeros((3,), dtype=np.float)
z = np.zeros((3,), dtype=np.float)

init_pos_x = np.zeros((3,), dtype=np.float)
init_pos_y = np.zeros((3,), dtype=np.float)
init_pos_z = np.zeros((3,), dtype=np.float)

sandbox = [2000, 2000, 2000]
sandbox_shutdown =[2200,2200,2500]
