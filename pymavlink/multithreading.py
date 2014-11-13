#!/usr/bin/python

import SocketServer, struct, time, threading, numpy
from time import sleep

# exitFlag = 0

index = 0
x = numpy.zeros((10,), dtype = numpy.float)
y = numpy.zeros((10,), dtype = numpy.float)
z = numpy.zeros((10,), dtype = numpy.float)

class myThread (threading.Thread):
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
        global index, x, y, z
        data = self.request[0]
        socket = self.request[0]
        # print "%s wrote:" % self.client_address[0]
        numOfValues = len(data) / 8
        vicn = struct.unpack('>' + 'd' * numOfValues, data)
        index = vicn[0]
        x = ([ vicn[1],vicn[4],vicn[7],vicn[10],vicn[13],vicn[16],vicn[19],vicn[22],vicn[25],vicn[28] ])
        y = ([ vicn[2],vicn[5],vicn[8],vicn[11],vicn[14],vicn[17],vicn[20],vicn[23],vicn[26],vicn[29] ])
        z = ([ vicn[3],vicn[6],vicn[9],vicn[12],vicn[15],vicn[18],vicn[21],vicn[24],vicn[27],vicn[30] ])

def get_vicon_data() :
        HOST, PORT = "0.0.0.0", 801
        server = SocketServer.UDPServer((HOST, PORT), MatlabUDPHandler)
        server.serve_forever()


# Create new threads
th = myThread(1, "vicon")
th.daemon = True