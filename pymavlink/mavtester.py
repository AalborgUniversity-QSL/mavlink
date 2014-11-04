#!/usr/bin/env python

'''
test mavlink messages
'''

import sys, struct, time, os
from curses import ascii

from time import sleep
from pymavlink import mavutil
from dialects.v10 import mavlinkv10 as mavlink

from argparse import ArgumentParser
parser = ArgumentParser(description=__doc__)

parser.add_argument("-b", type=int,
                  help="master port baud rate", default=57600)
parser.add_argument("-d", required=True, help="serial device")
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

def quad_arm_disarm(state):
    master.mav.command_long_send(
        mavlink.QUAD_FORMATION_ID_1,
        mavlink.MAV_COMP_ID_ALL,
        mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,
        state,
        0,
        0,
        0,
        0,
        0,
        0)
    print("Armed: %d" % (state))

ARM = True
DISARM = False


# create a mavlink serial instance
master = mavutil.mavlink_connection(args.d, baud=args.b, source_system=args.SOURCE_SYSTEM)

# wait for the heartbeat msg to find the system ID
wait_heartbeat(master)

quad_arm_disarm(ARM)


# master.mav.command_int_send(
#     mavlink.QUAD_FORMATION_ID_1,
#     0,
#     0,
#     mavlink.MAV_CMD_FORMATION_CONTROL_START,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0)

wait_statusmsg(master)

sleep(10)

quad_arm_disarm(DISARM)