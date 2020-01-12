import json
import hashlib
import datetime
from flask import Flask, jsonify, render_template, redirect

# Class containing code for basic blockchain functionality
class blockchain:

    # Constructor to create the genesis (#1) block
    def __init__(self):
        # Creating an empty chain to store blocks
        self.chain = []
        # Variable to keep track of difficulty
        self.diff = 4
        # Vlaues for genesis (#1) block
        block = {
            "index" : len(self.chain) + 1,
            "prev_hash" : 0,
            "diff" : self.diff,
            "timestamp" : str(datetime.datetime.now()),
            "nonce" : 1,
        }
        # Getting hash
        block["hash"] = hashlib.sha256(("1" + str(block["index"]) + str(block["prev_hash"]) + str(block["timestamp"]) + str(block["diff"])).encode()).hexdigest()
        # Adding genesis block
        self.chain.append(block)
    
    # Function to create new block
    def new_block(self, prev_hash):
        # Creating a dict containing values for new block
        block = {
            "index" : len(self.chain) + 1,
            "prev_hash" : prev_hash,
            "diff" : self.diff
        }
        # Returning block
        return block

    # Function to add new block
    def add_block(self, block, timestamp, nonce, hash):
        # Creating a dict containg values to be appended to the chain
        block["timestamp"] = timestamp
        block["nonce"] = nonce
        block["hash"] = hash
        # Increasing difficulty after certian block height is reached
        # Adding one to chain length because it starts with 0
        if (len(self.chain ) + 1) % 1000 == 0:
            self.diff = self.diff + 1
        # Appending the new block
        self.chain.append(block)  
    
    # Function to find nonce for new block
    def p_o_w(self, prev_nonce, current_block):
        # Variable to store nonce
        nonce = 1
        # Variable to store the required number of 0s for nonce
        nonce_start = ""
        # Loop to find the required number of 0s
        for _ in range(self.diff) :
            nonce_start = nonce_start + "0"
        # Loop to find the nonce whose hash has required number of starting 0s
        while True:
            timestamp = str(datetime.datetime.now())
            hash = hashlib.sha256((str(nonce**2 - prev_nonce**2) + str(current_block["index"]) + str(current_block["prev_hash"]) + timestamp + str(current_block["diff"])).encode()).hexdigest()
            # Checking if hash start has desired number of 0s
            if hash[0:self.diff] == nonce_start:
                return timestamp, nonce, hash
            else:
                nonce = nonce + 1   
    
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
            hash = hashlib.sha256((str(int(self.chain[i + 1]["nonce"])**2 - int(self.chain[i]["nonce"])**2) + str(self.chain[i + 1]["index"]) + str(self.chain[i + 1]["prev_hash"]) + str(self.chain[i + 1]["timestamp"]) + str(self.chain[i + 1]["diff"])).encode()).hexdigest()
            # Checking if hash start has desired number of 0s
            if hash[0:diff] != start:
                return False
        return True


# Creating a flask web app
app = Flask(__name__)

# Creating the blockchain instance
demo_chain = blockchain()

# Default route
@app.route("/")
def default():
    return redirect("/chain")

# Route to mine a block
@app.route("/mine", methods = ["GET"])
def mine_block():
    # Getting the last block in chain
    prev_block = demo_chain.chain[-1]
    # Getting the new block for the chain
    block = demo_chain.new_block(prev_block["hash"])
    # Calculating the nonce for new block and getting timestamp and hash once nonce is found
    timestamp, nonce, hash = demo_chain.p_o_w(prev_block["nonce"], block)
    # Adding the new block
    demo_chain.add_block(block, timestamp, nonce, hash)
    # Dictionary to display message to the miner
    message = demo_chain.chain[-1]
    message["message"] = "You have successfully mined and appended a block"
    # Returning the mined block and message
    return render_template("mine.html", message = message)

# Route to get the complete chain
@app.route("/chain", methods = ["GET"])
def get_chain():
    # Dictionary to display message    
    message = {}
    message["chain"] = demo_chain.chain
    # Adding the lenght of chain
    message["length"] = len(demo_chain.chain)
    # Returnng the chain and its length
    return render_template("chain.html", message = message)  

# Route to check validity of the blockchain
@app.route("/valid", methods = ["GET"])
def is_valid():
    # Checking if the chain is valid
    validity = demo_chain.is_valid()
    # Storing time of checking validity
    timestamp = datetime.datetime.now()
    # Renderong the message page
    return render_template("valid.html", valid = validity, timestamp = timestamp)

# When route deosn't exist
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', timestamp = datetime.datetime.now()), 404