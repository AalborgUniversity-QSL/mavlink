import sys, struct, time, os
from curses import ascii
import serial
from collections import deque

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

def quad_arm_disarm(m, target_system, arm_disarm) :
        msg = m.mav.command_long_encode(target_system, mavlink.MAV_COMP_ID_ALL, mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, arm_disarm, 0, 0, 0, 0, 0, 0)

        # m.Send(msg,0xD0E3)


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

def quad_cmd_pos(m, target_system, cmd_id, no, x, y, z):
    m.mav.quad_pos_send(
        target_system,
        cmd_id,
        no,
        x,
        y,
        z)

def commander_send(self,target_system,cmd_id):
        if self.mavlink10():
            self.mav.command_long_send(
                self.target_system,  # target_system
                0, # target_component
                mavlink.cmd_id, # command
                0, # confirmation
                1, # param1 (1 to indicate arm)
                0, # param2 (all other params meaningless)
                0, # param3
                0, # param4
                0, # param5
                0, # param6
                0) # param7

def Send(self, msg, addr=0xFFFF, options=0x01, frameid=0x00):
        """
        Inputs:
          msg: A message, in bytes or bytearray format, to be sent to an XBee
          addr: The 16 bit address of the destination XBee
            (default broadcast)
          options: Optional byte to specify transmission options
            (default 0x01: disable ACK)
          frameod: Optional frameid, only used if transmit status is desired
        Returns:
          Number of bytes sent
        """
        if not msg:
            return 0

        hexs = '7E 00 {:02X} 01 {:02X} {:02X} {:02X} {:02X}'.format(
            len(msg) + 5,           # LSB (length)
            frameid,
            (addr & 0xFF00) >> 8,   # Destination address high byte
            addr & 0xFF,            # Destination address low byte
            options
        )
        
        frame = bytearray.fromhex(hexs)
        #  Append message content
        frame.extend(msg)

        # Calculate checksum byte
        frame.append(0xFF - (sum(frame[3:]) & 0xFF))

        # Escape any bytes containing reserved characters
        frame = self.Escape(frame)

        print("Tx: " + self.format(frame))
        return self.serial.write(frame)