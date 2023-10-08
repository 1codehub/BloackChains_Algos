import hashlib
import json
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, proof, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.hash = hash

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(proof=100, previous_hash='0')  # Genesis block

    def create_block(self, proof, previous_hash):
        block = Block(len(self.chain) + 1, previous_hash, time.time(), self.current_transactions, proof, None)
        block.hash = self.calculate_hash(block)
        self.current_transactions = []
        self.chain.append(block)
        return block

    def create_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.last_block.index + 1

    def calculate_hash(self, block):
        block_string = json.dumps(vars(block), sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def proof_of_work(self, previous_proof):
        proof = 0
        while self.valid_proof(previous_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(previous_proof, proof):
        guess = f'{previous_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"  # Adjust the number of leading zeros for difficulty

    @property
    def last_block(self):
        return self.chain[-1]

# Create a new blockchain
blockchain = Blockchain()

# Example transactions
blockchain.create_transaction('Alice', 'Bob', 1)
blockchain.create_transaction('Bob', 'Charlie', 2)

# Mine a new block
previous_block = blockchain.last_block
previous_proof = previous_block.proof
proof = blockchain.proof_of_work(previous_proof)
blockchain.create_transaction('Miner', 'Alice', 0)  # Reward the miner
new_block = blockchain.create_block(proof, previous_block.hash)

# Print the blockchain
for block in blockchain.chain:
    print(f"Block #{block.index}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Transactions: {block.transactions}")
    print(f"Proof: {block.proof}")
    print(f"Hash: {block.hash}\n")
