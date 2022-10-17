from hashlib import sha256
from blockchain.transaction import Transaction

# A MerkleTree is a tree in which every leaf node is a hash of a data block and every inner node is the hash of its child nodes
# This class provides a function to get the Merkler Root given a list of transactions
class MerkleTree:
    @staticmethod
    def getMerkleRoot(transactionList: list[Transaction]) -> str:
        hashList = [sha256(Transaction.serialize(transaction)).hexdigest() for transaction in transactionList]
        while len(hashList) > 1:
            nextHashList = []
            if len(hashList) % 2 == 1:
                hashList.append(hashList[-1])
            for i in range(0, len(hashList), 2):
                nextHashList.append(sha256(str(hashList[i] + hashList[i + 1]).encode('utf-8')).hexdigest())
            hashList = nextHashList

        return hashList[0]
