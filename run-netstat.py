#!/usr/bin/env python3
import subprocess
from dataclasses import dataclass

protos = ('tcp', 'udp')
subprocess_run_args_str = "shell=True, capture_output=True, encoding='utf8', text=True"

subprocess_run_args = {}
for arg in subprocess_run_args_str.split(', '):
    key, value = arg.split('=')
    subprocess_run_args[key] = eval(value)

@dataclass
class TCP_Connection:
    proto: str
    recvQ: int
    sendQ: int
    localSocket: str
    foreignSocket: str
    state: str
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
class UDP_Connection:
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

def run_netstat(proto=None):
    proto = 'tcp'
    netstat_command = f"netstat -nval -p {proto}"

    netstat_out = subprocess.run(netstat_command, **subprocess_run_args).stdout
    netstat_lines = netstat_out.splitlines()
    return netstat_lines

def parse_netstat_connection(netstat_connection_line):
    if netstat_connection_line.startswith('tcp'):
        connection = TCP_Connection(*netstat_connection_line.split())
    return connection

from pprint import pprint
def main():
    for line in run_netstat():
        if line.startswith('tcp'):
            pprint(parse_netstat_connection(line))

if __name__ == '__main__':
    main()