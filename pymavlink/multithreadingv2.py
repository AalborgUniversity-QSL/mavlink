#!/usr/bin/python

import SocketServer, struct, time, threading, numpy
from time import sleep
from dialects.v10 import mavlinkv10 as mavlink

# exitFlag = 0

# x = numpy.zeros((10,), dtype = numpy.float)
# y = numpy.zeros((10,), dtype = numpy.float)
# z = numpy.zeros((10,), dtype = numpy.float)
index, x, y, z = 0,0,0,0
transmit = False
QUAD_CMD = 0;

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
	# index = vicn[0]
	# x = ([ vicn[1],vicn[4],vicn[7],vicn[10],vicn[13],vicn[16],vicn[19],vicn[22],vicn[25],vicn[28] ])
	# y = ([ vicn[2],vicn[5],vicn[8],vicn[11],vicn[14],vicn[17],vicn[20],vicn[23],vicn[26],vicn[29] ])
	# z = ([ vicn[3],vicn[6],vicn[9],vicn[12],vicn[15],vicn[18],vicn[21],vicn[24],vicn[27],vicn[30] ])
	index, x, y, z = vicn[0], vicn[1], vicn[2], vicn[3]

def get_vicon_data() :
	HOST, PORT = "0.0.0.0", 801
	server = SocketServer.UDPServer((HOST, PORT), MatlabUDPHandler)
	server.serve_forever()

def send_vicon_data() :
	global index, x, y, z, transmit, xbee
	index_old = 0;
	while True:
		if transmit and (index != index_old) :
			index_old = index
			xbee.mav.quad_pos_send(
			target_system,
			QUAD_CMD,
		        index,
		        x,
		        y,
		        z)

			# print("index: %u -> [%f,%f,%f]" % (index, x, y, z))

# Create new threads
get_vicon = myThread1(1, "Vicon serve")
send_vicon = myThread2(1, "Formation link")
get_vicon.daemon = True
send_vicon.daemon = True