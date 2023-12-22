#!/usr/bin/env python3
import subprocess
from dataclasses import asdict
from connection import TCP_Connection, UDP_Connection

subprocess_run_args_str = "shell=True, capture_output=True, encoding='utf8', text=True"
subprocess_run_args = {}
for arg in subprocess_run_args_str.split(', '):
    key, value = arg.split('=')
    subprocess_run_args[key] = eval(value)

protos = ('tcp', 'udp')

def run_netstat(proto=None) -> list[str]:
    netstat_command = f"netstat -nval {'-p '+proto if proto is not None else ''}"
    netstat_out = subprocess.run(netstat_command, **subprocess_run_args).stdout
    netstat_lines = netstat_out.splitlines()
    return netstat_lines

def parse_netstat_connection(netstat_connection_line) -> TCP_Connection|UDP_Connection:
    connection_classes = {'tcp': TCP_Connection, 'udp': UDP_Connection}
    proto = netstat_connection_line.split()[0]
    if proto.startswith('tcp'):
        proto = 'tcp'
    elif proto.startswith('udp'):
        proto = 'udp'
    Parse_Connection = connection_classes[proto]
    connection = Parse_Connection(*netstat_connection_line.split())
    return connection

def parse_netstat_connections(netstat_lines=None) -> list[TCP_Connection|UDP_Connection]:
    if netstat_lines == None:
        netstat_lines = run_netstat()
    connections = []
    for line in run_netstat():
        if line.startswith(protos):
            connection = parse_netstat_connection(line)
            connections.append(connection)
    return(connections)

from pprint import pprint
def main():
    connections = parse_netstat_connections()
    for connection in connections:
        connection_dict = asdict(connection)
        print(connection_dict)

if __name__ == '__main__':
    main()
