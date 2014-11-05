import sys, struct, time, os
from curses import ascii

from time import sleep
from pymavlink import mavutil
from dialects.v10 import mavlinkv10 as mavlink

def wait_heartbeat(m):
    '''wait for a heartbeat so we know the target system IDs'''
    print("Waiting for APM heartbeat")
    msg = m.recv_match(type='HEARTBEAT', blocking=True)
    print("Heartbeat from APM (system %u component %u)" % (m.target_system, m.target_component))

def wait_statusmsg(m):
    '''wait for a status msg'''
    # print("Waiting for STATUS_MSG")
    msg = m.recv_match(type='STATUSTEXT', blocking=False)

    if msg is not None :
        print(msg)

def quad_arm_disarm(m, target_system, arm_disarm):
    m.mav.command_long_send(
        m.target_system,
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

def quad_cmd_pos(m, target_system, cmd_id, no, x, y, z):
    m.mav.quad_pos_send(
        target_system,
        cmd_id,
        no,
        x,
        y,
        z)