#! usr/bin/env python3

import hashlib
import time

class Block:

    def __init__(self, index, proof_no, prev_hash, data, timestamp=None):
        self.index = index
        self.proof_no = proof_no
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp or time.time()
    
    def calculate_hash(self):
    
    #calculates the cryptographic hash of every block

        block_of_string = f"{self.index}{self.proof_no}{self.prev_hash}{self.data}{self.timestamp}"

        return hashlib.sha256(block_of_string.encode()).hexdigest()

    def __repr__(self):
        return f"{self.index} - {self.proof_no} - {self.prev_hash} - {self.data} - {self.timestamp}"
        
    
class BlockChain:
    
    def __init__(self):
     # constructor method
        
        self.chain = []
        self.current_data = []
        self.nodes = set()
        self.construct_genesis()
    
    def construct_genesis(self):
        # constructs the initial block
        
        self.construct_block(proof_no=0, prev_hash=0)

    def construct_block(self, proof_no, prev_hash):
        # constructs a new block and adds it to the chain
        
        block = Block(
            index=len(self.chain),
            proof_no=proof_no,
            prev_hash=prev_hash,
            data=self.current_data)
        self.current_data = []

        self.chain.append(block)
        return block


    @staticmethod
    def check_validity(block, prev_block):
        # checks whether the blockchain is valid
        
        if prev_block.index + 1 != block.index:
            return False

        elif prev_block.calculate_hash != block.prev_hash:
            return False

        elif not BlockChain.verifying_proof(block.proof_no, prev_block.proof_no):
            return False

        elif block.timestamp <= prev_block.timestamp:
            return False

        return True

    def new_data(self, sender, recipient, quantity):
        # adds a new transaction to the data of the transactions
        
        self.current_data.append({
        'sender': sender,
        'recipient': recipient,
        'quantity': quantity
        })
        return True

    @staticmethod
    def construct_proof_of_work(last_proof):
        # protects the blockchain from attack
        
        '''this simple algorithm identifies a number f' such that hash(ff') contain 4 leading zeroes
         f is the previous f'
         f' is the new proof
        '''
    
        proof_no = 0
        while BlockChain.verifying_proof(proof_no, last_proof) is False:
            proof_no += 1

        return proof_no

    @staticmethod
    def verifying_proof(last_proof, proof):
        #verifying the proof: does hash(last_proof, proof) contain 4 leading zeroes?

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @property
    def last_block(self):
        # returns the last block in the chain
        return self.chain[-1]


    def block_mining(self, details_miner):

        self.new_data(
            sender="0",  #it implies that this node has created a new block
            receiver=details_miner,
            quantity=
            1,  #creating a new block (or identifying the proof number) is awarded with 1
        )

        last_block = self.latest_block

        last_proof_no = last_block.proof_no
        proof_no = self.proof_of_work(last_proof_no)

        last_hash = last_block.calculate_hash
        block = self.construct_block(proof_no, last_hash)

        return vars(block)

    def create_node(self, address):
        self.nodes.add(address)
        return True

    @staticmethod
    def obtain_block_object(block_data):
        #obtains block object from the block data

        return Block(
            block_data['index'],
            block_data['proof_no'],
            block_data['prev_hash'],
            block_data['data'],
            timestamp=block_data['timestamp'])




blockchain = BlockChain()

print("***Mining fccCoin about to start***")
print(blockchain.chain)

last_block = blockchain.last_block
last_proof_no = last_block.proof_no
proof_no = blockchain.construct_proof_of_work(last_proof_no)

blockchain.new_data(
    sender="0",  #it implies that this node has created a new block
    recipient="Quincy Larson",  #let's send Quincy some coins!
    quantity=
    1,  #creating a new block (or identifying the proof number) is awarded with 1
)

last_hash = last_block.calculate_hash
block = blockchain.construct_block(proof_no, last_hash)

print("***Mining fccCoin has been successful***")
print(blockchain.chain)
