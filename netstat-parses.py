#!/usr/bin/env python3

import subprocess
from dataclasses import dataclass, asdict

@dataclass
class TCP_Connection:
    proto: str
    recvQ: int
    sendQ: int
    localAddress: str
    foreignAddress: str
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
    _command_line: str = None

    def __post_init__(self):
        result = subprocess.run(f"ps -p {self.pid} -o command", shell=True, capture_output=True, encoding='utf8', text=True)
        self._command_line = result.stdout.splitlines()[1]       

    @property
    def command_line(self) -> str:
        if self._command_line is None:
            self.set_command_line()
        return self._command_line

    def set_command_line(self):
        result = subprocess.run(f"ps -p {self.pid} -o command", shell=True, capture_output=True, encoding='utf8', text=True)
        self._command_line = result.stdout.splitlines()[1]


def run_netstat(proto: str = None) -> str:
    protos = ('tcp', 'udp')
    command = f"netstat -nlv {'-p' + proto if proto else ''}"
    tcp_connections = [TCP_Connection(*connection.split()) for connection
                       in subprocess.run(command, shell=True, capture_output=True, encoding='utf8', text=True).stdout.splitlines() if connection.startswith('tcp')]
    return tcp_connections

tcp_connections = run_netstat('tcp')

tcp_connections_json = [asdict(connection) for connection in tcp_connections]
print(tcp_connections_json)
