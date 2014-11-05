#!/usr/bin/env python
import sys, struct, time, os, shlex
import numpy as np
from curses import ascii
from time import sleep
from pymavlink import mavutil
from dialects.v10 import mavlinkv10 as mavlink
from pymavlink import mav_formation as formation

from argparse import ArgumentParser
parser = ArgumentParser(description=__doc__)

parser.add_argument("-b", type=int,
                  help="master port baud rate", default=57600)
parser.add_argument("-d", required=False, help="serial device", default="/dev/ttyUSB0")
parser.add_argument("--source-system", dest='SOURCE_SYSTEM', type=int,
                  default=255, help='MAVLink source system for this GCS')
args = parser.parse_args()

# create a mavlink serial instance
xbee = mavutil.mavlink_connection(args.d, baud=args.b, source_system=args.SOURCE_SYSTEM, dialect="mavlinkv10")

formation.wait_heartbeat(xbee)

while True:
	input = raw_input("FORMATION >> ")
	ans = shlex.split(input)
	dim = len(ans)

	if ans[0] == 'arm' :
		ARM = True

		if dim > 1 :
			target_system = int(ans[1])
		else:
			target_system = mavlink.QUAD_FORMATION_ID_ALL
		print ("1 - Arming target_system: %u" % (target_system))

		formation.quad_arm_disarm(xbee, target_system, ARM)
	elif ans[0] == 'disarm' :
		ARM = False
		if dim > 1 :
			target_system = int(ans[1])
		else:
			target_system = mavlink.QUAD_FORMATION_ID_ALL
		formation.quad_arm_disarm(xbee, target_system, ARM)
		print ("1 - Arming target_system: %u" % (target_system))

	elif ans[0] == 'start':
		if dim > 1 :
			target_system = int(ans[1])
			QUAD_CMD = int(ans[2])
		else:
			target_system = mavlink.QUAD_FORMATION_ID_ALL
			QUAD_CMD = mavlink.QUAD_CMD_START
		print ("1 - Start script - target_system: %u  CMD: %u" % (target_system, QUAD_CMD))

		sample_no = 25
		x = y = z = range(10)

		# Execute the given script
		formation.quad_cmd_pos(xbee, target_system, QUAD_CMD, sample_no, x, y, z)

		while 1:
			formation.wait_statusmsg(xbee)
			pass



	elif ans[0] == 'stop':
		if dim	> 1 :
			target_system = ans[1]
			target_system = int(ans[1])
		else :
			target_system = 0
		print ("2 - Stopping script - target_system: %u" %(target_system))

	elif ans[0] == 'log':
		print "3 - logging"
		target_system = ans[1]

	elif ans[0] == 'help':
		print "start [target_system] [cmd] - Start script"
		print "stop [target_system] - Stopping script"
		print "log [target_system] - logging"
		print "help"
		print "exit - close app"

	elif ans[0] == 'exit':
		print "goodbye!"
		break

	print