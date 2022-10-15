from hashlib import sha256
from blockchain.transaction import Transaction

class MerkleTree:
    @staticmethod
    def getMerkleRoot(transactionList: list[Transaction]) -> str:
        hashList = [sha256(Transaction.serialize(transaction)).hexdigest() for transaction in transactionList]
        while len(hashList) > 1:
            nextHashList = []
            if len(hashList) % 2 == 1:
                hashList.append(hashList[-1])
            print(hashList)
            for i in range(0, len(hashList), 2):
                nextHashList.append(sha256(str(hashList[i] + hashList[i + 1]).encode('utf-8')).hexdigest())
            hashList = nextHashList

        return hashList[0]
