#!/usr/bin/env python3
import subprocess

netstat_command = 'netstat -nval'
run_args = "shell=True, capture_output=True, encoding='utf8', text=True".split(', ')
print(subprocess.run(netstat_command, **run_args).stdout)