from network.network import Network

if __name__ == "__main__":
    network = Network()

    # Register users to the network
    network.run('connect alice 200')
    network.run('connect bob 150')

    # Declare lands for each user
    network.run('alice register land-1')
    network.run('bob register land-2')
    
    # Nodes stake coins to try and mint blocks
    network.run('alice stake 20')
    network.run('bob stake 100')

    # Two blocks have been minted, display balances, stakes and lands
    network.run('alice balance')
    network.run('bob balance')
    network.run('stakes')
    network.run('lands')

    # Node registers another land
    network.run('bob register land-3')

    # Buying and selling lands
    network.run('alice buy land-2 bob')
    network.run('alice sell land-1 bob')

    # View transactions in pool
    network.run('pool')

    # New node joins the network
    network.run('connect charlie 150')

    # Display nodes in the network
    network.run('nodes')

    # Node tries to register a land that someone already owns
    network.run('charlie register land-1')

    # Node stakes when their balance is 0
    # Balance for charlie is not 150 because the transaction is not in the chain yet
    network.run('charlie stake 100')

    # Two more blocks have been minted, display balances, stakes and lands
    network.run('alice balance')
    network.run('bob balance')
    network.run('charlie balance')
    network.run('stakes')
    network.run('lands')

    # Node stakes more than their balance
    network.run('charlie 200')
    
    # Node who doesn't own the land tries to sell it
    network.run('alice sell land-1 charlie')

    # Node sells land
    network.run('bob sell land-1 charlie')

    # Node stakes
    network.run('charlie stake 100')

    # Display transaction history of a land
    network.run('history land-1')

    # Display lands
    network.run('lands')

    # Display blockchain
    network.run('blockchain')

    # Get details of third block (block id = 2)
    network.run('block 2')

    # Save network state
    network.run('save')

    # Stop network
    network.run('stop')
