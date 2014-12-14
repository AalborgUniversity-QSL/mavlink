#!/usr/bin/python

import SocketServer, struct, time, threading
from time import sleep
from dialects.v10 import mavlinkv10 as mavlink
import mav_formation as formation
import numpy as np
import parm as pa
import XBee

# index, x, y, z = 0,0,0,0

class myThread1(threading.Thread):
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
	data = struct.unpack('>' + 'd' * numOfValues, data)

	# pa.index, pa.x, pa.y, pa.z = data[0], [data[1], data[4], 0], [data[2], data[5], 0], [data[3], data[6], 0]

	pa.index = data[0]

	for i in xrange(1,pa.no_of_quad) :
		pa.x[i-1] = data[3*i-2]
		pa.y[i-1] = data[3*i-1]
		pa.z[i-1] = data[3*i]

	if not(pa.initialised) :
		pa.init_pos_z = pa.z
		pa.last_run = int(round(time.time() * 1000))
		pa.initialised = True
		pa.tictoc = False
        else :
        	abs_x = np.absolute(pa.x)
        	abs_y = np.absolute(pa.y)

        	# print "[GCS] x:%.3f y:%.3f z:%.3f" % (abs_x[0], abs_y[0], pa.z[0])
        	pa.xbee.mav.quad_pos_send(
        		mavlink.QUAD_FORMATION_ID_ALL,
        	        pa.x,
        	        pa.y,
        	        np.subtract(pa.z, pa.init_pos_z))

        	# for i in xrange(1,no_of_quad) :
        	# 	if (abs_x[i-1] > pa.sandbox[0]) or (abs_y[i-1] > pa.sandbox[1]) or (z[i-1] > pa.sandbox[2]) :
        	# 		shutdown(i)
        	# 		print "\nOutside sandbox"


        	# if (abs_x[0] > pa.sandbox[0]) or (abs_y[0] > pa.sandbox[1]) or (pa.z[0] > pa.sandbox[2]) :
        	# 	shutdown(mavlink.QUAD_FORMATION_ID_ALL)
        	# 	print "Outside sandbox\n"


                if(pa.vicon_test == True) : 
        		time_diff = int(round(time.time() * 1000)) - pa.last_run
        	        pa.last_run = int(round(time.time() * 1000))

        		print "sample time: %d " % time_diff
        		print "x:%.3f y:%.3f z:%.3f" % (pa.x[0],
        						pa.y[0],
        	        				np.subtract(pa.z[0], pa.init_pos_z[0]))

               	time_diff = int(round(time.time() * 1000)) - pa.last_run
                pa.last_run = int(round(time.time() * 1000))

                if (time_diff > pa.timeout) or pa.index == pa.index_old :
                	shutdown(mavlink.QUAD_FORMATION_ID_ALL)
                	pa.initialised = False
                	print "Vicon timeout\n"

                pa.index_old = pa.index

                # pa.tictoc = not(pa.tictoc)

def get_vicon_data() :
	HOST, PORT = "0.0.0.0", 13001
	server = SocketServer.UDPServer((HOST, PORT), MatlabUDPHandler)
	server.serve_forever()

def shutdown(target_system) :
	formation.quad_arm_disarm(pa.xbee,target_system, False)

# Create new threads
get_vicon = myThread1(1, "VICON\n")
get_vicon.daemon = True