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

    # adds coins to the new node's wallet on registration
    def registerCoins(self, amount: int) -> Transaction:
        transaction = Transaction.newRCTransaction(self.id, amount)
        Log.info(f"{self.id} received {amount} coins from the network", "INITIATE TRANSACTION", self.id)
        return transaction
    
    # registers existing land under a user
    def registerLand(self, landId: str) -> Transaction:
        transaction = Transaction.newLDTransaction(self.id, landId)
        Log.info(f"{self.id} owns land {landId}", "INITIATE TRANSACTION", self.id)
        return transaction
    
    # initiates a new transaction for buying a land
    def buyLand(self, landId: str, sellerId: str) -> Transaction:
        transaction = Transaction.newLTTransaction(sellerId, landId, self.id)
        Log.info(f"{self.id} buys land {landId} from {sellerId}", "INITIATE TRANSACTION", self.id)
        return transaction
    # initiates a new transaction for selling a land
    def sellLand(self, buyerId: str, landId: str) -> Transaction:
        transaction = Transaction.newLTTransaction(self.id, landId, buyerId)
        Log.info(f"{self.id} sells land {landId} to {buyerId}", "INITIATE TRANSACTION", self.id)
        return transaction
    
    # increases the stake of the node and makes a transaction of it
    def stake(self, amount: int) -> Transaction:
        transaction = Transaction.newSTTransaction(self.id, amount)
        Log.info(f"{self.id} stakes {amount} coins", "INITIATE TRANSACTION", self.id)
        return transaction
    
    # creates a new transaction and adds it to the transaction pool
    def addTransaction(self, transaction: Transaction, peers: list[str]) -> bool:
        self.transactionPool.append(transaction)
        Log.info(f"Added {colored(transaction.id, 'yellow')} to pool", nodeId=self.id)
        if len(self.transactionPool) >= BLOCK_TRANSACTION_THRESHOLD:
            validator = self.getValidator(peers)
            if validator == self.id:
                return True
        return False

    # chooses and returns a validator from the existing group nodes via Proof of Stake consensus
    def getValidator(self, peers: list[str]) -> str:
        stakes = self.blockchain.getStakes(peers)
        ages = self.blockchain.getAges(peers)
        
        # all coinages are calculated and if they're all 0 then they're set as one(temporary)
        coinages = [stakes[peer] * ages[peer] + 1 for peer in peers]
        if sum(coinages) == 0:
            coinages = [1] * len(coinages)
        
        # the validator is chosen based on a skewed probability with the coinage of each node in consideration
        random.seed(Block.hashBlock(self.blockchain.getLastBlock()))
        validators = random.choices(
            peers,
            coinages,
            k = 1
        )
        return validators[0]
    
    # a new block is minted and returned after validating the transactions in the pool
    def mint(self) -> Block | None:
        blockData: list[Transaction] = []
        landOwners = self.blockchain.getLandOwners()
        balances = self.blockchain.getAllBalances()
        
        # validates all transactions in the transaction pool
        Log.info("Validating transactions", "MINTING", self.id)
        for transaction in self.transactionPool:
            isValid = self.validate(transaction, landOwners, balances)
            if isValid:
                # updates the wallets and the lands of the nodes once the transaction is validated
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
        
        # new block minted
        block = Block.createBlock(self.blockchain.getLength(), self.blockchain.getLastBlock(), self.id, blockData)
        Log.info("Minted new block", "MINTING", self.id)
        print(block)
        return block

    # validates the transaction by checking if the conditions are met
    def validate(self, transaction: Transaction, landOwners: dict[str, str], balances: dict[str, int]) -> bool:
        if transaction.type == Transaction.RC_TRANSACTION:
            pass
        # checks if the land is already declared
        elif transaction.type == Transaction.LD_TRANSACTION:
            if transaction.input["land_id"] in landOwners:
                Log.info(
                    f"{{ {repr(transaction)} }} is {colored('invalid', 'red', attrs=['bold'])} as land is already registered",
                    "MINTING",
                    self.id
                )
                return False
        # checks if the land is declared and that the seller owns said land
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
        # checks if the user has enough coins in their wallet to insrease stake
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
    
    # adds minted block to the blockchain
    def addBlock(self, block: Block | None) -> None:
        self.transactionPool = []

        if block is None:
            return
        
        self.blockchain.addBlock(block)
        Log.info(f"Added block {self.id} to blockchain", nodeId = self.id)
