#!/usr/bin/python
import SocketServer, struct, time
from time import sleep

class MatlabUDPHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		data = self.request[0]
		socket = self.request[0]
		# print "%s wrote:" % self.client_address[0]
		numOfValues = len(data) / 8
		unp = struct.unpack('>' + 'd' * numOfValues, data)
		print unp


def get_vicon_data(self):
	HOST, PORT = "0.0.0.0", 801
	server = SocketServer.UDPServer((HOST, PORT), MatlabUDPHandler)
	server.serve_forever()	