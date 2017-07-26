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
'''
LOGGER = logging.getLogger()
logging.basicConfig(level=logging.INFO)
'''
class TrafficIperfServer:
    def __init__(self, server_ip, username, userpassw, run_level="start", iperf_port='9001', transport="both"):
        self.server_ip       = server_ip
        self.username        = username
        self.userpassw       = userpassw
        self.transport       = transport
        self.iperf_port      = iperf_port
        self.run_level       = run_level

        ''' flow data which get updated upon success  '''
        self.flow            = {'listen_ip'   : server_ip, 
                                'listen_port' : iperf_port,
                                'udp_id'      : 'NA',
                                'tcp_id'      : 'NA', 
                                'run_status'  : 'NA',} 

    def create(self):
        ''' forming commands '''
        iperf_cmd_udp   = "iperf --server --bind {0} --udp --port {1} -D".format(self.server_ip, self.iperf_port)
        iperf_cmd_tcp   = "iperf --server --bind {0} --port {1} -D".format(self.server_ip, self.iperf_port)
        iperf_cmd_stop  = "pkill -9 iperf"
        process_udp_id  = "netstat -pan | grep iperf | grep udp | grep -o \'[0-9]\{3,6\}/iperf\' | grep -o \'[0-9]\{3,6\}\'"
        process_tcp_id  = "netstat -pan | grep iperf | grep tcp | grep -o \'[0-9]\{3,6\}/iperf\' | grep -o \'[0-9]\{3,6\}\'"
        run_msg_udp     = "Iperf UDP server {0} has started on port {1} using process id ".format(self.server_ip, self.flow['listen_port'])
        run_msg_tcp     = "Iperf TCP server {0} has started on port {1} using process id ".format(self.server_ip, self.flow['listen_port'])
        run_msg_stop    = "Iperf server {0} stopped by pkill proccess ID(s): ".format(self.server_ip)

        with settings(warn_only=True, host_string=self.server_ip, user=self.username, password=self.userpassw):
            if self.run_level == 'stop':
                process_ids = sudo("pgrep iperf")
                sudo(iperf_cmd_stop)
                self.flow['run_status'] = 'stopped'
                print run_msg_stop + ' ' + process_ids
            else:
                ''' stop running iperf instances '''
                sudo(iperf_cmd_stop)
                if self.transport == 'tcp':
                    run(iperf_cmd_tcp)
                    process_ip_tcp = sudo(process_tcp_id)
                    self.flow['tcp_id'] = process_ip_tcp
                    self.flow['run_status'] = 'started'
                    print run_msg_tcp + process_ip_tcp
                elif self.transport == 'udp':
                    run(iperf_cmd_udp)
                    process_ip_udp = sudo(process_udp_id)
                    self.flow['udp_id'] = process_ip_udp
                    self.flow['run_status'] = 'started'
                    print run_msg_udp + process_ip_udp
                else:
                    run(iperf_cmd_tcp)
                    process_ip_tcp = sudo(process_tcp_id)
                    self.flow['tcp_id'] = process_ip_tcp
                    self.flow['run_status'] = 'started'
                    print run_msg_tcp  + process_ip_tcp
                    run(iperf_cmd_udp)
                    process_ip_udp = sudo(process_udp_id)
                    self.flow['udp_id'] = process_ip_udp
                    print run_msg_udp + process_ip_udp



'''
HOW-TO:
   - instantiate : iperf_server_o = TrafficIperfServer(server_ip=myserver, username=myuser, userpassw=mypassw, run_level=how_run, transport=mytransport)
   - run         : iperf_server_o.create()
   - access flow data, source ip  : print iperf_server_o.flow['listen_ip']
   - access flow data, run status : print iperf_server_o.flow['run_status']
'''

