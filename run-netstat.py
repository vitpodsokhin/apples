#!/usr/bin/env python3
import subprocess

protos = ('tcp', 'udp')

def run_netstat(proto=None):
    proto = 'tcp'
    netstat_command = f"netstat -nval -p {proto}"
    run_args_str = "shell=True, capture_output=True, encoding='utf8', text=True"

    run_args = {}
    for arg in run_args_str.split(', '):
        key, value = arg.split('=')
        run_args[key] = eval(value)

    netstat_out = subprocess.run(netstat_command, **run_args).stdout
    netstat_lines = netstat_out.splitlines()
    return netstat_lines

for line in run_netstat():
    if line.startswith('tcp'):
        print(line)