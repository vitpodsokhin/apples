# Netstat Connection Analyzer

This Python project provides a comprehensive solution for analyzing network connections using the `netstat` command. The project is structured into multiple modules for enhanced readability and modularity.

## Project Structure

### Common.py

The `Common.py` module centralizes common configurations for subprocess execution.

```python
subprocess_run_args_str = "shell=True, capture_output=True, text=True, encoding='utf8'"
subprocess_run_args = {}
for arg in subprocess_run_args_str.split(', '):
    key, value = arg.split('=')
    subprocess_run_args[key] = eval(value)
del subprocess_run_args_str
```

### Process.py

The `Process.py` module defines a `Process` data class for representing system processes.

```python
from dataclasses import dataclass
from subprocess import run
from Common import subprocess_run_args

@dataclass
class Process:
    pid: int
    command_line: str = ''

    # ... (omitted for brevity)
```

### Connection.py

The `Connection.py` module contains data classes related to network connections, offering a structured representation.

```python
from dataclasses import dataclass

@dataclass
class BaseConnection:
    # ... (omitted for brevity)

@dataclass
class TCP_State():
    # ... (omitted for brevity)

@dataclass
class Common_Connection_metrics():
    # ... (omitted for brevity)

@dataclass
class TCP_Connection(Common_Connection_metrics, TCP_State, BaseConnection):
    # ... (omitted for brevity)

@dataclass
class UDP_Connection(Common_Connection_metrics, BaseConnection):
    # ... (omitted for brevity)
```

### Netstat.py

The `Netstat.py` module encapsulates the logic for running the `netstat` command and parsing its output.

```python
from subprocess import run
from Common import subprocess_run_args
from Connection import TCP_Connection, UDP_Connection

protos = ('tcp', 'udp')
families = ('inet', 'inet6')

class Netstat:
    # ... (omitted for brevity)
```

### test.py

The `test.py` script demonstrates the usage of the project by fetching network connections for each process.

```python
#!/usr/bin/env python3
from Netstat import Netstat
from Process import Process

# ... (omitted for brevity)
```

## How to Use

### Requirements

- Python >= 3.7

### Instructions

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/vitpodsokhin/apples.git
   ```

2. Navigate to the project directory:

   ```bash
   cd apples
   ```

3. Run the test script:

   ```bash
   ./test.py
   ```

   This script fetches and prints network connections for each process.

### Customization

- Modify the project modules to suit your specific requirements.
- Explore the individual modules to understand the data classes and functionalities they provide.

## Contributing

If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request. Your contributions are welcome!

## License

This project is licensed under the [GNU GPL License](LICENSE). Feel free to use, modify, and distribute the code for your purposes.

## Acknowledgments

- Special thanks to the Python community and contributors.
