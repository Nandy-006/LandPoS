import hashlib
import pickle
from datetime import datetime
from blockchain.merkle_tree import MerkleTree
from blockchain.transaction import Transaction
from blockchain.constants import GENESIS_BLOCK_MERKLE_ROOT, GENESIS_BLOCK_VALIDATOR, GENESIS_BLOCK_PREVIOUS_BLOCK_HASH, GENESIS_BLOCK_DATA

class Block:
    def __init__(
        self, 
        timestamp: datetime, 
        previousBlockHash: str, 
        merkleRoot: str, 
        validator: str, 
        data: list[Transaction]
    ) -> None:
        self.timestamp = timestamp
        self.previousBlockHash = previousBlockHash
        self.merkleRoot = merkleRoot
        self.validator = validator
        self.data = data

    @staticmethod
    def serialize(block: 'Block') -> bytes:
        return pickle.dumps(block)

    @staticmethod
    def hashBlock(block: 'Block') -> str:
        return hashlib.sha256(Block.serialize(block)).hexdigest()

    @staticmethod
    def genesis() -> 'Block':
        timestamp = datetime.now()
        return Block(
            timestamp, 
            GENESIS_BLOCK_PREVIOUS_BLOCK_HASH, 
            GENESIS_BLOCK_MERKLE_ROOT, 
            GENESIS_BLOCK_VALIDATOR,
            GENESIS_BLOCK_DATA
        )

    @staticmethod
    def createBlock(lastBlock: 'Block', validator: str, data: list[Transaction]) -> 'Block':
        timestamp = datetime.now()
        previousBlockHash = Block.hashBlock(lastBlock)
        merkleRoot = MerkleTree.getMerkleRoot(data)
        return Block(timestamp, previousBlockHash, merkleRoot, validator, data)
    
    def __str__(self) -> str:
        return "\n".join([
            f"BLOCK HEADER",
            f"Timestamp: {self.timestamp}",
            f"Prev. Block Hash: {self.previousBlockHash}",
            f"Merkle Root: {self.merkleRoot}",
            f"Validator: {self.validator}",
            f"",
            f"BLOCK DATA",
        ] + [
            str(transaction) for transaction in self.data
        ] + [
            "\n"
        ])
