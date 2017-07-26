#!/usr/bin/env python
from time import sleep
from fabric.api import settings, parallel, execute
from fabric.operations import run, sudo

import time
import sys
import os
import os.path
import logging
import re
import inspect
import yaml
import json
import unittest

class TrafficHttp:
    '''
    Class to ssh into a host (client_ip) and make http request using curl.
    It also provide flow and some http data; see 'self.flow' below
    HOW-TO:
   - instantiate : http_o = TrafficHttp(client_ip="10.24.9.18", url="www.yahoo.com", username='root', userpassw='testpass1', http_port=8081)
   - run         : http_o.create()
   - access flow data, source ip : print http_o.flow['src_ip']
   - access flow data, loss %    : print http_o.flow['rsp_code']
    '''
    def __init__(self, client_ip, username, userpassw, url="www.cloudgenix.com", http_port='80'):
        self.client_ip       = client_ip
        self.username        = username
        self.userpassw       = userpassw
        self.url             = url
        self.http_port       = http_port

        ''' Accessible flow data which get updated after curl execution
            src_ip      = source ip as reported by curl
            src_port    = source port as reported by curl 
            dst_ip      = destination ip as reported by curl
            dst_port    = destination port as reported by curl 
            flow_time   = approximate time of curl execution based on sending host's time
            rsp_code    = server's http response code
            conn_time   = second(s) it takes for transport protocol, TCP, to start/end connection
        '''
        self.flow            = {'src_ip'   : None, 
                                'src_port' : None,
                                'dst_ip'   : None,
                                'dst_port' : '', 
                                'flow_time': None, 
                                'rsp_code' : 'FAIL',
                                'conn_time': ''} 

    def create(self):
        ''' forming commands '''
        curl_cmd1    = "curl --show-error --max-time 2 --connect-timeout 1 --tcp-nodelay "
        curl_cmd2    = "--write-out \"%{local_ip}\\t%{local_port}\\t%{remote_ip}\\t%{remote_port}\\t%{http_code}\\t%{time_connect}\\n\" -o /dev/null -s "
        curl_cmd3    = " -o /dev/null -s http://{0}:{1}/".format(self.url, self.http_port)
        date_cmd     = "date +%s%3N"

        with settings(warn_only=True, host_string=self.client_ip, user=self.username, password=self.userpassw):
            try:
                time_before = int(run(date_cmd))
                my_result   = run(curl_cmd1 + curl_cmd2 + curl_cmd3)
                time_after  = int(run(date_cmd))
                http_flow = my_result.split("\t")
                ''' flow time is average of 'time_before' and 'time_after' '''
                my_flow_time = (time_before + time_after)/2
                print http_flow
                ''' updating http data flow data  '''
                self.flow['flow_time'] = my_flow_time
                self.flow['src_ip']    = http_flow[0]
                self.flow['src_port']  = http_flow[1]
                self.flow['dst_ip']    = http_flow[2]
                self.flow['dst_port']  = http_flow[3]
                self.flow['rsp_code']  = http_flow[4]
                self.flow['conn_time'] = http_flow[5]
            except:
                print "HTTP request fail with: {0}".format(my_result)
                return
