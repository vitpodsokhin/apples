# Netstat Connection Parser

This Python project provides a utility for parsing network connections using the `netstat` command. It defines classes to represent TCP and UDP connections, offering a structured way to analyze and process network information.

## Project Structure

The project consists of two main files:

1. **connection.py**: This file defines three classes - `BaseConnection`, `TCP_Connection`, and `UDP_Connection`. These classes encapsulate the attributes and methods related to network connections. The `BaseConnection` class serves as the base for TCP and UDP connections, containing common attributes and methods.

2. **run-netstat.py**: The main executable script interacts with the `netstat` command to retrieve network connection information. It utilizes the classes defined in `connection.py` to parse and represent the connections. The parsed data is then converted into a list of dictionaries and printed in JSON format.

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

3. Run the `run-netstat` script:

   ```bash
   ./run-netstat.py
   ```

   This will execute the `netstat` command, parse the connection information, get command lines of the corresponding processes
   #TODO: get cmd_line from pid only once; implement the [Process](connection.py#L103) class for this
   and print the results in JSON format.

### Customization

- You can customize the script to filter connections based on the network family (`inet` or `inet6`) and protocol (`tcp` or `udp`). Modify the `families` and `protos` variables in `main.py` accordingly.
- #TODO: filter by state, interface.

## Contributing

If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request. Your contributions are welcome!

## License

This project is licensed under the [GNU GPL License](LICENSE). Feel free to use, modify, and distribute the code for your purposes.

## Acknowledgments

- The project uses the `dataclasses` module for structured data representation.
- Special thanks to the Python community and contributors.
