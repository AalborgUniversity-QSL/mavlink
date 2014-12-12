#!/usr/bin/env python
import sys, struct, time, os, shlex, select
from argparse import ArgumentParser
from pymavlink import mavutil
import mav_formation as formation
import numpy as np

parser = ArgumentParser(description=__doc__)

parser.add_argument("-b", type=int,
                  help="master port baud rate", default=57600)
parser.add_argument("-d", required=False, help="serial device", default="/dev/ttyUSB0")
parser.add_argument("--source-system", dest='SOURCE_SYSTEM', type=int,
                  default=255, help='MAVLink source system for this GCS')

args = parser.parse_args()

# create a mavlink serial instance
xbee = mavutil.mavlink_connection(args.d, baud=args.b, source_system=args.SOURCE_SYSTEM, dialect="mavlinkv10")

target_system = 0
QUAD_CMD = 0
transmit = False
first_run = True
# no_of_quad = 1
last_run = int(round(time.time() * 1000))
vicon_test = False
index_old = 0
timeout,time_diff = 2000,0
data_recived = False

index = 0
x = np.zeros((3,), dtype=np.float)
y = np.zeros((3,), dtype=np.float)
z = np.zeros((3,), dtype=np.float)

init_pos_x = np.zeros((3,), dtype=np.float)
init_pos_y = np.zeros((3,), dtype=np.float)
init_pos_z = np.zeros((3,), dtype=np.float)

sandbox = [1000, 1500, 1500]
