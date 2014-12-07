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
import parm as pa

pa.index_old = 0

try:
	formation.wait_heartbeat(pa.xbee)
	# 172.26.56.58 is me
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

			formation.quad_arm_disarm(pa.xbee, pa.target_system, ARM)

			print ("1 - ARMING target_system: %u" % (pa.target_system))



		# DISARM
		elif ans[0] == 'd' :
			ARM = False
			if dim > 1 :
				pa.target_system = int(ans[1])
			else:
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL

			formation.quad_arm_disarm(pa.xbee, pa.target_system, ARM)

			print ("2 - DISARMING target_system: %u" % (pa.target_system))


		# START TAKEOFF
		elif ans[0] == 'takeoff' :
			if dim > 1 :
				pa.target_system = int(ans[1])
			else:
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL
			print ("4 - TAKEOFF - target_system: %u" % (pa.target_system))

			pa.first_run = True

			pa.xbee.mav.swarm_commander_send(pa.target_system, mavlink.QUAD_CMD_TAKEOFF);


		elif ans[0] == 'land' :
			if dim > 1 :
				pa.target_system = int(ans[1])
			else:
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL
			print ("4 - LANDING - target_system: %u" % (pa.target_system))

			pa.xbee.mav.swarm_commander_send(pa.target_system, mavlink.QUAD_CMD_LAND);


		# # START SCRIPT
		# elif ans[0] == 'start':
		# 	if dim > 1 :
		# 		pa.target_system = int(ans[1])
		# 		pa.QUAD_CMD = int(ans[2])
		# 	else:
		# 		pa.target_system = mavlink.QUAD_FORMATION_ID_ALL
		# 		pa.QUAD_CMD = mavlink.QUAD_CMD_START
		# 	print ("4 - Start script - target_system: %u  CMD: %u" % (pa.target_system, mavlink.QUAD_CMD_START))

		# 	pa.first_run = True

		# 	try:
		# 		while True:
		# 			formation.wait_statusmsg(pa.xbee)
		# 	except KeyboardInterrupt :
		# 		ARM = False
		# 		pa.QUAD_CMD = mavlink.QUAD_CMD_STOP
		# 		formation.quad_arm_disarm(pa.xbee, pa.target_system, ARM)
		# 		print "\nSTOPPING & DISARMING"
				
		# STOP SCRIPT
		elif ans[0] == 'stop':
			if dim	> 1 :
				pa.target_system = int(ans[1])
			else :
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL

			pa.xbee.mav.swarm_commander_send(pa.target_system, mavlink.QUAD_CMD_STOP) # Check before flight after new implementation
			print ("5 - Stopping script - target_system: %u" %(target_system))


		# LOG STATUSTEXT FROM FORMATION
		elif ans[0] == 'log':
			if dim > 1 :
				pa.target_system = ans[1]
			else:
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL
			
			print "6 - logging - target_system: %u " %(pa.target_system)
			print
			print("Waiting for STATUS_MSG")
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

		print

except KeyboardInterrupt:
        ARM = False
	formation.quad_arm_disarm(pa.xbee, mavlink.QUAD_FORMATION_ID_ALL, ARM)
	print "\nSTOPPING & DISARMING"