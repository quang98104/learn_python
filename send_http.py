#!/usr/bin/env python

from class_traffic_http import TrafficHttp
import time

myclient     = "10.24.17.235"
myserver     = "www.yahoo.com"
myuser       = "ubuntu"
mypassw      = "testpass1"
code_http_ok = ['200', '204', '206', '301', '302', '305', '307', '308']

''' instantiate traffic class with just a basic set of parameters; additional parameter can be pass dynamically '''
http_o = TrafficHttp(client_ip=myclient, url=myserver, username=myuser, userpassw=mypassw,)
http_o.create()
print '\n\n\nThis is http flow {}\n'.format(http_o.flow)
''' print 'Host \'{0}:{1}\' send http traffic to host \'{2}:{3}\' at {4}'.format(http_o.flow['src_ip'], http_o.flow['src_port'], http_o.flow['dst_ip'], http_o.flow['dst_port'], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(http_o.flow['flow_time']))) '''
if http_o.flow['rsp_code'] in code_http_ok:
    print 'Http traffic PASS with \'{0}\' response code'.format(http_o.flow['rsp_code'])
else:
    print 'Http traffic FAIL with \'{0}\' response code'.format(http_o.flow['rsp_code'])
