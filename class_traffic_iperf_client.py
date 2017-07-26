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
import unittest

class TrafficIperfClient:
    def __init__(self, server_ip, client_ip, username='ubuntu', userpassw='ubuntu', iperf_time=0, iperf_port='9001', transport="tcp"):
        self.server_ip       = server_ip
        self.client_ip       = client_ip
        self.username        = username
        self.userpassw       = userpassw
        self.transport       = transport
        self.iperf_port      = iperf_port
        self.iperf_time      = iperf_time

        ''' flow data which get updated upon success  '''
        self.flow            = {'src_ip'   : '',
                                'src_port' : '',
                                'dst_ip'   : '',
                                'dst_port' : '',
                                'flow_time': ''}

    def create(self):
        ''' forming commands '''
        iperf_cmd_udp         = "iperf -y C --client {0} -n 500 --udp --port {1}".format(self.server_ip, self.iperf_port)
        iperf_cmd_tcp         = "iperf -y C --client {0} -n 500 --port {1}".format(self.server_ip, self.iperf_port)
        iperf_cmd_time_udp    = "iperf -y C --client {0} -t {1} --udp --port {2}".format(self.server_ip, self.iperf_time, self.iperf_port)
        iperf_cmd_time_tcp    = "iperf -y C --client {0} -t {1} --port {2}".format(self.server_ip, self.iperf_time, self.iperf_port)
        date_cmd              = "date +%s%3N"

        ''' start ssh, get date in miliseconds, then send iperf traffic, get date again  '''
        with settings(warn_only=True, host_string=self.client_ip, user=self.username, password=self.userpassw):
            if self.iperf_time == 0:
                if self.transport == 'udp':
                    time_before = int(run(date_cmd))
                    my_result   = run(iperf_cmd_udp)
                    time_after  = int(run(date_cmd))
                else:
                    time_before = int(run(date_cmd))
                    my_result   = run(iperf_cmd_tcp)
                    time_after  = int(run(date_cmd))
            else:
                if self.transport == 'udp':
                    time_before = int(run(date_cmd))
                    my_result   = run(iperf_cmd_udp)
                    time_after  = int(run(date_cmd))
                else:
                    time_before = int(run(date_cmd))
                    my_result   = run(iperf_cmd_tcp)
                    time_after  = int(run(date_cmd))

        iperf_flow = my_result.split(",")

        ''' flow time is average of 'time_before' and 'time_after' '''
        my_flow_time = (time_before + time_after)/2
        print iperf_flow
        ''' updating out data flow data  '''
        self.flow['flow_time'] = my_flow_time
        self.flow['src_ip']    = iperf_flow[1]
        self.flow['src_port']  = iperf_flow[2]
        self.flow['dst_ip']    = iperf_flow[3]
        self.flow['dst_port']  = iperf_flow[4]
        print self.flow


'''
HOW-TO:
   - instantiate : iperf_client_o = TrafficIperfClient(client_ip=myclient, server_ip=myserver, username='root', userpassw=mypassw, transport=mytransport) 
   - run         : iperf_client_o.create()
   - access flow data, source ip : print iperf_client_o.flow['src_ip']
   - access flow data, loss %    : print iperf_client_o.flow['flow_time']
'''


