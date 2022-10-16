import uuid
from termcolor import colored

class Command:
    def __init__(self, key: str, help: str) -> None:
        self.key = key
        self.help = help
    
    def __str__(self) -> str:
        return f"{self.key} - {self.help}"

class Log:
    @staticmethod
    def info(message: str, type: str = 'INFO') -> None:
        print(f"{colored(type, 'blue', attrs=['bold'])}: {message}")
    
    @staticmethod
    def error(message: str) -> None:
        print(f"{colored('ERROR', 'red', attrs=['bold'])}: {message}")

def id() -> str:
    return str(uuid.uuid4())
