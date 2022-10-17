from network.network import Network

if __name__ == "__main__":
    
    network = Network()

    network.registerNode("3000", 100)
    network.registerNode("3001", 200)

    network.run("3000 register node")
    network.run("3001 register node")
    network.run("3001 stake 50")
