## Running the blockchain network
### Requirements
<li> Python 3.10
<li> pip

<br>

### Folder contents
The root folder consists of:
- `blockchain`, `network` and `utils` directories
- Two python files, `main.py` and `demo.py`.
- `requirements.txt`

Running `main.py` gives a command line interface to execute your own commands
in the network.
<br>
`demo.py` contains a sample test case containing three nodes and covering all possible operations that can be performed in the network.

<br>

### Steps to run program
1. From the root directory, run `pip install -r requirements.txt`
2. To execute `demo.py`, run `python demo.py`
3. To use the command line interface, execute `main.py` with the command `python main.py <file_name>` <br> where `<file_name>` is optional and contains the state of the blockchain network. `blockchain.net` contains the sample state of the network from `demo.py`.
4. After starting the `main.py` program, type `help` and hit enter to get a list of commands that can be performed in the network.

