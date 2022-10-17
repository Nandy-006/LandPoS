from os import stat
import pickle
from datetime import datetime
from termcolor import colored
from typing import TypedDict

from utils.utils import id

class InputType(TypedDict):
    user_id: str
    land_id: str
    amount: int

class OutputType(TypedDict):
    user_id: str
class Transaction:
    RC_TRANSACTION = 'Receive Coins'
    LD_TRANSACTION = 'Land Declaration'
    LT_TRANSACTION = 'Land Transfer'
    ST_TRANSACTION = 'Stake Increase'

    def __init__(self) -> None:
        self.id = id()
        self.type = ""
        self.timestamp = datetime.now()
        self.input: InputType = {"user_id": "", "land_id": "", "amount": 0}
        self.output: OutputType = {"user_id": ""}

    @staticmethod
    def newRCTransaction(receiver_id: str, amount: int) -> 'Transaction':
        input: InputType = {
            "user_id": receiver_id,
            "land_id": "",
            "amount": amount
        }
        output: OutputType = {
            "user_id": receiver_id
        }
        return Transaction.generateTransaction(Transaction.RC_TRANSACTION, input, output)

    @staticmethod
    def newLDTransaction(sender_id: str, land_id: str) -> 'Transaction':
        input: InputType = {
            "user_id": sender_id,
            "land_id": land_id,
            "amount": 0
        }
        output: OutputType = {
            "user_id": sender_id
        }
        return Transaction.generateTransaction(Transaction.LD_TRANSACTION, input, output)

    @staticmethod
    def newLTTransaction(sender_id: str, land_id: str, receiver_id: str) -> 'Transaction':
        input: InputType = {
            "user_id": sender_id,
            "land_id": land_id,
            "amount": 0
        }
        output: OutputType = {
            "user_id": receiver_id
        }
        return Transaction.generateTransaction(Transaction.LT_TRANSACTION, input, output)

    @staticmethod
    def newSTTransaction(sender_id: str, amount: int):
        input: InputType = {
            "user_id": sender_id,
            "land_id": "",
            "amount": amount
        }
        output: OutputType = {
            "user_id": sender_id
        }
        return Transaction.generateTransaction(Transaction.ST_TRANSACTION, input, output)

    @staticmethod
    def generateTransaction(type: str, input: InputType, output: OutputType):
        transaction = Transaction()
        transaction.type = type
        transaction.timestamp = datetime.now()
        transaction.input = input
        transaction.output = output
        return transaction
    
    @staticmethod
    def serialize(transaction):
        return pickle.dumps(transaction)
    
    def __repr__(self) -> str:
        return f"{colored(self.id, 'yellow')} [{colored(str(self.timestamp), 'cyan')}]: {str(self)}"
    
    def __str__(self) -> str:
        if self.type == Transaction.RC_TRANSACTION:
            return f"{self.input['user_id']} received {self.input['amount']} coins from the network"
        elif self.type == Transaction.LD_TRANSACTION:
            return f"{self.input['user_id']} owns {self.input['land_id']}"
        elif self.type == Transaction.LT_TRANSACTION:
            return f"{self.input['user_id']} transferred {self.input['land_id']} to {self.output['user_id']}"
        elif self.type == Transaction.ST_TRANSACTION:
            return f"{self.input['user_id']} staked {self.input['amount']} coins"
        return "Invalid transaction type"
