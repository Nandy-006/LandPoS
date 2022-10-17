# LandPoS-2.0
The new land management system using Proof of Stake consensus based blockchain

# Group 14 
`2019A7PS0164H` - Nandan H R
<br>

`2019A7PS0033H` - T V Chandra Vamsi
<br>

`2019A7PS0158H`	- Vraj Ketan Gandhi
<br>

# Function Definitions:

## Network
Holds the code implementation for the representation of the blockchain network. 
<br>

### `network.py`

This file contains classes pertaining to the commands a node in the blockchain can execute.
The Comands class contains all the possible commands and the Network contains all the implementation of all the commands.


| Function                 | Definition                                                                                            |
|--------------------------|-------------------------------------------------------------------------------------------------------|
| `connectNode()`          | Connects a new node to the network                                                                    |
| `start()`                | Starts the blockchain network which listens to the user inputs                                        |
| `handle()`               | Takes in the command input by a user node and calls the relevant function for executing that command  |
| `printCommands()`        | Invokes the Help command which just displays all the available commands                               |
| `broadcastTransaction()` | broadcasts the new transaction to all nodes                                                           |
| `broadcastBlock()`       | broadcasts the new minted block to all nodes                                                          |
|                          |                                                                                                       |

<br>

### `node.py`

This file contains the implementation of all the commands pertaining to operating a node as well as the **Proof of Stake consensus algorithm**

| Function           | Definition                                                                                                                                                                                                                                                          |
|--------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `registerCoins()`  | Adds coins to the new node's wallet on registration                                                                                                                                                                                                                 |
| `start()`          | Adds coins to the new node's wallet on registration                                                                                                                                                                                                                 |
| `registerLand()`   | Declares ownership of a land by a node and returns a transaction of it                                                                                                                                                                                              |
| `buyLand()`        | Allows the node to buy a land and returns a transaction of it                                                                                                                                                                                                       |
| `sellLand()`       | Allows the node to sell a land and returns a transaction of it                                                                                                                                                                                                      |
| `stake()`          | Increases the stake of the user and returns a transaction of it                                                                                                                                                                                                     |
| `addTransaction()` | Appends the transaction passed to it into the pool. If the pool has crossed its threshold then a new validator is searched.                                                                                                                                         |
| `getValidator()`   | **This contains the implementation for the PoS consensus**. The probability of a validator being selected is directly dependent on the stake the node holds in the blockchain. The validator mints the new block.This function will return the validator node's ID. |
| `mint()`           | This function calls the validator on all the transactions in the transaction pool                                                                                                                                                                                   |
| `validate()`       | This function actually validates all the transactions passed to it and returns a boolean based on whether the transaction is valid                                                                                                                                  |
| `addBlock()`       | Once all the transactions are validated, this function will mint and return the new block. The  **broadcastBlock()**  function will then broadcast the block to all nodes.                                                                                          |

