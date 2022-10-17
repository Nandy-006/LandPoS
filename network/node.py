import random
from termcolor import colored

from blockchain.block import Block
from blockchain.blockchain import Blockchain
from blockchain.transaction import Transaction
from blockchain.constants import BLOCK_TRANSACTION_THRESHOLD
from utils.utils import Log

class Node:

    def __init__(self, id: str, blockchain: Blockchain, transactionPool: list[Transaction]) -> None:
        self.id = id
        self.blockchain = blockchain
        self.transactionPool = transactionPool

    def registerCoins(self, amount: int) -> Transaction:
        transaction = Transaction.newRCTransaction(self.id, amount)
        Log.info(f"{self.id} received {amount} coins from the network", "INITIATE TRANSACTION", self.id)
        return transaction
    
    def registerLand(self, landId: str) -> Transaction:
        transaction = Transaction.newLDTransaction(self.id, landId)
        Log.info(f"{self.id} owns land {landId}", "INITIATE TRANSACTION", self.id)
        return transaction
    
    def buyLand(self, landId: str, sellerId: str) -> Transaction:
        transaction = Transaction.newLTTransaction(sellerId, landId, self.id)
        Log.info(f"{self.id} buys land {landId} from {sellerId}", "INITIATE TRANSACTION", self.id)
        return transaction
    
    def sellLand(self, buyerId: str, landId: str) -> Transaction:
        transaction = Transaction.newLTTransaction(self.id, landId, buyerId)
        Log.info(f"{self.id} sells land {landId} to {buyerId}", "INITIATE TRANSACTION", self.id)
        return transaction
    
    def stake(self, amount: int) -> Transaction:
        transaction = Transaction.newSTTransaction(self.id, amount)
        Log.info(f"{self.id} stakes {amount} coins", "INITIATE TRANSACTION", self.id)
        return transaction
    
    def addTransaction(self, transaction: Transaction, peers: list[str]) -> bool:
        self.transactionPool.append(transaction)
        Log.info(f"Added {colored(transaction.id, 'yellow')} to pool", nodeId=self.id)
        if len(self.transactionPool) >= BLOCK_TRANSACTION_THRESHOLD:
            validator = self.getValidator(peers)
            if validator == self.id:
                return True
        return False

    def getValidator(self, peers: list[str]) -> str:
        stakes = self.blockchain.getStakes(peers)
        ages = self.blockchain.getAges(peers)
        coinages = [stakes[peer] * ages[peer] + 1 for peer in peers]
        if sum(coinages) == 0:
            coinages = [1] * len(coinages)
        
        random.seed(Block.hashBlock(self.blockchain.getLastBlock()))
        validators = random.choices(
            peers,
            coinages,
            k = 1
        )
        return validators[0]
    
    def mint(self) -> Block | None:
        blockData: list[Transaction] = []
        landOwners = self.blockchain.getLandOwners()
        balances = self.blockchain.getAllBalances()
        Log.info("Validating transactions", "MINTING", self.id)
        for transaction in self.transactionPool:
            isValid = self.validate(transaction, landOwners, balances)
            if isValid:
                blockData.append(transaction)
                if transaction.type == Transaction.RC_TRANSACTION:
                    # balances[transaction.input["user_id"]] = transaction.input["amount"]
                    pass
                elif transaction.type == Transaction.LD_TRANSACTION:
                    landOwners[transaction.input["land_id"]] = transaction.input["user_id"]
                elif transaction.type == Transaction.LT_TRANSACTION:
                    landOwners[transaction.input["land_id"]] = transaction.output["user_id"]
                    pass
                elif transaction.type == Transaction.ST_TRANSACTION:
                    balances[transaction.input["user_id"]] -= transaction.input["amount"]
        
        if len(blockData) == 0:
            Log.info("All transactions are invalid. No new block is minted", "MINTING", self.id)
            return None
        
        block = Block.createBlock(self.blockchain.getLength(), self.blockchain.getLastBlock(), self.id, blockData)
        Log.info("Minted new block", "MINTING", self.id)
        print(block)
        return block

    def validate(self, transaction: Transaction, landOwners: dict[str, str], balances: dict[str, int]) -> bool:
        if transaction.type == Transaction.RC_TRANSACTION:
            pass
        elif transaction.type == Transaction.LD_TRANSACTION:
            if transaction.input["land_id"] in landOwners:
                Log.info(
                    f"{{ {repr(transaction)} }} is {colored('invalid', 'red', attrs=['bold'])} as land is already registered",
                    "MINTING",
                    self.id
                )
                return False
        elif transaction.type == Transaction.LT_TRANSACTION:
            trueLandOwners = self.blockchain.getLandOwners()
            if transaction.input["land_id"] not in trueLandOwners:
                Log.info(
                    f"{{ {repr(transaction)} }} is {colored('invalid', 'red', attrs=['bold'])} as land is not registered",
                    "MINTING",
                    self.id
                )
                return False
            if not transaction.input["user_id"] == trueLandOwners[transaction.input["land_id"]] == landOwners[transaction.input["land_id"]]:
                Log.info(
                    f"{{ {repr(transaction)} }} is {colored('invalid', 'red', attrs=['bold'])} as seller does not own this land",
                    "MINTING",
                    self.id
                )
                return False
            if transaction.input["user_id"] == transaction.output["user_id"]:
                Log.info(
                    f"{{ {repr(transaction)} }} is {colored('invalid', 'red', attrs=['bold'])} as buyer and seller cannot be the same",
                    "MINTING",
                    self.id
                )
                return False
        elif transaction.type == Transaction.ST_TRANSACTION:
            nodeId = transaction.input["user_id"]
            if nodeId not in balances:
                balance = 0
            else:
                balance = balances[nodeId]
            if balance < transaction.input["amount"]:
                Log.info(
                    f"{{ {repr(transaction)} }} is {colored('invalid', 'red', attrs=['bold'])} as user does not have sufficient balance",
                    "MINTING",
                    self.id
                )
                return False
            elif transaction.input["amount"] <= 0:
                Log.info(
                    f"{{ {repr(transaction)} }} is {colored('invalid', 'red', attrs=['bold'])} as stake needs to be a positive amount",
                    "MINTING",
                    self.id
                )
                return False
        else:
            Log.error(f"{{ {repr(transaction)} }} is of invalid type {transaction.type}")
            return False
        
        Log.info(f"{{ {repr(transaction)} }} is valid", "MINTING", self.id)
        return True
    
    def addBlock(self, block: Block | None) -> None:
        self.transactionPool = []

        if block is None:
            return
        
        self.blockchain.addBlock(block)
        Log.info(f"Added block {self.id} to blockchain", nodeId = self.id)
