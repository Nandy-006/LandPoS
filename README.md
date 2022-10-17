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
This folder holds the code implementation for the representation of the blockchain network. 

### `network.py`

The `Network` class represents a blockchain network. It manages all communications between nodes.
<br>

| Function                 | Definition                                                                                                                                                                                                                                                          |
|--------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `connectNode()`          | Connects a new node to the network                                                                                                                                                                                                                                  |
| `start()`                | Starts the blockchain network which listens to the user inputs                                                                                                                                                                                                      |
| `run()`                  | Run a specified command on the network                                                                                                                                                                                                                              |
| `nodeExists()`           | A helper function to check if a given node (or for atleast one node) exists on the network                                                                                                                                                                          |
| `handle()`               | Handle user commands                                                                                                                                                                                                                                                |
| `printCommands()`        | Displays all the available commands                                                                                                                                                                                                                                 |
| `broadcastTransaction()` | Broadcasts the new transaction to all nodes                                                                                                                                                                                                                         |
| `broadcastBlock()`       | Broadcasts the new minted block to all nodes                                                                                                                                                                                                                        |
| `getValidator()`         | **This contains the implementation for the PoS consensus**. The probability of a validator being selected is directly dependent on the stake the node holds in the blockchain. The validator mints the new block.This function will return the validator node's ID. |
| `mint()`                 | This function calls the validator on all the transactions in the transaction pool                                                                                                                                                                                   |
| `validate()`             | This function actually validates all the transactions passed to it and returns a boolean based on whether the transaction is valid                                                                                                                                  |
| `addBlock()`             | Once all the transactions are validated, this function will mint and return the new block. The  **broadcastBlock()**  function will then broadcast the block to all nodes.                                                                                          |

<br>

### `node.py`

This file contains the implementation of all the commands pertaining to operating a node as well as the **Proof of Stake consensus algorithm**
<br>

| Function           | Definition                                                                                                                                                                                                                                                          |
|--------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `registerCoins()`  | Inititates a transaction to set the node's initial balance                                                                                                                                                                                                          |
| `registerLand()`   | Initates a new transaction to register a new land under the node                                                                                                                                                                                                    |
| `buyLand()`        | Initiates a new transaction for buying a land                                                                                                                                                                                                                       |
| `sellLand()`       | Initiates a new transaction for selling a land                                                                                                                                                                                                                      |
| `stake()`          | Initiate a new transaction to increase the stake of a node                                                                                                                                                                                                          |
| `addTransaction()` | Adds a transaction to the transaction pool                                                                                                                                                                                                                          |
| `getValidator()`   | **This contains the implementation for the PoS consensus**. The probability of a validator being selected is directly dependent on the stake the node holds in the blockchain. The validator mints the new block.This function will return the validator node's ID. |
| `mint()`           | The validator chosen validates all transactions and mints a block                                                                                                                                                                                                   |
| `validate()`       | This function validates all the transactions passed to it and returns a boolean based on whether the transaction is valid                                                                                                                                           |
| `addBlock()`       | Adds a block to the transaction and empties the transaction pool                                                                                                                                                                                                    |

## Blockchain
This folder contains the blockchain implementation of the code

### `block.py`

This file contains implementation for the block of the blockchain
<br>

| Function        | Definition                                      |
|-----------------|-------------------------------------------------|
| `hashBlock()`   | Hashes a given block using the SHA256 algorithm |
| `genesis()`     | Generates the genesis block                     |
| `createBlock()` | Creates and returns a new block                 |
| `serialize()`   | Serializes the block                            |

### `blockchain.py`

The Blockchain class is used to represent a blockchain which is a series of cryptographically linked blocks.
The Blockchain is the single source of truth for all data in a distributed network.
<br>

| Function               | Definition                                         |
|------------------------|----------------------------------------------------|
| `addBlock()`           | Appends a block to the blockchain                  |
| `getLength()`          | Returns the length of the blockchain               |
| `getTransaction()`     | Returns transaction based on transaction ID        |
| `getLandHistory()`     | Gets history of the buyers and sellers of the land |
| `getLandOwner()`       | Returns the landowner of the land ID given         |
| `getLandOwners()`      | Returns a list of all the lands and their owners   |
| `getBlockFromHeight()` | Returns a block based on the block height          |
| `getLastBlock()`       | Returns the last block of the blockchain           |
| `getStakes()`          | Returns a list of the stakes of all nodes          |
| `getAges()`            | Get the coin ages of all nodes                     |
| `getBalance()`         | Get wallet balance of a node                       |
| `getAllBalances()`     | Get wallet balances of all nodes                   |

### `transaction.py`
The Transaction class represents a transaction in the blockchain. A transaction is a transfer of value in a blockchain.
<br>

| Function                | Definition                                       |
|-------------------------|--------------------------------------------------|
| `newRCTransaction()`    | Create a new Receive Coins transaction           |
| `newLDTransaction()`    | Create a new Land Declaration transaction        |
| `newLTTransaction()`    | Create a new Land Transfer transaction           |
| `newSTTransaction()`    | Create a new Stake Increase transaction          |
| `generateTransaction()` | Generates a transaction in the correct structure |
| `serialize()`           | Serializes the transaction object                |

### `merkle_tree.py`
A MerkleTree is a tree in which every leaf node is a hash of a data block and every inner node is the hash of its child nodes. This class provides a function called `getMerkleRoot()` to get the Merkle Root given a list of transactions
<br>