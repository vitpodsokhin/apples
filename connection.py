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
            address = '.'.join(self.localSocket.split('.')[:-1])
            port = self.localSocket.split('.')[-1]
            self.localSocket = f"{address}:{port}"

            setattr(self, "localAddr", address)
            setattr(self, "localPort", port)

        if self.remoteSocket != '*.*':
            address = '.'.join(self.remoteSocket.split('.')[:-1])
            port = self.remoteSocket.split('.')[-1]
            self.remoteSocket = f"{address}:{port}"

            setattr(self, "remoteAddr", address)
            setattr(self, "remotePort", port)

        result = subprocess.run(f"ps -p {self.pid} -o command", **subprocess_run_args)
        self.command_line = result.stdout.splitlines()[1]

    def as_dict(self):
        connection_dict = self.__dict__
        return connection_dict

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
