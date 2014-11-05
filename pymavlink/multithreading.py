#!/usr/bin/python

import SocketServer, struct, time, threading
from time import sleep

# exitFlag = 0

x = y = z = 3

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
        global x, y, z
        data = self.request[0]
        socket = self.request[0]
        # print "%s wrote:" % self.client_address[0]
        numOfValues = len(data) / 8
        unp = struct.unpack('>' + 'd' * numOfValues, data)
        x = unp[0]
        y = unp[1]
        z = unp[2]

# def print_time(threadName, delay, counter):
#     while counter:
#         if exitFlag:
#             thread.exit()
#         time.sleep(delay)
#         print "%s: %s" % (threadName, time.ctime(time.time()))
#         counter -= 1

def get_vicon_data():
    HOST, PORT = "0.0.0.0", 801
    server = SocketServer.UDPServer((HOST, PORT), MatlabUDPHandler)
    server.serve_forever()

# Create new threads
thread1 = myThread(1, "vicon")
# thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
# thread2.start()

try:

    while True:
        print ("%d,%d,%d" % (x,y,z) )
        sleep(0.1)
except(KeyboardInterrupt, SystemExit):
    clean_stop_thread;
    sys.exit()
    # print "Exiting Main Thread"