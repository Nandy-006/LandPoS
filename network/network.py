import random
from blockchain.block import Block
from blockchain.blockchain import Blockchain
from blockchain.transaction import Transaction
from blockchain.constants import BLOCK_TRANSACTION_THRESHOLD
from utils.utils import Log, Command
from network.node import Node
from termcolor import colored
from tabulate import tabulate

class Commands:

    # Node specific
    REGISTER = Command("register", "<node_id> register <land_id>", "Register new land under node")
    BUY = Command("buy", "<node_id> buy <land_id>", "Buy specified land")
    SELL = Command("sell", "<node_id> sell <land_id> <receiver_id>", "Sell specified land")
    STAKE = Command("stake", "<node_id> stake <amount>", "Stake specified amount")
    BALANCE = Command("balance", "<node_id> balance", "Get node's current balance")

    # Node independent
    TRANSACTION = Command("transaction", "transaction <transaction_id>", "Get details of a transaction on the blockchain")
    BLOCK = Command("block", "block <n>", "Get nth block in the blockchain")
    HISTORY = Command("history", "history <land_id>", "Get history of land owners")
    BLOCKCHAIN = Command("blockchain", "blockchain", "Get the blockchain")
    LANDS = Command("lands", "lands", "Get all registered lands and their owners")
    POOL = Command("pool", "pool", "Get the current transaction pool")

    # Network
    HELP = Command("help", "help", "List all commands")
    STOP = Command("stop", "stop", "Stop the network")

class Network:

    INVALID_COMMAND = f"Invalid command (use {colored(Commands.HELP.key, attrs=['bold'])} to list all commands)"

    def __init__(self) -> None:
        self.nodes: dict[int, Node] = {}
    
    def registerNode(self, id: int, balance: int) -> None:
        if id in self.nodes:
            Log.error("Node already exists")
            return None
        
        newNode = Node(id, balance)
        self.nodes[id] = newNode
        Log.info(f"Node {id} has joined the network", "New Node")
    
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

    def handle(self, command: list[str]) -> None:
        try:
            nodeId = int(command[0])
            if len(command) == 1:
                Log.error(Network.INVALID_COMMAND)
                return
            if command[1] == Commands.REGISTER.key:
                pass
            elif command[1] == Commands.BUY.key:
                pass
            elif command[1] == Commands.SELL.key:
                pass
            elif command[1] == Commands.STAKE.key:
                pass
            elif command[1] == Commands.BALANCE.key:
                pass
            else:
                Log.error(Network.INVALID_COMMAND)
        except:
            if command[0] == Commands.HELP.key:
                self.printCommands()
            elif command[0] == Commands.STOP.key:
                return
            elif command[0] == Commands.TRANSACTION.key:
                pass
            elif command[0] == Commands.BLOCK.key:
                pass
            elif command[0] == Commands.HISTORY.key:
                pass
            elif command[0] == Commands.BLOCKCHAIN.key:
                pass
            elif command[0] == Commands.LANDS.key:
                pass
            elif command[0] == Commands.POOL.key:
                pass
            else:
                Log.error(Network.INVALID_COMMAND)
    
    def printCommands(self) -> None:
        commands = []
        for _, command in vars(Commands).items():
            if type(command) == Command:
                commands.append([command.key, command.syntax, command.help])
        print(tabulate(commands, headers=["Command", "Syntax", "Description"], tablefmt="simple"))
    
    def getValidator(self) -> Node:
        validators = random.choices(
            list(self.nodes.values()),
            [node.stake * node.age + 1 for node in list(self.nodes.values())],
            k = 1
        )
        return validators[0]
    
    def broadcastTransaction(self, transaction: Transaction) -> None:
        self.transactionPool.append(transaction)
        if len(self.transactionPool) >= BLOCK_TRANSACTION_THRESHOLD:
            validator = self.getValidator()
            block = validator.mint(self.transactionPool, self.lands, self.nodes, self.blockchain)
            if block is None:
                Log.error("All transactions are invalid. No new block minted")
                return
            self.addBlock(block)
    
    def addBlock(self, block: Block) -> None:
        if self.blockchain.addBlock(block) is None:
            Log.error(f"Invalid block\n {block}")
            return
        
        for _, node in self.nodes.items():
            if node.id == block.validator:
                node.age = 0
            else:
                node.age += 1
        
        for transaction in block.data:
            if transaction.type == Transaction.LD_TRANSACTION:
                self.lands[transaction.input["land_id"]] = self.nodes[transaction.input["user_id"]]
            elif transaction.type == Transaction.LT_TRANSACTION:
                self.lands[transaction.input["land_id"]] = self.nodes[transaction.output["user_id"]]
            elif transaction.type == Transaction.ST_TRANSACTION:
                node = self.nodes[transaction.input["user_id"]]
                node.balance -= transaction.input["amount"]
                node.stake += transaction.input["amount"]
            else:
                Log.error(f"<{transaction}> is of invalid type {transaction.type}")
        
        self.transactionPool = []

    def registerLand(self, node: Node, land: str) -> None:
        transaction = Transaction.newLDTransaction(node.id, land)
        Log.info(f"{node.id} owns land {land}", "New Transaction")
        self.broadcastTransaction(transaction)

    def stake(self, node: Node, amount: int) -> None:
        transaction = Transaction.newSTTransaction(node.id, amount)
        Log.info(f"{node.id} staked {amount} coins", "New Transaction")
        self.broadcastTransaction(transaction)
    
    def buy(self, buyer: Node, land: str) -> None:
        seller = self.lands[land]
        transaction = Transaction.newLTTransaction(seller.id, land, buyer.id)
        Log.info(f"{buyer.id} buys land {land} from {seller.id}", "New Transaction")
        self.broadcastTransaction(transaction)

    def sell(self, seller: Node, buyer: Node, land: str) -> None:
        transaction = Transaction.newLTTransaction(seller.id, land, buyer.id)
        Log.info(f"{seller.id} sells land {land} to {buyer.id}", "New Transaction")
        self.broadcastTransaction(transaction)

    def getLandHistory(self, land: str) -> None:
        history = self.blockchain.getLandHistory(land)
        if len(history) == 0:
                Log.error("Unknown Land ID")
                return None
        Log.info(f"Transactions associated with land {land}", "Land History")
        for transaction in history:
            print(f"- {transaction.timestamp}: {transaction.input['user_id']}")    
