import random
from termcolor import colored

from blockchain.block import Block
from blockchain.blockchain import Blockchain
from blockchain.transaction import Transaction
from blockchain.constants import BLOCK_TRANSACTION_THRESHOLD
from utils.utils import Log

# Node represents a single user on the blockchain network
class Node:

    def __init__(self, id: str, blockchain: Blockchain, transactionPool: list[Transaction]) -> None:
        self.id = id
        self.blockchain = blockchain
        self.transactionPool = transactionPool

    # Inititates a transaction to set the node's initial balance
    def registerCoins(self, amount: int) -> Transaction:
        transaction = Transaction.newRCTransaction(self.id, amount)
        Log.info(f"{self.id} received {amount} coins from the network", "INITIATE TRANSACTION", self.id)
        return transaction
    
    # Initates a new transaction to register a new land under the user
    def registerLand(self, landId: str) -> Transaction:
        transaction = Transaction.newLDTransaction(self.id, landId)
        Log.info(f"{self.id} owns land {landId}", "INITIATE TRANSACTION", self.id)
        return transaction
    
    # Initiates a new transaction for buying a land
    def buyLand(self, landId: str, sellerId: str) -> Transaction:
        transaction = Transaction.newLTTransaction(sellerId, landId, self.id)
        Log.info(f"{self.id} buys land {landId} from {sellerId}", "INITIATE TRANSACTION", self.id)
        return transaction

    # Initiates a new transaction for selling a land
    def sellLand(self, buyerId: str, landId: str) -> Transaction:
        transaction = Transaction.newLTTransaction(self.id, landId, buyerId)
        Log.info(f"{self.id} sells land {landId} to {buyerId}", "INITIATE TRANSACTION", self.id)
        return transaction
    
    # Initiate a new transaction to increase the stake of a node
    def stake(self, amount: int) -> Transaction:
        transaction = Transaction.newSTTransaction(self.id, amount)
        Log.info(f"{self.id} stakes {amount} coins", "INITIATE TRANSACTION", self.id)
        return transaction
    
    # Adds a transaction to the transaction pool
    def addTransaction(self, transaction: Transaction, peers: list[str]) -> bool:
        self.transactionPool.append(transaction)
        Log.info(f"Added {colored(transaction.id, 'yellow')} to pool", nodeId=self.id)
        if len(self.transactionPool) >= BLOCK_TRANSACTION_THRESHOLD:
            validator = self.getValidator(peers)
            if validator == self.id:
                return True
        return False

    # PROOF OF STAKE CONSENSUS
    # A validator is selected from the set of nodes in the network. This done by using the coinage of the nodes.
    # Stake - The amount of coins staked by the node in the network
    # Age - The number of blocks since the last block minted by a node
    # Coinage - The product of stake and age
    # A node is randomly chose as a validator (Weighted by their coinages)
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
    
    # Minting
    # The validator chosen validates all transactions and mints a block
    def mint(self) -> Block | None:
        blockData: list[Transaction] = []
        landOwners = self.blockchain.getLandOwners()
        balances = self.blockchain.getAllBalances()
        
        # Validate all transactions in the pool
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

        block = Block.createBlock(self.blockchain.getLength(), self.blockchain.getLastBlock(), self.id, blockData)
        Log.info("Minted new block", "MINTING", self.id)
        print(block)
        return block

    # Transaction validation
    # Receive Coins Transaction
    #   Is assumed to be valid since it is initiated by the network
    #
    # Land Declaration Transaction
    #   Is invalid if the land is already declared by someone else
    #
    # Land Transfer Transaction
    #   Is invalid if the land is not registered
    #   Is invalid if the seller is not the owner of the land
    #   Is invalid if the buyer and seller is the same
    #
    # Stake Increase Transaction
    #   Is invalid if the user's balance is less than the amount they are trying to stake 
    #   Is invalid if the amount specified is negative or 0
    def validate(self, transaction: Transaction, landOwners: dict[str, str], balances: dict[str, int]) -> bool:
        if transaction.type == Transaction.RC_TRANSACTION:
            pass
        elif transaction.type == Transaction.LD_TRANSACTION:
            if transaction.input["land_id"] in landOwners:
                Log.info(
                    f"Transaction {colored(transaction.id, 'yellow')}: {str(transaction)} is {colored('invalid', 'red', attrs=['bold'])} as land is already registered",
                    "MINTING",
                    self.id
                )
                return False
        elif transaction.type == Transaction.LT_TRANSACTION:
            trueLandOwners = self.blockchain.getLandOwners()
            if transaction.input["land_id"] not in trueLandOwners:
                Log.info(
                    f"Transaction {colored(transaction.id, 'yellow')}: {str(transaction)} is {colored('invalid', 'red', attrs=['bold'])} as land is not registered",
                    "MINTING",
                    self.id
                )
                return False
            if not transaction.input["user_id"] == trueLandOwners[transaction.input["land_id"]] == landOwners[transaction.input["land_id"]]:
                Log.info(
                    f"Transaction {colored(transaction.id, 'yellow')}: {str(transaction)} is {colored('invalid', 'red', attrs=['bold'])} as seller does not own this land",
                    "MINTING",
                    self.id
                )
                return False
            if transaction.input["user_id"] == transaction.output["user_id"]:
                Log.info(
                    f"Transaction {colored(transaction.id, 'yellow')}: {str(transaction)} is {colored('invalid', 'red', attrs=['bold'])} as buyer and seller cannot be the same",
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
                    f"Transaction {colored(transaction.id, 'yellow')}: {str(transaction)} is {colored('invalid', 'red', attrs=['bold'])} as user does not have sufficient balance",
                    "MINTING",
                    self.id
                )
                return False
            elif transaction.input["amount"] <= 0:
                Log.info(
                    f"Transaction {colored(transaction.id, 'yellow')}: {str(transaction)} is {colored('invalid', 'red', attrs=['bold'])} as stake needs to be a positive amount",
                    "MINTING",
                    self.id
                )
                return False
        else:
            Log.error(f"Transaction {colored(transaction.id, 'yellow')}: {str(transaction)} is of invalid type {transaction.type}")
            return False
        
        Log.info(f"Transaction {colored(transaction.id, 'yellow')}: {str(transaction)} is {colored('valid', 'green')}", "MINTING", self.id)
        return True
    
    # Adds a block to the transaction and empties the transaction pool
    def addBlock(self, block: Block | None) -> None:
        self.transactionPool = []

        if block is None:
            return
        
        self.blockchain.addBlock(block)
        Log.info(f"Added block {self.id} to blockchain", nodeId = self.id)
