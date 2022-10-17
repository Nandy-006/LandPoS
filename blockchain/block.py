import hashlib
import pickle
from datetime import datetime
from termcolor import colored
from tabulate import tabulate

from blockchain.merkle_tree import MerkleTree
from blockchain.transaction import Transaction
from blockchain.constants import GENESIS_BLOCK_MERKLE_ROOT, GENESIS_BLOCK_VALIDATOR, GENESIS_BLOCK_PREVIOUS_BLOCK_HASH, GENESIS_BLOCK_DATA

# The Block class is used to represent a block in the blockchain and has methods relating to creating and modifying blocks
# The structure of the block is as follows
#
# BLOCK HEADER
#   ID: The height of the block
#   Timestamp: The timestamp when the block was minted
#   Prev. block hash: The hash of the previous block
#   Merkle Root: The merkle root of the transactions in the block
#   Validator: The ID of the validator of the block
# BLOCK DATA
#   Transaction 1 ... n 
class Block:
    def __init__(
        self,
        id: int,
        timestamp: datetime,
        previousBlockHash: str,
        merkleRoot: str,
        validator: str,
        data: list[Transaction]
    ) -> None:
        self.id = id
        self.timestamp = timestamp
        self.previousBlockHash = previousBlockHash
        self.merkleRoot = merkleRoot
        self.validator = validator
        self.data = data

    @staticmethod
    def hashBlock(block: 'Block') -> str:
        return hashlib.sha256(Block.serialize(block)).hexdigest()

    @staticmethod
    def genesis() -> 'Block':
        timestamp = datetime.now()
        return Block(
            0,
            timestamp, 
            GENESIS_BLOCK_PREVIOUS_BLOCK_HASH, 
            GENESIS_BLOCK_MERKLE_ROOT, 
            GENESIS_BLOCK_VALIDATOR,
            GENESIS_BLOCK_DATA
        )

    @staticmethod
    def createBlock(id: int, lastBlock: 'Block', validator: str, data: list[Transaction]) -> 'Block':
        timestamp = datetime.now()
        previousBlockHash = Block.hashBlock(lastBlock)
        merkleRoot = MerkleTree.getMerkleRoot(data)
        return Block(id, timestamp, previousBlockHash, merkleRoot, validator, data)
    
    @staticmethod
    def serialize(block: 'Block') -> bytes:
        return pickle.dumps(block)
    
    def __str__(self) -> str:
        return tabulate([
            [colored("BLOCK HEADER", "green", attrs=["bold"]), "", ""],
            [colored("ID", attrs=["bold"]), self.id, ""],
            [colored("Timestamp", attrs=["bold"]), self.timestamp, ""],
            [colored("Prev. Block Hash", attrs=["bold"]), self.previousBlockHash, ""],
            [colored("Merkle Root", attrs=["bold"]), self.merkleRoot, ""],
            [colored("Validator", attrs=["bold"]), self.validator, ""],
            [colored("BLOCK DATA", "green", attrs=["bold"]), "", ""],
        ] + [[transaction.id, transaction.timestamp, str(transaction)] for transaction in self.data],
        tablefmt="grid") + "\n"
