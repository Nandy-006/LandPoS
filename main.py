import sys
import pickle

from network.network import Network
from utils.utils import Log

if __name__ == "__main__":
    # if a file name is passed as an argument when the program is executed then the blockchain is loaded from that file
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], "rb") as f:
                network = pickle.load(f)
            Log.info(f"Successfully loaded network from file {sys.argv[1]}")
        except:
            Log.error(f"Invalid file {sys.argv[1]}")
    # if there is no file with the blockchain then a new blockchain is created
    else:
        network = Network()

    network.start()
