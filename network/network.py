import random
from blockchain.block import Block
from blockchain.blockchain import Blockchain
from blockchain.transaction import Transaction
from blockchain.constants import BLOCK_TRANSACTION_THRESHOLD
from utils.utils import Log
from network.node import Node

class Network:

    def __init__(self) -> None:
        self.nodes = {}
        self.lands = {}
        self.transactionPool = []
        self.blockchain = Blockchain()
    
    def registerNode(self, id: str, balance: int) -> None:
        if id in self.nodes:
            Log.error("Node already exists")
            return None
        
        newNode = Node(id, balance)
        self.nodes[id] = newNode
        Log.info(f"Node with ID {id} has joined the network", "New Node")
        return newNode
    
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
