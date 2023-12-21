#!/usr/bin/env python3
import subprocess
from dataclasses import dataclass

subprocess_run_args_str = "shell=True, capture_output=True, encoding='utf8', text=True"
subprocess_run_args = {}
for arg in subprocess_run_args_str.split(', '):
    key, value = arg.split('=')
    subprocess_run_args[key] = eval(value)

protos = ('tcp', 'udp')

from connection import TCP_Connection, UDP_Connection

def run_netstat(proto=None):
    netstat_command = f"netstat -nval {'-p '+proto if proto is not None else ''}"
    netstat_out = subprocess.run(netstat_command, **subprocess_run_args).stdout
    netstat_lines = netstat_out.splitlines()
    return netstat_lines

def parse_netstat_connection(netstat_connection_line):
    connection_classes = {'tcp': TCP_Connection, 'udp': UDP_Connection}
    if netstat_connection_line.startswith('tcp'):
        connection = TCP_Connection(*netstat_connection_line.split())
    elif netstat_connection_line.startswith('udp'):
        connection = UDP_Connection(*netstat_connection_line.split())
    return connection

from pprint import pprint
def main():
    for proto in protos:
        for line in run_netstat(proto):
            if line.startswith(proto):
                pprint(parse_netstat_connection(line))

if __name__ == '__main__':
    main()
