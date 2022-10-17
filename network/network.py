import pickle
from copy import deepcopy
from termcolor import colored
from tabulate import tabulate

from blockchain.block import Block
from blockchain.blockchain import Blockchain
from blockchain.constants import BLOCK_TRANSACTION_THRESHOLD
from blockchain.transaction import Transaction
from utils.utils import Log, Command
from network.node import Node

class Commands:

    # Node specific
    REGISTER = Command("register", "<node_id> register <land_id>", "Register new land under node")
    BUY = Command("buy", "<node_id> buy <land_id> <seller_id>", "Buy specified land")
    SELL = Command("sell", "<node_id> sell <land_id> <receiver_id>", "Sell specified land")
    STAKE = Command("stake", "<node_id> stake <amount>", "Stake specified amount")
    BALANCE = Command("balance", "<node_id> balance", "Get node's current balance")

    # Node independent
    TRANSACTION = Command("transaction", "transaction <transaction_id>", "Get details of a transaction on the blockchain")
    BLOCK = Command("block", "block <n>", "Get nth block in the blockchain (-1 for last block)")
    HISTORY = Command("history", "history <land_id>", "Get history of land owners")
    BLOCKCHAIN = Command("blockchain", "blockchain", "Get the blockchain")
    LANDS = Command("lands", "lands", "Get all registered lands and their owners")
    POOL = Command("pool", "pool", "Get the current transaction pool")
    STAKES = Command("stakes", "stakes", "Get stakes of all nodes in the network")
    NODES = Command("nodes", "nodes", "Get all registered nodes")

    # Network
    CONNECT = Command("connect", "connect <node_id> <balance>", "Connect new node to the network")
    SAVE = Command("save", "save [<filename>]", "Save the network into a file")
    HELP = Command("help", "help", "List all commands")
    STOP = Command("stop", "stop", "Stop the network")

class Network:

    DEFAULT_NETWORK_FILE = "blockchain.net"

    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
    
    def connectNode(self, id: str, balance: int) -> None:
        Log.info(f"Node {id} is trying to join the network", "NEW NODE")
        if id in self.nodes:
            Log.error("Node already exists")
            return None

        if len(self.nodes) == 0:
            newNode = Node(id, Blockchain(), [])
        else:
            existingNode = list(self.nodes.values())[0]
            newNode = Node(id, deepcopy(existingNode.blockchain), deepcopy(existingNode.transactionPool))
        self.nodes[id] = newNode
        transaction = newNode.registerCoins(balance)
        self.broadcastTransaction(transaction)
        Log.info(f"Node {id} has joined the network", "NEW NODE")
    
    def start(self) -> None:
        Log.info("Starting the network")
        while True:
            command = input("\n> ").split(" ")
            if command[0] == Commands.STOP.key:
                Log.info("Stopping the network...")
                break
            else:
                self.handle(command)
                print()
        Log.info("Stopped the network")

    def run(self, command: str) -> None:
        print()
        Log.info(command, "RUN")
        self.handle(command.split(" "))
    
    def nodeExists(self, nodeId: str | None = None) -> bool:
        if nodeId is None:
            if len(self.nodes) <= 0:
                Log.error(f"At least one node needs to be connected to the network")
                return False
            return True
        
        if nodeId not in self.nodes:
            Log.error(f"Node ID {nodeId} is invalid")
            return False
        return True

    def handle(self, command: list[str]) -> None:
        match command:
            case [nodeId, "register", landId]:
                if self.nodeExists(nodeId):
                    transaction = self.nodes[nodeId].registerLand(landId)
                    self.broadcastTransaction(transaction)
            case [nodeId, "buy", landId, sellerId]:
                if self.nodeExists(nodeId) and self.nodeExists(sellerId):
                    transaction = self.nodes[nodeId].buyLand(landId, sellerId)
                    self.broadcastTransaction(transaction)
            case [nodeId, "sell", landId, receiverId]:
                if self.nodeExists(nodeId) and self.nodeExists(receiverId):
                    transaction = self.nodes[nodeId].sellLand(receiverId, landId)
                    self.broadcastTransaction(transaction)
            case [nodeId, "stake", amount]:
                try:
                    amount = int(amount)
                except:
                    Log.error("Invalid amount provided")
                    return
                if self.nodeExists(nodeId):
                    transaction = self.nodes[nodeId].stake(amount)
                    self.broadcastTransaction(transaction)
            case [nodeId, "balance"]:
                if self.nodeExists(nodeId):
                    Log.info(f"{self.nodes[nodeId].blockchain.getBalance(nodeId)}", f"{colored('BALANCE', attrs=['bold'])}", nodeId)
            case ["transaction", trId]:
                if self.nodeExists():
                    node = list(self.nodes.values())[0]
                    transaction = node.blockchain.getTransaction(trId)
                    if transaction is not None:
                        print(repr(transaction))
            case ["block", height]:
                if self.nodeExists():
                    node = list(self.nodes.values())[0]
                    try:
                        height = int(height)
                    except:
                        Log.error("Block height (n) needs to be an integer")
                        return
                    if height == -1:
                        block = node.blockchain.getLastBlock()
                    else:
                        block = node.blockchain.getBlockFromHeight(height)
                    if block is not None:
                        print(block)
            case ["history", landId]:
                if self.nodeExists():
                    node = list(self.nodes.values())[0]
                    history = node.blockchain.getLandHistory(landId)
                    if len(history) == 0:
                        Log.error("Unknown Land ID")
                        return None
                    Log.info(f"Transactions associated with land {landId}", "LAND HISTORY")
                    for transaction in history:
                        print(repr(transaction))
            case ["blockchain"]:
                if self.nodeExists():
                    node = list(self.nodes.values())[0]
                    print(node.blockchain)
            case ["lands"]:
                if self.nodeExists():
                    node = list(self.nodes.values())[0]
                    landOwners = node.blockchain.getLandOwners()
                    if len(landOwners) == 0:
                        Log.info("There are no lands registered in the network yet")
                    else:
                        Log.info(f"List of available lands and their owners", "LANDS")
                        print(tabulate(
                            [[land, owner] for land, owner in landOwners.items()],
                            headers=[colored("Land", attrs=["bold"]), colored("Owner", attrs=["bold"])],
                            tablefmt="simple"
                        ))
            case ["pool"]:
                if self.nodeExists():
                    node = list(self.nodes.values())[0]
                    pool = node.transactionPool
                    if len(pool) == 0:
                        Log.info("The transaction pool is empty", "TRANSACTION POOL")
                    else:
                        Log.info("Currently the transaction pool contains the following transactions", "TRANSACTION POOL")
                        for transaction in pool:
                            print(repr(transaction))
            case ["stakes"]:
                if self.nodeExists():
                    node = list(self.nodes.values())[0]

                    stakes = node.blockchain.getStakes(self.nodes)
                    ages = node.blockchain.getAges(self.nodes)
                    
                    data = [[nodeId, stakes[nodeId], ages[nodeId], stakes[nodeId] * ages[nodeId]] for nodeId in stakes]
                    Log.info("Current stakes in the blockchain", "STAKES")
                    if len(data) == 0:
                        Log.info("No one has staked in the network yet")
                    else:
                        print(tabulate(
                            data, headers=[
                                colored("Node", attrs=["bold"]),
                                colored("Stake", attrs=["bold"]),
                                colored("Age", attrs=["bold"]),
                                colored("Coinage", attrs=["bold"])
                            ] , tablefmt="simple"))
            case ["nodes"]:
                if len(self.nodes) <= 0:
                    Log.info("No node is registered to the network")
                else:
                    for nodeId in self.nodes.keys():
                        print(f"- {nodeId}")
            case ["connect", nodeId, balance]:
                try:
                    balance = int(balance)
                    if balance <= 0:
                        Log.error("Balance needs to be positive")
                        return
                    self.connectNode(nodeId, balance)
                except:
                    Log.error("Balance needs to be an integer")
            case ["save"]:
                with open(Network.DEFAULT_NETWORK_FILE, "wb") as f:
                    pickle.dump(self, f)
                Log.info(f"Successfully saved network to file {Network.DEFAULT_NETWORK_FILE}")
            case ["save", filename]:
                with open(filename, "wb") as f:
                    pickle.dump(self, f)
                Log.info(f"Successfully saved network to file {filename}")
            case ["help"]:
                self.printCommands()
            case ["stop"]:
                return
            case _:
                print(f"Invalid command (use {colored(Commands.HELP.key, attrs=['bold'])} to list all commands)")
    
    def printCommands(self) -> None:
        commands = []
        for _, command in vars(Commands).items():
            if type(command) == Command:
                commands.append([command.key, command.syntax, command.help])
        print(tabulate(commands, headers=[
            colored("Command", attrs=['bold']),
            colored("Syntax", attrs=['bold']),
            colored("Description", attrs=['bold'])
            ], tablefmt="simple"))
    
    def broadcastTransaction(self, transaction: Transaction) -> None:
        Log.info(f"Broadcasting transaction {colored(transaction.id, 'yellow')} to all nodes")
        validator = None
        for node in self.nodes.values():
            isMinting = node.addTransaction(transaction, list(self.nodes.keys()))
            if isMinting:
                validator = node
        if validator is not None:
            print()
            Log.info(f"Block Transaction Threshold of {BLOCK_TRANSACTION_THRESHOLD} reached. Proceeding to mint new block")
            Log.info(f"{colored(validator.id, attrs=['bold'])} is chosen as the validator", "MINTING")
            block = validator.mint()
            self.broadcastBlock(block)
    
    def broadcastBlock(self, block: Block | None) -> None:
        if block is not None:
            Log.info(f"Broadcasting minted block {block.id} to all nodes")
        for node in self.nodes.values():
            node.addBlock(block)
