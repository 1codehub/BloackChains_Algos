import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, data):
    value = str(index) + str(previous_hash) + str(timestamp) + str(data)
    return hashlib.sha256(value.encode()).hexdigest()

def create_genesis_block():
    return Block(0, "0", int(time.time()), "Genesis Block", calculate_hash(0, "0", int(time.time()), "Genesis Block"))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = int(time.time())
    hash = calculate_hash(index, previous_block.hash, timestamp, data)
    return Block(index, previous_block.hash, timestamp, data, hash)

# Create the blockchain and add the genesis block
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# Number of blocks to add to the chain
num_blocks_to_add = 10

# Add blocks to the blockchain
for i in range(num_blocks_to_add):
    new_data = f"Data for Block {i+1}"
    new_block = create_new_block(previous_block, new_data)
    blockchain.append(new_block)
    previous_block = new_block
    print(f"Block #{new_block.index} has been added to the blockchain!")
    print(f"Hash: {new_block.hash}\n")

# Verify the blockchain
def is_valid_blockchain(blockchain):
    for i in range(1, len(blockchain)):
        current_block = blockchain[i]
        previous_block = blockchain[i - 1]

        if current_block.hash != calculate_hash(current_block.index, previous_block.hash, current_block.timestamp, current_block.data):
            return False

    return True

print("Is the blockchain valid?", is_valid_blockchain(blockchain))
