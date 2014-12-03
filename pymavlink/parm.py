#!/usr/bin/env python
import sys, struct, time, os, shlex, select
from argparse import ArgumentParser
from pymavlink import mavutil

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
no_of_quad = 1

sandbox = [1000, 1000, 500]
