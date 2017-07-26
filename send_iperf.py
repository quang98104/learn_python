#!/usr/bin/env python

from traffic_class import traffic
import time

myclient     = "10.24.9.18"
myserver     = "www.yahoo.com"
myuser       = "root"
mypassw      = "testpass1"
code_http_ok = ['200', '204', '206', '301', '302', '305', '307', '308']

''' instantiate traffic class with just a basic set of parameters; additional parameter can be pass dynamically '''
curl_o = traffic(client_ip=myclient, server_ip=myserver, username=myuser, userpassw=mypassw)

curl_o.server_ip="10.24.17.235"
curl_o.username="ubuntu"

''' IPERF TCP '''
curl_o.traffic_iperf_server_start()
curl_o.username="root"
curl_o.traffic_iperf_client()
print '\n\n\nThis is the iperf tcp flow {}'.format(curl_o.iperf_flow)
print '\nTraffic from {0}:{1} to {2}:{3} PASS\n\n\n'.format(curl_o.iperf_flow[0], curl_o.iperf_flow[1], curl_o.iperf_flow[2], curl_o.iperf_flow[3])
curl_o.username="ubuntu"
curl_o.traffic_iperf_server_stop()

''' IPERF UDP '''
curl_o.traffic_iperf_server_start(proto="udp")
curl_o.username="root"
curl_o.traffic_iperf_client(proto="udp")
print '\n\n\nThis is the iperf flow {}'.format(curl_o.iperf_flow)
print '\nTraffic from {0}:{1} to {2}:{3} PASS\n\n\n'.format(curl_o.iperf_flow[0], curl_o.iperf_flow[1], curl_o.iperf_flow[2], curl_o.iperf_flow[3])
curl_o.username="ubuntu"
curl_o.traffic_iperf_server_stop()
