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
	formation.wait_heartbeat(pa.xbee)
	if pa.two_in_air :
		formation.wait_heartbeat(pa.xbee2)

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

			if pa.two_in_air :
				formation.quad_arm_disarm(pa.xbee2, pa.target_system, ARM)



			print ("[GCS] ARMING -> TARGET SYSTEM: %u \n" % (pa.target_system))


		# DISARM
		elif ans[0] == 'd' :
			ARM = False
			if dim > 1 :
				pa.target_system = int(ans[1])
			else:
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL

			formation.quad_arm_disarm(pa.xbee, pa.target_system, ARM)

			if pa.two_in_air :
				formation.quad_arm_disarm(pa.xbee2, pa.target_system, ARM)

			print ("[GCS] DISARMING -> TARGET SYSTEM: %u \n" % (pa.target_system))


		# START TAKEOFF
		elif ans[0] == 't' :
			if dim > 1 :
				pa.target_system = int(ans[1])
			else:
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL
			print ("[GCS] TAKEOFF -> TARGET SYSTEM: %u \n" % (pa.target_system))


			pa.xbee.mav.swarm_commander_send(pa.target_system, mavlink.QUAD_CMD_TAKEOFF)

			if pa.two_in_air :
				pa.xbee2.mav.swarm_commander_send(pa.target_system, mavlink.QUAD_CMD_TAKEOFF)

			try:
				while True:
					formation.wait_statusmsg(pa.xbee, not(pa.two_in_air))
					if pa.two_in_air :
						formation.wait_statusmsg(pa.xbee2, False)

			except KeyboardInterrupt :
				print

		# START LANDING
		elif ans[0] == 'l' :
			if dim > 1 :
				pa.target_system = int(ans[1])
			else:
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL
			print ("[GCS] LANDING -> TARGET SYSTEM: %u \n" % (pa.target_system))

			pa.xbee.mav.swarm_commander_send(pa.target_system, mavlink.QUAD_CMD_LAND)
			
			if pa.two_in_air :
				pa.xbee2.mav.swarm_commander_send(pa.target_system, mavlink.QUAD_CMD_LAND)

			try:
				while True:
					formation.wait_statusmsg(pa.xbee, not(pa.two_in_air))
					if pa.two_in_air :
						formation.wait_statusmsg(pa.xbee2, False)
			except KeyboardInterrupt :
				print

		# START SWARMING
		elif ans[0] == 'q' :
			if dim > 1 :
				pa.target_system = int(ans[1])
			else:
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL
			print ("[GCS] START SWARMING -> TARGET SYSTEM: %u \n" % (pa.target_system))

			pa.xbee.mav.swarm_commander_send(pa.target_system, mavlink.QUAD_CMD_START_SWARM)

			if pa.two_in_air :
				pa.xbee2.mav.swarm_commander_send(pa.target_system, mavlink.QUAD_CMD_SWARM)

			try:
				while True:
					formation.wait_statusmsg(pa.xbee, not(pa.two_in_air))
					if pa.two_in_air :
						formation.wait_statusmsg(pa.xbee2, False)
			except KeyboardInterrupt :
				print

		# STOP SWARMING
		elif ans[0] == 's' :
			if dim > 1 :
				pa.target_system = int(ans[1])
			else:
				pa.target_system = mavlink.QUAD_FORMATION_ID_ALL
			print ("[GCS] STOP SWARMING -> TARGET SYSTEM: %u \n" % (pa.target_system))

			pa.xbee.mav.swarm_commander_send(pa.target_system, mavlink.QUAD_CMD_STOP_SWARM)
			if pa.two_in_air :
				pa.xbee2.mav.swarm_commander_send(pa.target_system, mavlink.QUAD_CMD_STOP_SWARM)


			try:
				while True:
					formation.wait_statusmsg(pa.xbee, not(pa.two_in_air))
					if pa.two_in_air :
						formation.wait_statusmsg(pa.xbee2, False)
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
					formation.wait_statusmsg(pa.xbee, not(pa.two_in_air))
					if pa.two_in_air :
						formation.wait_statusmsg(pa.xbee2, False)
			except KeyboardInterrupt :
				print

		else :
			print "[GCS] WRONG COMMAND"

except KeyboardInterrupt:
        ARM = False
	formation.quad_arm_disarm(pa.xbee, mavlink.QUAD_FORMATION_ID_ALL, ARM)
	if pa.two_in_air :
		formation.quad_arm_disarm(pa.xbee2, mavlink.QUAD_FORMATION_ID_ALL, ARM)
	print "\n[GCS] DISARMING"