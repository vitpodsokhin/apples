#!/usr/bin/env python3
import subprocess, json
from connection import TCP_Connection, UDP_Connection, subprocess_run_args

families = ('inet', 'inet6')
protos = ('tcp', 'udp')

def run_netstat(
        family:families=None,
        proto:protos=None
    ) -> list[str]:

    family_selector = '-f '+family if family is not None else ''
    proto_selector = '-p '+proto if proto is not None else ''

    netstat_command = f"netstat -nval {family_selector} {proto_selector}"
    netstat_out = subprocess.run(netstat_command, **subprocess_run_args).stdout
    netstat_lines = netstat_out.splitlines()

    return netstat_lines

def parse_netstat_connection(
        netstat_connection_line:str
    ) -> TCP_Connection|UDP_Connection:

    connection_classes = {'tcp': TCP_Connection, 'udp': UDP_Connection}
    proto = netstat_connection_line.split()[0]

    for protocol_name in protos:
        if proto.startswith(protocol_name):
            proto = protocol_name
    Parse_Connection = connection_classes[proto]
    connection = Parse_Connection(*netstat_connection_line.split())

    return connection

def parse_netstat_connections(
        family:families=None,
        proto:protos=None,
        netstat_lines:str=None
    ) -> list[TCP_Connection|UDP_Connection]:

    if netstat_lines == None:
        netstat_lines = run_netstat(family, proto)

    connections = []
    for line in netstat_lines:
        if line.startswith(protos):
            connection = parse_netstat_connection(line)
            connections.append(connection)

    return connections

def main():
    connections = parse_netstat_connections()
    connections_list = []
    for connection in connections:
        connection_dict = connection.to_dict()
        connections_list.append(connection_dict)
    
    print(json.dumps(connections_list))

if __name__ == '__main__':
    main()
