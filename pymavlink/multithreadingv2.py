#!/usr/bin/python

import SocketServer, struct, time, threading
from time import sleep
from dialects.v10 import mavlinkv10 as mavlink
import mav_formation as formation
import numpy as np
import parm as pa

# index, x, y, z = 0,0,0,0


class myThread1 (threading.Thread):
    def __init__(self, threadID, name):
	threading.Thread.__init__(self)
	self.threadID = threadID
	self.name = name
    def run(self):
	print "Starting " + self.name
	get_vicon_data()
	print "Exiting " + self.name

class MatlabUDPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
	data = self.request[0]
	socket = self.request[0]
	# print "%s wrote:" % self.client_address[0]
	numOfValues = len(data) / 8
	vicn = struct.unpack('>' + 'd' * numOfValues, data)

	# index, x, y, z = vicn[0], vicn[1], vicn[2], vicn[3]

	# Find the number of quadrotors
	# no_of_quad = (len(vicn)-1)/3

	no_of_quad = 1

	pa.index = vicn[0]

	for i in xrange(1,no_of_quad) :
		pa.x[i-1] = vicn[3*i-2]
		pa.y[i-1] = vicn[3*i-1]
		pa.z[i-1] = vicn[3*i]

	if pa.first_run :
		pa.init_pos_x = pa.x
		pa.init_pos_y = pa.y
		pa.init_pos_z = pa.z
		pa.first_run = False
		pa.last_run = int(round(time.time() * 1000))

	abs_x = np.absolute(np.subtract(pa.x, pa.init_pos_x))
	abs_y = np.absolute(np.subtract(pa.y, pa.init_pos_y))

	# print "x:%.3f y:%.3f" % (abs_x, abs_y)
	pa.xbee.mav.quad_pos_send(
		mavlink.QUAD_FORMATION_ID_ALL,
	        np.subtract(pa.x, pa.init_pos_x),
	        np.subtract(pa.y, pa.init_pos_y),
	        np.subtract(pa.z, pa.init_pos_z))

	for i in xrange(1,no_of_quad) :
		if (abs_x[i-1] > pa.sandbox[0]) or (abs_y[i-1] > pa.sandbox[1]) or (z[i-1] > pa.sandbox[2]) :
			shutdown(i)
			print "\nOutside sandbox"


        if(pa.vicon_test == True) : 
		time_diff = int(round(time.time() * 1000)) - pa.last_run
	        pa.last_run = int(round(time.time() * 1000))

		# print "sample time: %d " % time_diff
		print "x:%.3f y:%.3f z:%.3f" % (np.subtract(pa.x, pa.init_pos_x),
						np.subtract(pa.y, pa.init_pos_y),
	        				np.subtract(pa.z, pa.init_pos_z))

       	time_diff = int(round(time.time() * 1000)) - pa.last_run
        pa.last_run = int(round(time.time() * 1000))

        if (time_diff > pa.timeout) or index == pa.index_old :
        	shutdown(mavlink.QUAD_FORMATION_ID_ALL)
        	first_run = True
        	print "\nVicon timeout"

        pa.index_old = index

def get_vicon_data() :
	HOST, PORT = "0.0.0.0", 13001
	server = SocketServer.UDPServer((HOST, PORT), MatlabUDPHandler)
	server.serve_forever()

def shutdown(target_system) :
	formation.quad_arm_disarm(pa.xbee,target_system, False)

# Create new threads
get_vicon = myThread1(1, "\nVicon serve")
get_vicon.daemon = True