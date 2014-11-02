#!/usr/bin/env python

'''
test mavlink messages
'''

import sys, struct, time, os
from curses import ascii

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
    print("Heartbeat from APM (system %u component %u)" % (m.target_system, m.target_system))

# create a mavlink serial instance
master = mavutil.mavlink_connection(args.d, baud=args.b, source_system=args.SOURCE_SYSTEM)

# wait for the heartbeat msg to find the system ID
wait_heartbeat(master)

# class fifo(object):
#     def __init__(self):
#         self.buf = []
#     def write(self, data):
#         self.buf += data
#         return len(data)
#     def read(self):
#         return self.buf.pop(0)

# f = fifo()

# mav = mavlink.MAVLink(f)

# # set the WP_RADIUS parameter on the MAV at the end of the link
# mav.param_set_send(7, 1, "WP_RADIUS", 101, mavlink.MAV_PARAM_TYPE_REAL32)

# # alternatively, produce a MAVLink_param_set object 
# # this can be sent via your own transport if you like
# m = mav.param_set_encode(7, 1, "WP_RADIUS", 101, mavlink.MAV_PARAM_TYPE_REAL32)

# # get the encoded message as a buffer
# b = m.get_msgbuf()

# # decode an incoming message
# m2 = mav.decode(b)

# #print("Got a message with id %u" % (m2.get_msgId())
# print(m2)

#master.set_mode_flag(1,128)
master.mav.command_long_send(1,0,mavlink.MAV_CMD_COMPONENT_ARM_DISARM,0,0,0,0,0,0,0,0)
#master.mav.command_long_send(1,0,42,0,0,0,0,0,0,0,0)