from subprocess import run
from Common import subprocess_run_args
from Connection import TCP_Connection, UDP_Connection

families = ('inet', 'inet6')
protos = ('tcp', 'udp')

class Netstat:

    @staticmethod
    def run_netstat(
            proto: protos = None,
            family: families = None
        ) -> list[str]:
        proto_selector = '-p ' + proto if proto is not None else ''
        family_selector = '-f ' + family if family is not None else ''

        netstat_command = f"netstat -nval {family_selector} {proto_selector}"
        netstat_out = run(netstat_command, **subprocess_run_args).stdout
        netstat_lines = netstat_out.splitlines()

        return netstat_lines

    @staticmethod
    def parse_netstat_connection(
            netstat_connection_line: str
        ) -> TCP_Connection | UDP_Connection:
        connection_classes = {'tcp': TCP_Connection, 'udp': UDP_Connection}
        proto = netstat_connection_line.split()[0]

        for protocol_name in protos:
            if proto.startswith(protocol_name):
                proto = protocol_name
        Parse_Connection = connection_classes[proto]
        connection = Parse_Connection(*netstat_connection_line.split())

        return connection

    @staticmethod
    def parse_netstat_connections(
            proto: protos = None,
            family: families = None,
            netstat_lines: str = None
        ) -> list[TCP_Connection | UDP_Connection]:
        if netstat_lines is None:
            netstat_lines = Netstat.run_netstat(family, proto)

        connections = []
        for line in netstat_lines:
            if line.startswith(protos):
                connection = Netstat.parse_netstat_connection(line)
                connections.append(connection)

        return connections
