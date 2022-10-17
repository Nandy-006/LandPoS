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

- connectNode(self, id: str, balance: int) : Node joins the network
- start(self) : Starts the blockchain network. It will remain in an infinite loop, taking the user's commands and executing them via the handle function until the exit command is invoked. 
- def handle(self, command: list[str]) : Takes in the command input by a user node and calls the relevant function for executing that command. For example, inputting the "SELL" command causes the node to begin the process for selling a land. It contains a switch case for the list of commands in the Commands class.
- printCommands(self) : Invokes the Help command which just displays all the available commands.
- broadcastTransaction(self, transaction: Transaction) : broadcasts the new transaction to all nodes
- def broadcastBlock(self, block: Block | None) : broadcasts the new minted block to all nodes
<!-- - processConnect(self, message: str) : Connects the node to the blockchain.
- processBuy(self, message: str) : Initiates a new transaction for buying a land. If an incorrect land ID is provided then an error message is shown. It takes the land ID as input.
- processSell(self, message: str) : Initiates a new transaction for selling a land. Makes sure that the land is owned by you and the buyer is within the network else throws an error. It takes land ID and the buyer node's ID as input.
- processStake(self, message: str) : Increases the stake of the node. If the wallet limit is exceeded then an error message is thrown. It takes the stake amount as input.
- processBlock(self, message: str) : Retrieves and displays a block from the blockchain. Takes height of the block as input.
- processLand(self, message: str) :  Retrieves the transaction history of the land ID that is passed as input.
- processTransaction(self, message: str) : Retrieves a transaction for validation purposes based. The transaction ID is passed as input.
- processBalance(self) : Retrieves wallet balance of the node. -->

NOTE: All these functions do not return anything.
<br>

### `node.py`

This file contains the implementation of all the commands pertaining to operating a node.

- getValidator(self) : This contains the implementation for the PoS consensus. The node with the maximum coin age value is chosen as the validator, and the validator mints the new block. The age of the node's coins is the depth of the block they mined previously. The coinage of the node is the product of the age and the number of coins they staked. This function will return the validator node's ID.

- mintBlock(self) : Once the transactions are validated by the chosen validator, the validator adds the block to the chain by minting a new block and the transaction pool is updated. 