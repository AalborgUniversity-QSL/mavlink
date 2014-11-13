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
x = np.zeros((10,), dtype = np.float)
y = np.zeros((10,), dtype = np.float)
z = [0.8, -1, -1, -1, -1, -1, -1, -1, -1, -1,]

try:
	formation.wait_heartbeat(xbee)
	# 172.26.56.58 is me
	multi.th.start()

	while True:
		print
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

		# elif ans[0] == 'set_mode' :
		# 	if dim > 1 :
		# 		target_system = int(ans[1])
		# 		mode = int(ans[2])
		# 	else:
		# 		target_system = mavlink.QUAD_FORMATION_ID_ALL
		# 	xbee.set_mode(mode)
		# 	print ("3 - Setting mode - target_system: %u - mode: %u" % (target_system, mode))
		# 	print("Waiting for STATUS_MSG")
		# 	try:
		# 		while True:
		# 			# print index_old
		# 				formation.wait_statusmsg(xbee)
		# 	except KeyboardInterrupt :
		# 		print

		# elif ans[0] == 'set_flag' :
		# 	if dim > 1:
		# 		target_system = int(ans[1])
		# 		flag = int(ans[2])
		# 		enable = int(ans[3])
		# 	xbee.set_mode_flag(flag,enable)
		# 	print ("3 - Setting mode flag - target_system: %u - flag: %u - enable: %u" % (target_system, flag, enable))

		# START SCRIPT
		elif ans[0] == 'start':
			if dim > 1 :
				target_system = int(ans[1])
				QUAD_CMD = int(ans[2])
			else:
				target_system = mavlink.QUAD_FORMATION_ID_ALL
				# QUAD_CMD = mavlink.QUAD_CMD_START
			print ("4 - Start script - target_system: %u  CMD: %u" % (target_system, mavlink.QUAD_CMD_START))
			print
			print("Waiting for STATUS_MSG")

			# try:
			# 	while True:
			# 		# print index_old
			# 		formation.wait_statusmsg(xbee)
			# except KeyboardInterrupt :
			# 	print

			try:
				while True:
					# print index_old
					formation.wait_statusmsg(xbee)
					if multi.index != index_old :
						index_old = multi.index
						formation.wait_statusmsg(xbee)

						xbee.mav.quad_pos_send(
							0,
							target_system,
							mavlink.QUAD_CMD_START,
					        multi.index,
					        multi.x,
					        multi.y,
					        multi.z)

						# formation.quad_cmd_pos(xbee, target_system, QUAD_CMD, multi.index, multi.x, multi.y, multi.z)
						print("index: %u -> [%f,%f,%f]" % (multi.index, multi.x[0], multi.y[0], multi.z[0]))
			except KeyboardInterrupt :
				print

			# try:
			# 	while True:
			# 		# print index_old
			# 		formation.wait_statusmsg(xbee)
			# 		formation.quad_cmd_pos(xbee, target_system, QUAD_CMD, index, x, y, z)
						
			# except KeyboardInterrupt :
			# 	print
		
		# STOP SCRIPT
		elif ans[0] == 'stop':
			if dim	> 1 :
				target_system = int(ans[1])
			else :
				target_system = 0

			formation.quad_cmd_pos(xbee, target_system, mavlink.QUAD_CMD_STOP, multi.index, multi.x, multi.y, multi.z)
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