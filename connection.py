import subprocess
import json
from dataclasses import dataclass

subprocess_run_args_str = "shell=True, capture_output=True, text=True, encoding='utf8'"
subprocess_run_args = {}
for arg in subprocess_run_args_str.split(', '):
    key, value = arg.split('=')
    subprocess_run_args[key] = eval(value)
del subprocess_run_args_str

@dataclass
class BaseConnection:
    proto: str
    recvQ: int
    sendQ: int
    localSocket: str
    remoteSocket: str

    def process_socket(self, socket_attr, socket_str, socket_type):
        address = '.'.join(socket_str.split('.')[:-1])
        port = socket_str.split('.')[-1]
        if socket_str != '*.*':
            setattr(self, socket_attr, f"{address}:{port}")
            setattr(self, f"{socket_type}Addr", address)
            setattr(self, f"{socket_type}Port", port)
        else:
            setattr(self, socket_attr, '*:*')

    def convert_to_int(self, *attributes):
        for attribute in attributes:
            setattr(self, attribute, int(getattr(self, attribute)))

    def __post_init__(self):
        self.convert_to_int('recvQ', 'sendQ', 'pid', 'epid', 'rhiwat', 'shiwat')
        self.family = 4 if self.proto.endswith('4') else 6
        self.process_socket("localSocket", self.localSocket, "local")
        self.process_socket("remoteSocket", self.remoteSocket, "remote")

    def as_dict(self) -> dict:
        connection_dict = self.__dict__
        return connection_dict

    def to_dict(self) -> dict:
        connection_dict = {
            'pid': self.pid,
            'family': self.family,
            'proto': self.proto,
            'localSocket': self.localSocket,
            'remoteSocket': self.remoteSocket
        }
        return connection_dict

@dataclass
class TCP_State():
    state: str

@dataclass
class Common_Connection_metrics():
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
    family: int = None

@dataclass
class TCP_Connection(Common_Connection_metrics, TCP_State, BaseConnection):
    ...

@dataclass
class UDP_Connection(Common_Connection_metrics, BaseConnection):
    ...

@dataclass
class Process:
    pid: int
    command_line: str = ''

    def __post_init__(self):
        result = subprocess.run(f"ps -p {self.pid} -o command", **subprocess_run_args)
        try:
            self.command_line = result.stdout.splitlines()[1]
        except IndexError:
            self.command_line = ''
