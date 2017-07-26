#!/usr/bin/env python

from class_elem_housekeeping import *
from class_elem_check_log import ElemCheckLog
from class_traffic_http import TrafficHttp
from class_elem_flow_log import *
from class_elem_fc_rule import ElemFcRule
from class_elem_get_info import *
from class_vyos_config import VyosConfig

import time

myvyos       = "10.24.17.218"
cmd1         = "interfaces ethernet eth2 description"
cmd2         = "show interfaces"
cmd3         = 'interfaces ethernet eth2 description "test 666"'
vyos_o = VyosConfig(vyos_ip=myvyos, conf_cmd=cmd3, show_cmd=cmd2, del_cmd=cmd1)
print vyos_o.create()
print vyos_o.read()
print  vyos_o.delete()
print vyos_o.read()
