import sys, struct, time, os
from curses import ascii
import serial
from collections import deque

from time import sleep
from pymavlink import mavutil
import parm as pa

from dialects.v10 import mavlinkv10 as mavlink

def wait_heartbeat(self):
    '''wait for a heartbeat so we know the target system IDs'''
    print("Waiting for APM heartbeat")
    msg = self.recv_match(type='HEARTBEAT', blocking=True)
    print("Heartbeat -> system_id: %u" % msg.target_system)

def wait_statusmsg(m):
    '''wait for a status msg'''
    # print("Waiting for STATUS_MSG")
    msg = m.recv_match(type='STATUSTEXT', blocking=False)

    if msg is not None :
        print(msg)

def quad_arm_disarm(m, target_system, arm_disarm) :
        msg = m.mav.command_long_encode(
                target_system,
                mavlink.MAV_COMP_ID_ALL,
                mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                0,
                arm_disarm,
                0,
                0,
                0,
                0,
                0,
                0)

        m.mav.sendAPI(msg, pa.system_addr[target_system])

    # m.mav.command_long_send(
    #     target_system,
    #     mavlink.MAV_COMP_ID_ALL,
    #     mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    #     0,
    #     arm_disarm,
    #     0,
    #     0,
    #     0,
    #     0,
    #     0,
    #     0)