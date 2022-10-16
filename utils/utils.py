import uuid
from termcolor import colored

class Command:
    def __init__(self, key: str, syntax:str, help: str) -> None:
        self.key = key
        self.syntax = syntax
        self.help = help

class Log:
    @staticmethod
    def info(message: str, type: str = 'INFO') -> None:
        print(f"{colored(type, 'blue', attrs=['bold'])}: {message}")
    
    @staticmethod
    def error(message: str) -> None:
        print(f"{colored('ERROR', 'red', attrs=['bold'])}: {message}")

def id() -> str:
    return str(uuid.uuid4())
