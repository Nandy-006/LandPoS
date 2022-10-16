from blockchain.block import Block
from blockchain.transaction import Transaction
from utils.utils import Log

class Blockchain:
    def __init__(self) -> None:
        self.chain = [Block.genesis()]

    def addBlock(self, block: Block) -> Block | None:
        if block.previousBlockHash == Block.hashBlock(self.getLastBlock()):
            self.chain.append(block)
            print("Added new block")
            print(block)
        else:
            Log.error("Invalid block")
            return None
        return block
    
    def getLength(self) -> int:
        return len(self.chain)

    def getLandHistory(self, landId: str) -> list[Transaction]:
        landHistory = []
        for block in self.chain:
            for transaction in block.data:
                if transaction.type in [Transaction.LD_TRANSACTION, Transaction.LT_TRANSACTION] and transaction.input['land_id'] == landId:
                    landHistory.append(transaction)

        return landHistory
    
    def getTransaction(self, transactionId: str) -> Transaction | None:
        for block in self.chain:
            for transaction in block.data:
                if transaction.id == transactionId:
                    return transaction

        Log.error("Transaction does not exist")
        return

    def getLandOwner(self, landId: str) -> str | None:
        history = self.getLandHistory(landId)
        if len(history) == 0:
            return None
        return history[-1].output['user_id']

    def getBlockFromHeight(self, height: int) -> Block | None:
        if height >= len(self.chain):
            return None
        return self.chain[height]
    
    def getLastBlock(self) -> Block:
        return self.chain[-1]

    def __str__(self) -> str:
        return "\n\n".join(["BLOCKCHAIN"] + [
            str(block) for block in self.chain
        ])
            
