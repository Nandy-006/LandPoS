from blockchain.block import Block
from blockchain.blockchain import Blockchain
from blockchain.transaction import Transaction
from utils.utils import Log

class Node:

    def __init__(self, id: str, balance: int) -> None:
        self.id = id
        self.balance = balance
        self.stake = 0
        self.age = 1
    
    def mint(self, transactionPool: list[Transaction], lands: dict, nodes: dict, blockchain: Blockchain) -> Block | None:
        blockTransactions = []
        for transaction in transactionPool:
            isValid = self.validate(transaction, lands, nodes)
            if isValid:
                blockTransactions.append(transaction)
            else:
                return None
        
        if len(blockTransactions) == 0:
            return None
        return Block.createBlock(blockchain.getLastBlock(), self.id, blockTransactions)

    def validate(self, transaction: Transaction, lands: dict, nodes: dict) -> bool:
        if transaction.type == Transaction.LD_TRANSACTION:
            if transaction.input["land_id"] in lands:
                Log.error(f"<{transaction}> is invalid as land is already registered")
                return False
        elif transaction.type == Transaction.LT_TRANSACTION:
            if transaction.input["user_id"] != lands[transaction.input["land_id"]].id:
                Log.error(f"<{transaction} is invalid as seller does not own this land")
                return False
        elif transaction.type == Transaction.ST_TRANSACTION:
            if transaction.input["amount"] > nodes[transaction.input["user_id"]].balance:
                Log.error(f"<{transaction} is invalid as user does not have sufficient balance")
                return False
        else:
            Log.error(f"<{transaction}> is of invalid type {transaction.type}")
            return False
        
        return True