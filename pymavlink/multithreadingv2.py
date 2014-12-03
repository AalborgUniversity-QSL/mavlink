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

	# index, x, y, z = vicn[0], vicn[1], vicn[2], vicn[3]

	# Find the number of quadrotors
	no_of_quad = (len(vicn)-1)/3

	index = vicn[0]

	for i in xrange(1,no_of_quad):
		x = vicn[3*i-2]
		y = vicn[3*i-1]
		z = vicn[3*i]

def get_vicon_data() :
	HOST, PORT = "0.0.0.0", 801
	server = SocketServer.UDPServer((HOST, PORT), MatlabUDPHandler)
	server.serve_forever()

def send_vicon_data() :
	global index, x, y, z
	index_old = 0;
	timeout,time_diff = 1000,0
	last_run = int(round(time.time() * 1000))
	data_recived = False
	first_no_data = True

	# time2kill = 5000 
	while True:
		if pa.transmit and (index != index_old) :
			index_old = index

			# # For test of safty cutoff
			# if pa.first_run :
			# 	last_run = int(round(time.time() * 1000))
			# 	pa.first_run = False
			# if time2kill > (int(round(time.time() * 1000)) - last_run) :
			# 	pa.xbee.mav.quad_pos_send(
			# 	pa.target_system,
			# 	pa.QUAD_CMD,
			#         index,
			#         x,
			#         y,
			#         z)

			# else :
			# 	print "not sending"

			if pa.first_run :
				init_pos_x = x
				init_pos_y = y
				init_pos_z = z
				pa.first_run = False
				last_run = int(round(time.time() * 1000))

			abs_x = np.absolute(x - init_pos_x)
			abs_y = np.absolute(y - init_pos_y)

			# print "x:%.3f y:%.3f" % (abs_x, abs_y)

			if abs_x > pa.sandbox[0] or abs_y > pa.sandbox[1] or z > pa.sandbox[2] :
				shutdown()
				print "Outside sandbox"
			else :
				# pa.xbee.mav.quad_pos_send(
				# pa.target_system,
				# pa.QUAD_CMD,
			 #        index,
			 #        x - init_pos_x,
			 #        y - init_pos_y,
			 #        z - init_pos_z)

			        time_diff = int(round(time.time() * 1000)) - last_run
			        last_run = int(round(time.time() * 1000))

			        print "sample time: %.3f " % time_diff

			        first_no_data = True

		elif pa.transmit and (index == index_old) :
			if first_no_data :
				time_off = int(round(time.time() * 1000))
				first_no_data = False

			if (int(round(time.time() * 1000)) - time_off) > timeout :
				shutdown()
				pa.transmit, first_no_data,first_run = False, True, True
				print "Vicon timeout"


def shutdown() :
	formation.quad_arm_disarm(pa.xbee,pa.target_system, False)
				
	pa.xbee.mav.quad_pos_send(
	pa.target_system,
	mavlink.QUAD_CMD_STOP,
	0,
	0,
	0,
	0)



# Create new threads
get_vicon = myThread1(1, "Vicon serve")
send_vicon = myThread2(1, "Formation link")
get_vicon.daemon = True
send_vicon.daemon = True