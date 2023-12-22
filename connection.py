import subprocess
import json
from dataclasses import dataclass

subprocess_run_args_str = "shell=True, capture_output=True, encoding='utf8', text=True"
subprocess_run_args = {}
for arg in subprocess_run_args_str.split(', '):
    key, value = arg.split('=')
    subprocess_run_args[key] = eval(value)

@dataclass
class BaseConnection:
    proto: str
    recvQ: int
    sendQ: int
    localSocket: str
    remoteSocket: str

    def __post_init__(self):
        if self.localSocket != '*.*':
            self.localAddr = '.'.join(self.localSocket.split('.')[:-1])
            self.localPort = self.localSocket.split('.')[-1]
        if self.remoteSocket != '*.*':
            self.remoteAddr = '.'.join(self.remoteSocket.split('.')[:-1])
            self.remotePort = self.remoteSocket.split('.')[-1]
        result = subprocess.run(f"ps -p {self.pid} -o command", **subprocess_run_args)
        self.command_line = result.stdout.splitlines()[1]

    def to_json(self):
        connection = {
            'pid': self.pid,
            'proto': self.proto,
            'command_line': self.command_line,
            'localSocket': self.localSocket,
            'remoteSocket': self.remoteSocket
        }
        connection_json = json.dumps(connection)
        return connection_json

@dataclass
class TCP_Connection(BaseConnection):
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

@dataclass
class UDP_Connection(BaseConnection):
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
