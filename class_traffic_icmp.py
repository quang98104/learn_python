#!/usr/bin/env python

from time import sleep
from fabric.api import settings, parallel, execute
from fabric.operations import run, sudo

import time
import os
import os.path
import logging
import re
import inspect
import yaml
import json

LOGGER = logging.getLogger()
logging.basicConfig(level=logging.INFO)
class TrafficPing:
    def __init__(self, dst_ip, host_ip, username, userpassw, src_ip,  packet_num=10):
        self.host_ip       = host_ip
        self.dst_ip       = dst_ip
        self.username        = username
        self.userpassw       = userpassw
        self.src_ip          = src_ip
        self.packet_num      = packet_num
        ''' flow data which get updated upon success  '''
        self.flow            = {'src_ip'   : self.src_ip, 
                                'dst_ip'   : self.dst_ip, 
                                'flow_time': '', 
                                'pkt_sent' : '', 
                                'pkt_rcvd' : '', 
                                'loss_pkt' : '', 
                                'loss_pct' : ''}

    def create(self):
        LOGGER.info('Start the ping traffic')
        ''' forming commands '''
        icmp_cmd1   = "ping -W 1 -c {0} -I {1} {2} ". format(self.packet_num, self.src_ip, self.dst_ip)
        icmp_cmd2   = "| grep received | sed \'s/[a-zA-Z]\|\%//g\'"
        date_cmd     = "date +%s%3N"
        
        ''' using fabric to ssh into client ip then send ping to server ip '''
        with settings(warn_only=True, host_string=self.host_ip, user=self.username, password=self.userpassw):
            time_before = int(run(date_cmd))
            my_result   = run(icmp_cmd1 + icmp_cmd2)
            time_after  = int(run(date_cmd))
        
        ''' updating flow data  '''
        ''' split 'icmp_flow' list's element then convert into integer '''
        icmp_flow = map(int, my_result.split(","))
        my_flow_time = (time_before + time_after)/2
        my_loss_pkt = icmp_flow[0] - icmp_flow[1]
        self.flow['flow_time']  = time_after
        self.flow['pkt_sent']   = icmp_flow[0]
        self.flow['pkt_rcvd']   = icmp_flow[1]
        self.flow['loss_pct']   = icmp_flow[2]
        self.flow['loss_pkt']   = my_loss_pkt

'''
HOW-TO:
   - instantiate : ping_o = TrafficPing(host_ip="10.24.9.18", dst_ip="www.yahoo.com", username='root', userpassw='testpass1', packet_num="4")
   - run         : ping_o.create()
   - access flow data, source ip : print ping_o.flow['src_ip']
   - access flow data, loss %    : print ping_o.flow['loss_pct']
'''
