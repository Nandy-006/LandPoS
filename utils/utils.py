import uuid
from simple_chalk import blue, red

class Command:
    def __init__(self, key: str, help: str) -> None:
        self.key = key
        self.help = help
    
    def __str__(self) -> str:
        return f"{self.key} - {self.help}"

class Log:
    @staticmethod
    def info(message: str) -> None:
        print(f"{blue.bold('INFO')}: {message}")
    
    @staticmethod
    def error(message: str) -> None:
        print(f"{red.bold('ERROR')}: {message}")

def id() -> str:
    return str(uuid.uuid4())
