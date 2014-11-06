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
        unp = struct.unpack('>' + 'd' * numOfValues, data)
        index = unp[0]
        x = ([ unp[1],unp[4],unp[7],unp[10],unp[13],unp[16],unp[19],unp[22],unp[25],unp[28] ])
        y = ([ unp[2],unp[5],unp[8],unp[11],unp[14],unp[17],unp[20],unp[23],unp[26],unp[29] ])
        z = ([ unp[3],unp[6],unp[9],unp[12],unp[15],unp[18],unp[21],unp[24],unp[27],unp[30] ])

def get_vicon_data():
    HOST, PORT = "0.0.0.0", 801
    server = SocketServer.UDPServer((HOST, PORT), MatlabUDPHandler)
    server.serve_forever()

# Create new threads
th = myThread(1, "vicon")
th.daemon = True
# # thread2 = myThread(2, "Thread-2", 2)

# # Start new Threads
# th.start()
# # thread2.start()

# try:

#     while True:
#         print ("%d,%d,%d" % (x,y,z) )
#         sleep(0.1)
# except(KeyboardInterrupt, SystemExit):
#     print