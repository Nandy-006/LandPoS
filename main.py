import sys
import pickle

from network.network import Network
from utils.utils import Log

if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], "rb") as f:
                network = pickle.load(f)
            Log.info(f"Successfully loaded network from file {sys.argv[1]}")
            network.start()
        except:
            Log.error(f"Invalid file {sys.argv[1]}")
    else:
        network = Network()
        network.start()
