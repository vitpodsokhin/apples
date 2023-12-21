#!/usr/bin/env python3
from os import geteuid, uname

def check_root_permissions():
    return uname().sysname.lower() == 'darwin' and geteuid() != 0

if check_root_permissions():
    print('Under macOS, you need to run this version as root. Exiting.')
    exit()

import psutil, json

processes_list = [p.as_dict() for p in psutil.process_iter()]

print(json.dumps(processes_list))