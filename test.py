#!/usr/bin/env python3
from Netstat import Netstat
from Process import Process

def get_connections_of_process(process, connections=None) -> dict:
    if connections is None:
        connections = Netstat.get_connections()
    connections_of_process = [connection for connection in connections if connection.pid == process.pid]
    return {
        str(process.pid): process.as_dict,
        'connections_count': len(connections_of_process),
        'connections': [connection.to_dict() for connection in connections_of_process]
    }

connections = Netstat.get_connections()
pids = Netstat.get_connection_pids(connections)
processes = [Process(pid) for pid in pids]

from json import dumps
for process in processes:
    print(dumps(get_connections_of_process(process, connections)))
