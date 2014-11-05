#!/usr/bin/env python

import sys, struct, time, os
from curses import ascii

from time import sleep
from pymavlink import mavutil
import numpy as np
from dialects.v10 import mavlinkv10 as mavlink

from argparse import ArgumentParser
parser = ArgumentParser(description=__doc__)

parser.add_argument("-b", type=int,
                  help="master port baud rate", default=57600)
parser.add_argument("-d", required=False, help="serial device", default="/dev/ttyUSB0")
parser.add_argument("--source-system", dest='SOURCE_SYSTEM', type=int,
                  default=255, help='MAVLink source system for this GCS')
args = parser.parse_args()

def wait_heartbeat(m):
    '''wait for a heartbeat so we know the target system IDs'''
    print("Waiting for APM heartbeat")
    msg = m.recv_match(type='HEARTBEAT', blocking=True)
    print("Heartbeat from APM (system %u component %u)" % (m.target_system, m.target_component))

def wait_statusmsg(m):
    '''wait for a status msg'''
    print("Waiting for STATUS_MSG")
    msg = m.recv_match(type='STATUSTEXT', blocking=True)
    print(msg)

def quad_arm_disarm(m, target_system, arm_disarm):
    master.mav.command_long_send(
        m.target_system,
        m.MAV_COMP_ID_ALL,
        m.MAV_CMD_COMPONENT_ARM_DISARM,
        0,
        arm_disarm,
        0,
        0,
        0,
        0,
        0,
        0)


ARM = True
DISARM = False
NO_OF_QUADS = 10

x = y = np.zeros((1,NO_OF_QUADS),dtype=np.int16)

z = np.zeros((1,NO_OF_QUADS),dtype=np.int16)

z[:] = -1

# create a mavlink serial instance
xbee = mavutil.mavlink_connection(args.d, baud=args.b, source_system=args.SOURCE_SYSTEM)

# wait for the heartbeat msg to find the system ID
wait_heartbeat(xbee)

quad_arm_disarm(xbee, QUAD_FORMATION_ID_1, ARM)


while 1:
    wait_statusmsg(xbee)

    master.mav.quad_pos_send(
    QUAD_FORMATION_ID_1,
    QUAD_CMD_START,
    NO,
    x,
    y,
    z)

    Sleep(10)

quad_arm_disarm(DISARM)