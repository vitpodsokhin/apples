from dataclasses import dataclass
import subprocess

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
        result = subprocess.run(f"ps -p {self.pid} -o command", shell=True, capture_output=True, encoding='utf8', text=True)
        try:
            self.command_line = result.stdout.splitlines()[1]
        except Exception as e:
            print(e)


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
        result = subprocess.run(f"ps -p {self.pid} -o command", shell=True, capture_output=True, encoding='utf8', text=True)
        self.command_line = result.stdout.splitlines()[1]
