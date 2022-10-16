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
    
    def registerNode(self, id, balance):
        if id in self.nodes:
            Log.error("Node already exists")
            return None
        
        newNode = Node(id, balance)
        self.nodes[id] = newNode
        return newNode
    
    def getValidator(self):
        validators = []
        for _, node in self.nodes.items():
            validators.append((node.stake * node.age, node.id))
        validators.sort(reverse=True)
        return self.nodes[validators[0][1]]
    
    def broadcastTransaction(self, transaction):
        self.transactionPool.append(transaction)
        if len(self.transactionPool) >= BLOCK_TRANSACTION_THRESHOLD:
            validator = self.getValidator()
            block = validator.mint(self.transactionPool, self.lands, self.nodes, self.blockchain)
            if block is None:
                Log.error("All transactions are invalid. No new block minted")
                return
            self.addBlock(block)
    
    def addBlock(self, block):
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

    def registerLand(self, node, land):
        transaction = Transaction.newLDTransaction(node.id, land)
        self.broadcastTransaction(transaction)

    def stake(self, node, amount):
        transaction = Transaction.newSTTransaction(node.id, amount)
        self.broadcastTransaction(transaction)
    
    def buy(self, buyer, land):
        seller = self.lands[land]
        transaction = Transaction.newLTTransaction(seller.id, land, buyer.id)
        self.broadcastTransaction(transaction)

    def sell(self, seller, buyer, land):
        transaction = Transaction.newLTTransaction(seller.id, land, buyer.id)
        self.broadcastTransaction(transaction)

    def getLandHistory(self, land):
        history = self.blockchain.getLandHistory(land)
        if len(history) == 0:
                Log.error("Unknown Land ID")
                return None
        for transaction in history:
            print(f"- {transaction.timestamp}: {transaction.input['user_id']}")    
