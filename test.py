#!/usr/bin/env python3
from Netstat import Netstat
from Process import Process

def get_connections_of_process(process, connections=None) -> dict:
    if connections is None:
        connections = Netstat.parse_netstat_connections()
    process_connections = [connection for connection in connections if connection.pid == process.pid]
    return {
        str(process.pid): process.as_dict,
        'connections_count': len(process_connections),
        'connections': [connection.to_dict() for connection in process_connections]
    }

connections = Netstat.parse_netstat_connections()
pids = Netstat.get_connection_pids(connections)
processes = [Process(pid) for pid in pids]

from json import dumps
for process in processes:
    print(dumps(get_connections_of_process(process, connections)))
