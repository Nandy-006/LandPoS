import typing
import pickle
from datetime import datetime
from utils.utils import Log, id

class Transaction:
    LD_TRANSACTION = 'Land Declaration'
    LT_TRANSACTION = 'Land Transfer'
    ST_TRANSACTION = 'Stake Increase'

    def __init__(self):
        self.id = id()
        self.type = ""
        self.timestamp = datetime.now()
        self.input = {"user_id": "", "land_id": "", "amount": 0}
        self.output = {"user_id": ""}

    @staticmethod
    def newLDTransaction(sender_id: str, land_id: str) -> 'Transaction':
        input = {
            "user_id": sender_id,
            "land_id": land_id,
            "amount": 0
        }
        output = {
            "user_id": sender_id
        }
        return Transaction.generateTransaction(Transaction.LD_TRANSACTION, input, output)

    @staticmethod
    def newLTTransaction(sender_id: str, land_id: str, receiver_id: str) -> 'Transaction':
        input = {
            "user_id": sender_id,
            "land_id": land_id,
            "amount": 0
        }
        output = {
            "user_id": receiver_id
        }
        return Transaction.generateTransaction(Transaction.LT_TRANSACTION, input, output)

    @staticmethod
    def newSTTransaction(sender_id: str, amount: int):
        input = {
            "user_id": sender_id,
            "land_id": "",
            "amount": amount
        }
        output = {
            "user_id": sender_id
        }
        return Transaction.generateTransaction(Transaction.ST_TRANSACTION, input, output)

    @staticmethod
    def generateTransaction(type: str, input, output):
        transaction = Transaction()
        transaction.type = type
        transaction.timestamp = datetime.now()
        transaction.input = input
        transaction.output = output
        return transaction
    
    @staticmethod
    def serialize(transaction):
        return pickle.dumps(transaction)
    
    def __str__(self) -> str:
        if self.type == Transaction.LD_TRANSACTION:
            return f"{self.id} [{self.timestamp}]: {self.input['user_id']} owns {self.input['land_id']}"
        elif self.type == Transaction.LT_TRANSACTION:
            return f"{self.id} [{self.timestamp}]: {self.input['user_id']} transferred {self.input['land_id']} to {self.output['user_id']}"
        elif self.type == Transaction.ST_TRANSACTION:
            return f"{self.id} [{self.timestamp}]: {self.input['user_id']} staked {self.input['amount']} coins"
        return "Invalid transaction type"
