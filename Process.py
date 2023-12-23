from dataclasses import dataclass
from subprocess import run

from Common import subprocess_run_args

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

    def get_connections(self):
        self.connections = []

    @property
    def as_dict(self):
        return self.__dict__
