from dataclasses import dataclass
from subprocess import run

from Common import subprocess_run_args
from Netstat import Netstat

@dataclass
class Process:
    pid: int
    command_line: str = ''

    def __post_init__(self):
        result = run(f"ps -p {self.pid} -o command", **subprocess_run_args)
        try:
            self.command_line = result.stdout.splitlines()[1]
        except IndexError:
            self.command_line = ''

    @property
    def as_dict(self):
        return self.__dict__

    @staticmethod
    def get_connections_of_a_process(process, connections=None) -> dict:
        if connections is None:
            connections = Netstat.get_connections()
        connections_of_process = [connection for connection in connections if connection.pid == process.pid]
        dict_of_process_with_connections = {
            'process': process.as_dict,
            'connections_count': len(connections_of_process),
            'connections': [connection.to_dict() for connection in connections_of_process]
        }

        return dict_of_process_with_connections

    def get_connections_of_process(self) -> dict:
        dict_of_process_with_connections = Process.get_connections_of_a_process(self)
        return dict_of_process_with_connections
