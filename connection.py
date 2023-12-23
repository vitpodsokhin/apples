from dataclasses import dataclass

@dataclass
class BaseConnection:
    proto: str
    recvQ: int
    sendQ: int
    localSocket: str
    remoteSocket: str

    def process_socket(self, socket_attr, socket_str, socket_location):
        address = '.'.join(socket_str.split('.')[:-1])
        port = socket_str.split('.')[-1]
        if socket_str != '*.*':
            setattr(self, socket_attr, f"{address}:{port}")
            setattr(self, f"{socket_location}Addr", address)
            setattr(self, f"{socket_location}Port", int(port))
        else:
            setattr(self, socket_attr, '*:*')
            setattr(self, f"{socket_location}Addr", address)
            setattr(self, f"{socket_location}Port", 0)

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
class TCP_Connection(Common_Connection_metrics, TCP_State, BaseConnection): ...
@dataclass
class UDP_Connection(Common_Connection_metrics, BaseConnection): ...
