import sys, struct, time, os
from curses import ascii
import serial
# from collections import deque

from time import sleep
from pymavlink import mavutil
import parm as pa

from dialects.v10 import mavlinkv10 as mavlink

def wait_heartbeat(self, blocking):
    '''wait for a heartbeat so we know the target system IDs'''
    print("Waiting for APM heartbeat")
    msg = self.recv_match(type='HEARTBEAT', blocking = blocking)
    if msg is not None :
         print("Heartbeat -> system_id: %u" % msg.target_system)

def wait_statusmsg(self, blocking):
    '''wait for a status msg'''
    # print("Waiting for STATUS_MSG")
    msg = self.recv_match(type='STATUSTEXT', blocking = blocking)

    if msg is not None :
        print("[system_id: %u] %s " % msg.target_system, msg)

def quad_arm_disarm(m, target_system, arm_disarm) :
        msg = m.mav.command_long_encode(target_system, mavlink.MAV_COMP_ID_ALL, mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, arm_disarm, 0, 0, 0, 0, 0, 0)
        
        '''
        Send a command with up to seven parameters to the MAV

        target_system             : System which should the position data is for as defined in QUAD_FORMATION_ID enum (uint8_t)
        target_component          : Component which should execute the command, 0 for all components (uint8_t)
        command                   : Command ID, as defined by MAV_CMD enum. (uint16_t)
        confirmation              : 0: First transmission of this command. 1-255: Confirmation transmissions (e.g. for kill command) (uint8_t)
        param1                    : Parameter 1, as defined by MAV_CMD enum. (float)
        param2                    : Parameter 2, as defined by MAV_CMD enum. (float)
        param3                    : Parameter 3, as defined by MAV_CMD enum. (float)
        param4                    : Parameter 4, as defined by MAV_CMD enum. (float)
        param5                    : Parameter 5, as defined by MAV_CMD enum. (float)
        param6                    : Parameter 6, as defined by MAV_CMD enum. (float)
        param7                    : Parameter 7, as defined by MAV_CMD enum. (float)

        '''
        m.mav.sendAPI(msg, pa.system_addr[target_system])

def send_pos(m, target_system, x, y, z) :
        msg = m.mav.quad_pos_encode(target_system, x, y, z)

        '''
        Generate a MAVLink package

        target_system        : System which should the position data is for (uint8_t)
        x                    : x[3] (float)
        y                    : y[3] (float)
        z                    : z[3] (float)

        '''

        m.mav.sendAPI(msg, pa.system_addr[target_system])

def swarm_cmd(m, target_system, cmd) :
        msg = m.mav.swarm_commander_encode(target_system, cmd)

        '''
        Generate a MAVLink package

        target_system        : System which should the position data is for as defined in QUAD_FORMATION_ID enum (uint8_t)
        cmd                  : cmd, as defined in QUAD_CMD enum (uint8_t)

        '''

        m.mav.sendAPI(msg, pa.system_addr[target_system])

