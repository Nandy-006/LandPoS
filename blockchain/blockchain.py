from termcolor import colored

from blockchain.block import Block
from blockchain.transaction import Transaction
from utils.utils import Log

class Blockchain:
    def __init__(self) -> None:
        self.chain = [Block.genesis()]

    def addBlock(self, block: Block) -> Block | None:
        if block.previousBlockHash == Block.hashBlock(self.getLastBlock()):
            self.chain.append(block)
        else:
            Log.error("Invalid block")
            return None
        return block
    
    def getLength(self) -> int:
        return len(self.chain)

    def getTransaction(self, transactionId: str) -> Transaction | None:
        for block in self.chain:
            for transaction in block.data:
                if transaction.id == transactionId:
                    return transaction

        Log.error("Transaction does not exist")
        return

    def getLandHistory(self, landId: str) -> list[Transaction]:
        landHistory = []
        for block in self.chain:
            for transaction in block.data:
                if transaction.type in [Transaction.LD_TRANSACTION, Transaction.LT_TRANSACTION] and transaction.input['land_id'] == landId:
                    landHistory.append(transaction)

        return landHistory

    def getLandOwner(self, landId: str) -> str | None:
        history = self.getLandHistory(landId)
        if len(history) == 0:
            return None
        return history[-1].output['user_id']
    
    def getLandOwners(self) -> dict[str, str]:
        landOwners = {}
        for block in self.chain:
            for transaction in block.data:
                if transaction.type == Transaction.LD_TRANSACTION:
                    landOwners[transaction.input["land_id"]] = transaction.input["user_id"]
                elif transaction.type == Transaction.LT_TRANSACTION:
                    landOwners[transaction.input["land_id"]] = transaction.output["user_id"]
        return landOwners

    def getBlockFromHeight(self, height: int) -> Block | None:
        if not 0 <= height < len(self.chain):
            Log.error("Invalid block height")
            return None
        return self.chain[height]
    
    def getLastBlock(self) -> Block:
        return self.chain[-1]
    
    def getStakes(self) -> dict[str, int]:
        stakes = {}
        for block in self.chain:
            for transaction in block.data:
                if transaction.type == Transaction.ST_TRANSACTION:
                    nodeId = transaction.input["user_id"]
                    stake = transaction.input["amount"]
                    stakes[nodeId] = stakes[nodeId] + stake if nodeId in stakes else stake
        return stakes

    def getAges(self) -> dict[str, int]:
        ages = {}
        for i, block in enumerate(self.chain):
            nodeId = block.validator
            ages[nodeId] = i
        for nodeId in ages:
            ages[nodeId] = self.getLength() - ages[nodeId] - 1
        return ages

    def __str__(self) -> str:
        return "\n".join([colored("THE BLOCKCHAIN", "green", attrs=["bold"])] + [
            str(block) for block in self.chain
        ])
