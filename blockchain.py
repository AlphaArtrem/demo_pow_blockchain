import json
import hashlib
import datetime
from flask import Flask, jsonify

# Class containing code for basic blockchain functionality
class blockchain:

    # Constructor to create the genesis (#1) block
    def __init__(self):
        # Creating an empty chain to store blocks
        self.chain = []
        # Variable to keep track of difficulty
        self.diff = 4
        # Adding genesis (#1) block
        self.add_block(nonce = 1, prev_hash = "0")
        ## Creating hash of genesis block
        self.chain[0]["hash"] = self.block_hash(self.chain[0])
    
    # Function to add new block
    def add_block(self, nonce, prev_hash):
        # Creating a dict containg values to be appended to the chain
        block = {
            "index" : len(self.chain) + 1,
            "nonce" : nonce,
            "prev_hash" : prev_hash,
            "timestamp" : str(datetime.datetime.now()),
            "diff" : self.diff
        }
        ## Creating hash of current block
        block["hash"] = self.block_hash(block)
        # Increasing difficulty after certian block height is reached
        # Adding one to chain length because it starts with 0
        if (len(self.chain ) + 1) % 1000 == 0:
            self.diff = self.diff + 1
        # Appending the new block
        self.chain.append(block)
    
    # Function to find nonce for new block
    def p_o_w(self, prev_nonce):
        # Variable to store nonce
        nonce = 1
        # Variable to store the required number of 0s for nonce
        nonce_start = ""
        # Loop to find the required number of 0s
        for _ in range(self.diff) :
            nonce_start = nonce_start + "0"
        # Loop to find the nonce whose hash has required number of starting 0s
        while True:
            hash = hashlib.sha256(str(nonce**2 - prev_nonce**2).encode()).hexdigest()
            # Checking if hash start has desired number of 0s
            if hash[0:self.diff] == nonce_start:
                return nonce
            else:
                nonce = nonce + 1   
    
    # Function to calculate hash of block in json format
    def block_hash(self, block):
        # Converting the block from dictionary to json format
        # sort_keys = True , so that values of block are sorted using keys of dictionary
        en_block = json.dumps(block, sort_keys = True).encode()
        # Taking hash of encoded block and returning it
        hash = hashlib.sha256(en_block).hexdigest()
        return hash
    
    # Function to check if chain is valid    
    def is_valid(self):
        # Run the loop untill end of chain is reached
        for i in range(len(self.chain) - 1):
            # Check if the previous hash of current block is equal to hash of previous block
            if self.chain[i + 1]["prev_hash"] != self.chain[i]["hash"]:
                return False
            # Getting difficulty of current block
            diff = int(self.chain[i + 1]["diff"])
            # Storing the required number of 0s in the start of hash of nonce for current block
            start = ""
            for _ in range(diff):
                start = start + "0"
            # Calculating hash for nonce of current block
            hash = hashlib.sha256(str(int(self.chain[i + 1]["nonce"])**2 - int(self.chain[i]["nonce"])**2).encode()).hexdigest()
            # Checking if hash start has desired number of 0s
            if hash[0:diff] != start:
                return False
        return True


a = blockchain()
for _ in range(10):
    a.add_block(int(a.p_o_w(a.chain[-1]["nonce"])), a.chain[-1]["hash"])
for i in range(len(a.chain)):
    print(a.chain[i])
    print("\n")
print(a.is_valid())