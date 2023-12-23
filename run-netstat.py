#!/usr/bin/env python3
import subprocess, json
from connection import TCP_Connection, UDP_Connection, subprocess_run_args

families = ('inet', 'inet6')
protos = ('tcp', 'udp')

def run_netstat(
        family: families = None,
        proto: protos = None
    ) -> list[str]:
    """
    Executes the 'netstat' command to retrieve network connection information.

    Parameters:
    - family: Optional[str] - The network family to filter (options: 'inet', 'inet6').
    - proto: Optional[str] - The protocol to filter (options: 'tcp', 'udp').

    Returns:
    - list[str]: A list of strings containing the output lines of the 'netstat' command.
    """
    family_selector = '-f ' + family if family is not None else ''
    proto_selector = '-p ' + proto if proto is not None else ''

    netstat_command = f"netstat -nval {family_selector} {proto_selector}"
    netstat_out = subprocess.run(netstat_command, **subprocess_run_args).stdout
    netstat_lines = netstat_out.splitlines()

    return netstat_lines

def parse_netstat_connection(
        netstat_connection_line: str
    ) -> TCP_Connection | UDP_Connection:
    """
    Parses a single line of 'netstat' output to create a TCP or UDP connection object.

    Parameters:
    - netstat_connection_line: str - A line of 'netstat' output representing a network connection.

    Returns:
    - TCP_Connection or UDP_Connection: An instance of the appropriate connection class.
    """
    connection_classes = {'tcp': TCP_Connection, 'udp': UDP_Connection}
    proto = netstat_connection_line.split()[0]

    for protocol_name in protos:
        if proto.startswith(protocol_name):
            proto = protocol_name
    Parse_Connection = connection_classes[proto]
    connection = Parse_Connection(*netstat_connection_line.split())

    return connection

def parse_netstat_connections(
        proto: protos = None,
        family: families = None,
        netstat_lines: str = None
    ) -> list[TCP_Connection | UDP_Connection]:
    """
    Parses 'netstat' output lines to create a list of TCP or UDP connection objects.

    Parameters:
    - proto: Optional[str] - The protocol to filter (options: 'tcp', 'udp').
    - family: Optional[str] - The network family to filter (options: 'inet', 'inet6').
    - netstat_lines: Optional[list[str]] - List of 'netstat' output lines.

    Returns:
    - list[TCP_Connection or UDP_Connection]: A list of connection objects.
    """
    if netstat_lines is None:
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
        # connection_dict = connection.to_dict()
        connection_dict = connection.as_dict()
        connections_list.append(connection_dict)

    print(json.dumps(connections_list))

if __name__ == '__main__':
    main()
