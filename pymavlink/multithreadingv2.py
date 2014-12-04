#!/usr/bin/python

import SocketServer, struct, time, threading
from time import sleep
from dialects.v10 import mavlinkv10 as mavlink
import mav_formation as formation
import numpy as np
import parm as pa

# exitFlag = 0

# x = numpy.zeros((10,), dtype = numpy.float)
# y = numpy.zeros((10,), dtype = numpy.float)
# z = numpy.zeros((10,), dtype = numpy.float)
index, x, y, z = 0,0,0,0

class myThread1 (threading.Thread):
    def __init__(self, threadID, name):
	threading.Thread.__init__(self)
	self.threadID = threadID
	self.name = name
    def run(self):
	print "Starting " + self.name
	get_vicon_data()
	print "Exiting " + self.name

class myThread2 (threading.Thread):
    def __init__(self, threadID, name):
	threading.Thread.__init__(self)
	self.threadID = threadID
	self.name = name
    def run(self):
	print "Starting " + self.name
	send_vicon_data()
	print "Exiting " + self.name

class MatlabUDPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
	global index, x, y, z
	data = self.request[0]
	socket = self.request[0]
	# print "%s wrote:" % self.client_address[0]
	numOfValues = len(data) / 8
	vicn = struct.unpack('>' + 'd' * numOfValues, data)

	index, x, y, z = vicn[0], vicn[1], vicn[2], vicn[3]

	# # Find the number of quadrotors
	# no_of_quad = (len(vicn)-1)/3

	# index = vicn[0]

	# for i in xrange(1,no_of_quad):
	# 	x = vicn[3*i-2]
	# 	y = vicn[3*i-1]
	# 	z = vicn[3*i]

	if pa.transmit :
		if pa.first_run :
			pa.init_pos_x = x
			pa.init_pos_y = y
			pa.init_pos_z = z
			pa.first_run = False
			pa.last_run = int(round(time.time() * 1000))

		abs_x = np.absolute(x - pa.init_pos_x)
		abs_y = np.absolute(y - pa.init_pos_y)

		# print "x:%.3f y:%.3f" % (abs_x, abs_y)

		if abs_x > pa.sandbox[0] or abs_y > pa.sandbox[1] or z > pa.sandbox[2] :
			shutdown()
			print "\nOutside sandbox"
		else :
			pa.xbee.mav.quad_pos_send(
			pa.target_system,
		        x - pa.init_pos_x,
		        y - pa.init_pos_y,
		        z - pa.init_pos_z)

		        if(pa.vicon_test == True) : 
				time_diff = int(round(time.time() * 1000)) - pa.last_run
			        pa.last_run = int(round(time.time() * 1000))

       				# print "sample time: %d " % time_diff
       				print "x:%.3f y:%.3f z:%.3f" % (x- pa.init_pos_x, y - pa.init_pos_y, z - pa.init_pos_z)

	       	time_diff = int(round(time.time() * 1000)) - pa.last_run
	        pa.last_run = int(round(time.time() * 1000))

	        if (time_diff > pa.timeout) or index == pa.index_old :
	        	shutdown()
	        	pa.transmit,first_run = False, True
	        	print "\nVicon timeout"

	        pa.index_old = index

def get_vicon_data() :
	HOST, PORT = "0.0.0.0", 13001
	server = SocketServer.UDPServer((HOST, PORT), MatlabUDPHandler)
	server.serve_forever()

def shutdown() :
	formation.quad_arm_disarm(pa.xbee,pa.target_system, False)
	
	pa.transmit = False

	# pa.xbee.mav.quad_pos_send(pa.target_system, )

# Create new threads
get_vicon = myThread1(1, "Vicon serve")
# send_vicon = myThread2(1, "Formation link")
get_vicon.daemon = True
# send_vicon.daemon = True