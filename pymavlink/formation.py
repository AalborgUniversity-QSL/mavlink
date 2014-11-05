#!/usr/bin/env python
import shlex
import numpy as np


while True:
	input = raw_input("FORMATION >> ")
	ans = shlex.split(input)
	dim = len(ans)

	if ans[0] == 'start':
		if dim > 1 :
			target_system = int(ans[1])
			QUAD_CMD = int(ans[2])
		else:
			target_system = QUAD_CMD = 0
		print ("1 - Start script - target_system: %u  CMD: %u" % (target_system, QUAD_CMD))

	elif ans[0] == 'stop':
		if dim	> 1 :
			target_system = ans[1]
			target_system = int(ans[1])
		else:
			target_system = 0
		print ("2 - Stopping script - target_system: %u" %(target_system)

	elif ans[0] == 'log':
		print "3 - logging"
		target_system = ans[1]

	elif ans[0] == 'help':
		print "start [target_system] [cmd] - Start script"
		print "stop [target_system] - Stopping script"
		print "log [target_system] - logging"
		print "help"
		print "exit - close app"

	elif ans[0] == 'exit':
		print "goodbye!"
		break

	print