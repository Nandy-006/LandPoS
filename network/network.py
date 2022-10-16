from copy import deepcopy
from termcolor import colored
from tabulate import tabulate

from blockchain.block import Block
from blockchain.blockchain import Blockchain
from blockchain.transaction import Transaction
from utils.utils import Log, Command
from network.node import Node

class Commands:

    # Node specific
    REGISTER = Command("register", "<node_id> register <land_id>", "Register new land under node")
    BUY = Command("buy", "<node_id> buy <land_id>", "Buy specified land")
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
    NODES = Command("nodes", "nodes", "Get all registered nodes")

    # Network
    HELP = Command("help", "help", "List all commands")
    STOP = Command("stop", "stop", "Stop the network")

class Network:

    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
    
    def registerNode(self, id: str, balance: int) -> None:
        if id in self.nodes:
            Log.error("Node already exists")
            return None

        if len(self.nodes) == 0:
            newNode = Node(id, balance, Blockchain(), [])
        else:
            existingNode = list(self.nodes.values())[0]
            newNode = Node(id, balance, deepcopy(existingNode.blockchain), deepcopy(existingNode.transactionPool))
        self.nodes[id] = newNode
        Log.info(f"Node {id} has joined the network", "NEW NODE")
    
    def start(self):
        Log.info("Starting the network")
        while True:
            command = input("\n> ").split(" ")
            if command[0] == Commands.STOP.key:
                Log.info("Stopping the network...")
                break
            else:
                self.handle(command)
        Log.info("Stopped the network")

    def run(self, command: str) -> None:
        self.handle(command.split(" "))
    
    def nodeExists(self, nodeId: str | None = None) -> bool:
        if nodeId is None:
            if len(self.nodes) <= 0:
                Log.error(f"At least one node needs to be registered in the network")
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
            case [nodeId, "buy", landId]:
                if self.nodeExists(nodeId):
                    transaction = self.nodes[nodeId].buyLand(landId)
                    if transaction is not None:
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
                    if transaction is not None:
                        self.broadcastTransaction(transaction)
            case [nodeId, "balance"]:
                if self.nodeExists(nodeId):
                    print(f"{colored('BALANCE', attrs=['bold'])}: {self.nodes[nodeId].balance}")
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
                    Log.info(f"List of available lands", "LANDS")
                    for land in landOwners.keys():
                        print(f"* {land}")
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
            case ["nodes"]:
                if len(self.nodes) <= 0:
                    Log.info("No node is registered to the network")
                else:
                    for nodeId in self.nodes.keys():
                        print(f"- {nodeId}")
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
        print(tabulate(commands, headers=["Command", "Syntax", "Description"], tablefmt="simple"))
    
    def broadcastTransaction(self, transaction: Transaction) -> None:
        validator = None
        for node in self.nodes.values():
            isMinting = node.addTransaction(transaction, list(self.nodes.keys()))
            if isMinting:
                validator = node
        if validator is not None:
            block = validator.mint()
            self.broadcastBlock(block)
    
    def broadcastBlock(self, block: Block | None) -> None:
        Log.info("Broadcasting minted block to all nodes")
        for node in self.nodes.values():
            node.addBlock(block)
