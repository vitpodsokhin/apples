from dataclasses import dataclass
import subprocess

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
    foreignSocket: str

    def __post_init__(self):
        result = subprocess.run(f"ps -p {self.pid} -o command", **subprocess_run_args)
        self.command_line = result.stdout.splitlines()[1]

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
