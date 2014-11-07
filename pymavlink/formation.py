#!/usr/bin/env python
import sys, struct, time, os, shlex, select
import numpy as np
from curses import ascii
from time import sleep
from pymavlink import mavutil
import multithreading as multi
from dialects.v10 import mavlinkv10 as mavlink
import mav_formation as formation
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

index_old = 0

# For test (BGT) commet after you are done
index = 0
x = y = z = np.zeros((10,), dtype = np.float)

try:
	formation.wait_heartbeat(xbee)
	# multi.th.start() '''<-- starts a thread for update on vicon data'''

	while True:
		input = raw_input("FORMATION >> ")
		ans = shlex.split(input)
		dim = len(ans)

		# ARM
		if ans[0] == 'arm' :
			ARM = True

			if dim > 1 :
				target_system = int(ans[1])
			else:
				target_system = mavlink.QUAD_FORMATION_ID_ALL
			print ("1 - Arming target_system: %u" % (target_system))

			formation.quad_arm_disarm(xbee, target_system, ARM)

		# DISARM
		elif ans[0] == 'disarm' :
			ARM = False
			if dim > 1 :
				target_system = int(ans[1])
			else:
				target_system = mavlink.QUAD_FORMATION_ID_ALL
			formation.quad_arm_disarm(xbee, target_system, ARM)
			print ("2 - Arming target_system: %u" % (target_system))

		elif ans[0] == 'set_mode' :
			if dim > 1 :
				target_system = int(ans[1])
				mode = int(ans[2])
			else:
				target_system = mavlink.QUAD_FORMATION_ID_ALL
			xbee.set_mode(mode)
			print ("3 - Setting mode - target_system: %u - mode: %u" % (target_system, mode))
			print("Waiting for STATUS_MSG")
			try:
				while True:
					# print index_old
						formation.wait_statusmsg(xbee)
			except KeyboardInterrupt :
				print

		elif ans[0] == 'set_flag' :
			if dim > 1:
				target_system = int(ans[1])
				flag = int(ans[2])
				enable = int(ans[3])
			xbee.set_mode_flag(flag,enable)
			print ("3 - Setting mode flag - target_system: %u - flag: %u - enable: %u" % (target_system, flag, enable))

		# elif ans[0] = 'command' :
		# 	for thrust in xrange(0,1000):
		# 		xbee.mav.MAVLink_manual_control_message.__init__(0,0,thrust,0,0)
				


		# START SCRIPT
		elif ans[0] == 'start':
			if dim > 1 :
				target_system = int(ans[1])
				QUAD_CMD = int(ans[2])
			else:
				target_system = mavlink.QUAD_FORMATION_ID_ALL
				QUAD_CMD = mavlink.QUAD_CMD_START
			print ("4 - Start script - target_system: %u  CMD: %u" % (target_system, QUAD_CMD))
			print
			print("Waiting for STATUS_MSG")

			formation.quad_cmd_pos(xbee, target_system, QUAD_CMD, index, x, y, z)

			try:
				while True:
					# print index_old
					formation.wait_statusmsg(xbee)
			except KeyboardInterrupt :
				print


			# try:
			# 	while True:
			# 		# print index_old
			# 		formation.wait_statusmsg(xbee)
			# 		if multi.index != index_old :
			# 			# index_old = multi.index 		'''<-- out comment after test'''
			# 			formation.wait_statusmsg(xbee)
			# 			# formation.quad_cmd_pos(xbee, target_system, QUAD_CMD, multi.index, multi.x, multi.y, multi.z)		'''<-- Sends a command to Pixhawk including Vicon data'''
			# 			# print("index: %u -> [%f,%f,%f],[%f,%f,%f]" % (multi.index, multi.x[1], multi.y[2], multi.z[3], multi.x[4], multi.y[5], multi.z[6]))  '''<-- Debug the vicon data'''
			# except KeyboardInterrupt :
			# 	print
		
		# STOP SCRIPT
		elif ans[0] == 'stop':
			if dim	> 1 :
				target_system = int(ans[1])
			else :
				target_system = 0

			formation.quad_cmd_pos(xbee, target_system, mavlink.QUAD_CMD_STOP, sample_no, x, y, z)
			print ("5 - Stopping script - target_system: %u" %(target_system))

		# LOG STATUSTEXT FROM FORMATION
		elif ans[0] == 'log':
			if dim > 1 :
				target_system = ans[1]
			else:
				target_system = mavlink.QUAD_FORMATION_ID_ALL
			
			print "6 - logging - target_system: %u " %(target_system)
			print
			print("Waiting for STATUS_MSG")
			try:
				while True:
					# print index_old
					formation.wait_statusmsg(xbee)
			except KeyboardInterrupt :
				print

		# HELP
		elif ans[0] == 'help':
			print
			print "ALL COMMANDS HAVE DEFAULT:" 
			print "target_system = 0 (CALL TO ALL)"
			print
			print "arm [target_system]"
			print "disarm [target_system]"
			print "start [target_system] [cmd] - Start script"
			print "stop [target_system] - Stopping script"
			print "log [target_system] - logging"
			print "help"
			print "exit - close app"

		elif ans[0] == 'exit':
			print "goodbye!"
			break

		print

except KeyboardInterrupt:
        print
