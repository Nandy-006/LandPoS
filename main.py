
from blockchain.blockchain import Blockchain
from network.network import Network


if __name__ == "__main__":
    
    network = Network()
    nodes = []

    nodes.append(network.registerNode('node1', 50))
    nodes.append(network.registerNode('node2', 150))
    nodes.append(network.registerNode('node3', 250))
    nodes.append(network.registerNode('node4', 350))
    nodes.append(network.registerNode('node5', 450))

    network.registerLand(nodes[0], 'land1')
    network.registerLand(nodes[1], 'land2')
    network.registerLand(nodes[2], 'land3')

    print(network.blockchain)