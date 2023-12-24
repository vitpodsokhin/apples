#!/usr/bin/env python3
import json
from Netstat import Netstat
from Process import Process

connections = Netstat.parse_netstat_connections()
pids = Netstat.get_connection_pids(connections)

def get_connections_of_process(process, connections=None):
    if connections == None:
        connections = Netstat.parse_netstat_connections()
    process_connections = [connection for connection in connections if connection.pid == process.pid]
    return (process, process_connections)

processes = [Process(pid) for pid in pids]

from pprint import pprint
for process in processes:
    pprint(get_connections_of_process(process, connections))
# for process in processes:
#     pprint(get_connections_of_process(process, connections))


# print(json.dumps(processes))