import random
from termcolor import colored

from blockchain.block import Block
from blockchain.blockchain import Blockchain
from blockchain.transaction import Transaction
from blockchain.constants import BLOCK_TRANSACTION_THRESHOLD
from utils.utils import Log

class Node:

    def __init__(self, id: str, balance: int, blockchain: Blockchain, transactionPool: list[Transaction]) -> None:
        self.id = id
        self.balance = balance
        self.blockchain = blockchain
        self.transactionPool = transactionPool
    
    def registerLand(self, landId: str) -> Transaction:
        transaction = Transaction.newLDTransaction(self.id, landId)
        Log.info(f"{self.id} owns land {landId}", "INITIATE TRANSACTION", self.id)
        return transaction
    
    def buyLand(self, landId: str) -> Transaction | None:
        sellerId = self.blockchain.getLandOwner(landId)
        if sellerId is None:
            Log.error(f"Land ID {landId} is unknown")
            return None
        transaction = Transaction.newLTTransaction(sellerId, landId, self.id)
        Log.info(f"{self.id} buys land {landId} from {sellerId}", "INITIATE TRANSACTION", self.id)
        return transaction
    
    def sellLand(self, buyerId: str, landId: str) -> Transaction:
        transaction = Transaction.newLTTransaction(self.id, landId, buyerId)
        Log.info(f"{self.id} sells land {landId} to {buyerId}", "INITIATE TRANSACTION", self.id)
        return transaction
    
    def stake(self, amount: int) -> Transaction | None:
        if amount > self.balance:
            Log.error("Insufficient balance for this transaction")
            return None
        transaction = Transaction.newSTTransaction(self.id, amount)
        Log.info(f"{self.id} stakes {amount} coins", "INITIATE TRANSACTION", self.id)
        return transaction
    
    def addTransaction(self, transaction: Transaction, peers: list[str]) -> bool:
        self.transactionPool.append(transaction)
        if len(self.transactionPool) >= BLOCK_TRANSACTION_THRESHOLD:
            validator = self.getValidator(peers)
            if validator == self.id:
                return True
        return False

    def getValidator(self, peers: list[str]) -> str:
        stakes = self.blockchain.getStakes()
        ages = self.blockchain.getAges()
        for peer in peers:
            stakes[peer] = 0 if peer not in stakes else stakes[peer]
            ages[peer] = 0 if peer not in ages else ages[peer]
        
        random.seed(Block.hashBlock(self.blockchain.getLastBlock()))
        validators = random.choices(
            peers,
            [stakes[peer] * ages[peer] + 1 for peer in peers],
            k = 1
        )
        return validators[0]
    
    def mint(self) -> Block | None:
        blockData: list[Transaction] = []
        landOwners = self.blockchain.getLandOwners()
        for transaction in self.transactionPool:
            isValid = self.validate(transaction, landOwners)
            if isValid:
                blockData.append(transaction)
                if transaction.type == Transaction.LD_TRANSACTION:
                    landOwners[transaction.input["land_id"]] = transaction.input["user_id"]
                elif transaction.type == Transaction.LT_TRANSACTION:
                    landOwners[transaction.input["land_id"]] = transaction.output["user_id"]
        
        if len(blockData) == 0:
            Log.info("All transactions are invalid. No new block is minted", "MINTING", self.id)
            return None
        
        block = Block.createBlock(self.blockchain.getLastBlock(), self.id, blockData)
        Log.info("Minted new block", "MINTING", self.id)
        print(block)
        return block

    def validate(self, transaction: Transaction, landOwners: dict) -> bool:
        if transaction.type == Transaction.LD_TRANSACTION:
            if transaction.input["land_id"] in landOwners:
                Log.info(
                    f"{{ {repr(transaction)} }} is {colored('invalid', 'red', attrs=['bold'])} as land is already registered",
                    "MINTING",
                    self.id
                )
                return False
        elif transaction.type == Transaction.LT_TRANSACTION:
            if transaction.input["user_id"] != landOwners[transaction.input["land_id"]]:
                Log.info(
                    f"{{ {repr(transaction)} }} is {colored('invalid', 'red', attrs=['bold'])} as seller does not own this land",
                    "MINTING",
                    self.id
                )
                return False
        elif transaction.type == Transaction.ST_TRANSACTION:
            Log.info(f"{{ {repr(transaction)} }} is valid", "MINTING", self.id)
        else:
            Log.error(f"{{ {repr(transaction)} }} is of invalid type {transaction.type}")
            return False
        
        return True
    
    def addBlock(self, block: Block | None) -> None:
        self.transactionPool = []

        if block is None:
            return
        
        self.blockchain.addBlock(block)
        Log.info("Added minted block to blockchain", nodeId = self.id)