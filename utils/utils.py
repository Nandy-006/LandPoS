import uuid
from termcolor import colored

class Command:
    def __init__(self, key: str, syntax:str, help: str) -> None:
        self.key = key
        self.syntax = syntax
        self.help = help

class Log:
    @staticmethod
    def info(message: str, type: str = 'INFO', nodeId: str = "", end="\n") -> None:
        infoMessage = f"{colored(type, 'blue', attrs=['bold'])}: {message}"
        if nodeId != "":
            infoMessage = f"[{colored(nodeId, 'yellow', attrs=['bold'])}] " + infoMessage
        print(infoMessage, end=end)
    
    @staticmethod
    def error(message: str) -> None:
        print(f"{colored('ERROR', 'red', attrs=['bold'])}: {message}")

def id() -> str:
    return str(uuid.uuid4())
