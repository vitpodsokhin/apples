import subprocess
import json
from dataclasses import dataclass
from sys import stdout

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

        #TODO change the asterisks in the addresses to 0.0.0.0 or :: 
            # depending on the network protocol family
        # elif address == '*': # and port != '*':
        #     setattr(self, socket_attr, f"0.0.0.0:{port}")
        #     setattr(self, f"{socket_type}Addr", '0.0.0.0')
        #     setattr(self, f"{socket_type}Port", port)

    def __post_init__(self):

        self.pid = int(self.pid)
        self.family = 4 if self.proto.endswith('4') else 6
        self.process_socket("localSocket", self.localSocket, "local")
        self.process_socket("remoteSocket", self.remoteSocket, "remote")
        result = subprocess.run(f"ps -p {self.pid} -o command", **subprocess_run_args)
        try:
            self.command_line = result.stdout.splitlines()[1]
        except IndexError:
            self.command_line = ''

    def as_dict(self) -> dict:
        connection_dict = self.__dict__
        return connection_dict

    def to_dict(self) -> json:
        connection_dict = {
            'pid': self.pid,
            'command_line': self.command_line,
            'family': self.family,
            'proto': self.proto,
            'localSocket': self.localSocket,
            'remoteSocket': self.remoteSocket
        }
        return connection_dict

@dataclass
class TCP_Connection(BaseConnection):
    '''... inherits class BaseConnection'''
    state: str
    #TODO following are common for both -- there must be a way to ...
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
    command_line: str = ''

@dataclass
class UDP_Connection(BaseConnection):
    '''... inherits class BaseConnection'''
    #TODO ... to reduce the code repetition.
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
    family: str = None
    command_line: str = ''

@dataclass
class Process:
    pid: int
    command_line: str
