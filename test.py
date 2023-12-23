#!/usr/bin/env python3

import json
from Netstat import Netstat

connections = Netstat.parse_netstat_connections()

connection_dicts = [connection.to_dict() for connection in connections]

print(json.dumps(connection_dicts))