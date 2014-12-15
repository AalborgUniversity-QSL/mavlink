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

try:
	formation.wait_heartbeat(pa.xbee, True)
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
			print ("[GCS] ARMING -> TARGET SYSTEM: %u \n" % (pa.target_system))


		# DISARM
		elif ans[0] == 'd' :
			ARM = False
			if dim > 1 :
				pa.target_system = int(ans[1])
			else:
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL

			formation.quad_arm_disarm(pa.xbee, pa.target_system, ARM)
			print ("[GCS] DISARMING -> TARGET SYSTEM: %u \n" % (pa.target_system))


		# START TAKEOFF
		elif ans[0] == 't' :
			if dim > 1 :
				pa.target_system = int(ans[1])
			else:
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL

			formation.swarm_cmd(pa.xbee, pa.target_system, mavlink.QUAD_CMD_TAKEOFF)
			print ("[GCS] TAKEOFF -> TARGET SYSTEM: %u \n" % (pa.target_system))

			try:
				while True:
					formation.wait_statusmsg(pa.xbee, True)
			except KeyboardInterrupt :
				print

		# START LANDING
		elif ans[0] == 'l' :
			if dim > 1 :
				pa.target_system = int(ans[1])
			else:
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL

			formation.swarm_cmd(pa.xbee, pa.target_system, mavlink.QUAD_CMD_LAND)
			print ("[GCS] LANDING -> TARGET SYSTEM: %u \n" % (pa.target_system))

			try:
				while True:
					formation.wait_statusmsg(pa.xbee, True)
			except KeyboardInterrupt :
				print

		# START SWARMING
		elif ans[0] == 'start' :
			if dim > 1 :
				pa.target_system = int(ans[1])
			else:
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL

			formation.swarm_cmd(pa.xbee, pa.target_system, mavlink.QUAD_CMD_START_SWARM)
			print ("[GCS] START SWARMING -> TARGET SYSTEM: %u \n" % (pa.target_system))


			try:
				while True:
					formation.wait_statusmsg(pa.xbee, True)
			except KeyboardInterrupt :
				print

		# STOP SWARMING
		elif ans[0] == 's' :
			if dim > 1 :
				pa.target_system = int(ans[1])
			else:
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL

			formation.swarm_cmd(pa.xbee, pa.target_system, mavlink.QUAD_CMD_STOP_SWARM)
			print ("[GCS] STOP SWARMING -> TARGET SYSTEM: %u \n" % (pa.target_system))

			try:
				while True:
					formation.wait_statusmsg(pa.xbee, True)
			except KeyboardInterrupt :
				print		


		# LOG STATUSTEXT FROM FORMATION
		elif ans[0] == 'log':
			if dim > 1 :
				pa.target_system = ans[1]
			else:
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL
			
			print "LOGGING -> TARGET SYSTEM: %u \n" %(pa.target_system)

			try:
				while True:
					formation.wait_statusmsg(pa.xbee, True)
			except KeyboardInterrupt :
				print

		else :
			print "WRONG COMMANDO - TRY AGAIN"

except KeyboardInterrupt:
        ARM = False
	formation.quad_arm_disarm(pa.xbee, mavlink.QUAD_FORMATION_ID_ALL, ARM)
	print "\n[GCS] DISARMING"