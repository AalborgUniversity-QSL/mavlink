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
# import watchdog
import parm as pa
# import XBee

pa.index_old = 0

try:
	# formation.wait_heartbeat(pa.xbee)
	# watchdog.watchdog.start()
	multi.get_vicon.start()

	pa.vicon_test = False

	while True:
		input = raw_input("\nFORMATION >> ")
		ans = shlex.split(input)
		dim = len(ans)

		# ARM
		if ans[0] == 'a' :

			ARM = True
			if dim > 1 :
				pa.target_system = int(ans[1])
			else:
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL

			pa.first_run = True
			formation.quad_arm_disarm(pa.xbee, pa.target_system, ARM)

			print ("1 - ARMING target_system: %u \n" % (pa.target_system))


		# DISARM
		elif ans[0] == 'd' :
			ARM = False
			if dim > 1 :
				pa.target_system = int(ans[1])
			else:
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL

			pa.first_run = False
			formation.quad_arm_disarm(pa.xbee, pa.target_system, ARM)

			print ("2 - DISARMING target_system: %u \n" % (pa.target_system))


		# START TAKEOFF
		elif ans[0] == 't' :
			if dim > 1 :
				pa.target_system = int(ans[1])
			else:
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL
			print ("4 - TAKEOFF - target_system: %u \n" % (pa.target_system))


			pa.xbee.mav.swarm_commander_send(pa.target_system, mavlink.QUAD_CMD_TAKEOFF)

			try:
				while True:
					formation.wait_statusmsg(pa.xbee)
			except KeyboardInterrupt :
				print

		# START LANDING
		elif ans[0] == 'l' :
			if dim > 1 :
				pa.target_system = int(ans[1])
			else:
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL
			print ("4 - LANDING - target_system: %u \n" % (pa.target_system))

			pa.xbee.mav.swarm_commander_send(pa.target_system, mavlink.QUAD_CMD_LAND)

			try:
				while True:
					formation.wait_statusmsg(pa.xbee)
			except KeyboardInterrupt :
				print

		# START SWARMING
		elif ans[0] == 'start' :
			if dim > 1 :
				pa.target_system = int(ans[1])
			else:
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL
			print ("4 - START SWARMING - target_system: %u \n" % (pa.target_system))

			pa.xbee.mav.swarm_commander_send(pa.target_system, mavlink.QUAD_CMD_START_SWARM)

			try:
				while True:
					formation.wait_statusmsg(pa.xbee)
			except KeyboardInterrupt :
				print

		# STOP SWARMING
		elif ans[0] == 's' :
			if dim > 1 :
				pa.target_system = int(ans[1])
			else:
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL
			print ("4 - STOP SWARMING - target_system: %u \n" % (pa.target_system))

			pa.xbee.mav.swarm_commander_send(pa.target_system, mavlink.QUAD_CMD_STOP_SWARM)

			try:
				while True:
					formation.wait_statusmsg(pa.xbee)
			except KeyboardInterrupt :
				print		


		# LOG STATUSTEXT FROM FORMATION
		elif ans[0] == 'log':
			if dim > 1 :
				pa.target_system = ans[1]
			else:
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL
			
			print "6 - logging - target_system: %u \n" %(pa.target_system)
			print
			print("Waiting for STATUS_MSG \n")
			try:
				while True:
					formation.wait_statusmsg(pa.xbee)
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

except KeyboardInterrupt:
        ARM = False
	formation.quad_arm_disarm(pa.xbee, mavlink.QUAD_FORMATION_ID_ALL, ARM)
	print "DISARMING"