#!/usr/bin/env python3
import subprocess

netstat_command = 'netstat -nval'
run_args_str = "shell=True, capture_output=True, encoding='utf8', text=True"

run_args = {}
for arg in run_args_str.split(', '):
    key, value = arg.split('=')
    run_args[key] = eval(value)

netstat_out = subprocess.run(netstat_command, **run_args).stdout
netstat_lines = netstat_out.splitlines()
for line in netstat_lines:
    print(line)