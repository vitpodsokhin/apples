#!/usr/bin/env python3

import subprocess
from dataclasses import dataclass

def create_connection(proto, *args):
    connection = BaseConnection(proto, *args)
    setattr(connection, 'rhiwat', None)
    setattr(connection, 'shiwat', None)
    setattr(connection, 'pid', None)
    setattr(connection, 'epid', None)
    setattr(connection, 'state_str', None)
    setattr(connection, 'options', None)
    setattr(connection, 'gencnt', None)
    setattr(connection, 'flags', None)
    setattr(connection, 'flags1', None)
    setattr(connection, 'usscnt', None)
    setattr(connection, 'rtncnt', None)
    setattr(connection, 'fltrs', None)
    setattr(connection, 'command_line', None)
    return connection

@dataclass
class BaseConnection:
    proto: str
    recvQ: int
    sendQ: int
    localSocket: str
    foreignSocket: str
    rhiwat: int
    shiwat: int
    pid: int
    epid: int
    state_str: str
    options: str
    gencnt: str
    flags: str
    flags1: str
    usscnt: int
    rtncnt: int
    fltrs: int
    command_line: str = None

    def __post_init__(self):
        result = subprocess.run(f"ps -p {self.pid} -o command", **subprocess_run_args)
        self.command_line = result.stdout.splitlines()[1]

@dataclass
class TCP_Connection(BaseConnection):
    state: str

@dataclass
class UDP_Connection(BaseConnection):
    pass

def run_netstat(proto=None):
    netstat_command = f"netstat -nval -p {proto}"
    netstat_out = subprocess.run(netstat_command, **subprocess_run_args).stdout
    netstat_lines = netstat_out.splitlines()
    return netstat_lines

def parse_netstat_connection(netstat_connection_line):
    if netstat_connection_line.startswith('tcp'):
        connection = create_connection('tcp', *netstat_connection_line.split())
        return TCP_Connection(*connection.__dict__.values())
    elif netstat_connection_line.startswith('udp'):
        connection = create_connection('udp', *netstat_connection_line.split())
        return UDP_Connection(*connection.__dict__.values())
    return None

from pprint import pprint
def main():
    for proto in protos:
        for line in run_netstat(proto):
            if line.startswith(proto):
                pprint(parse_netstat_connection(line))

if __name__ == '__main__':
    main()
