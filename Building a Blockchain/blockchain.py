import hashlib
import json
from time import time
import requests
from urllib.parse import urlparse


class Blockchain:
    def __init__(self):
        self.chain = []  # The BlockChain list
        self.current_transactions = []  # ToStoreTransactions
        self.nodes = set()  # Holds the list of nodes - to ensure addition of new nodes is idempotent

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash):
        # To Create a new Block
        """
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: <Optional> <str> Hash of the previous block
        :return: <dict> new Block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        # Appending a new transaction to the list of transactions
        """
        A new transaction to go into the next mined block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <str> Amount
        :return: <int> The index of the block that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        # Returns the last block in the chain
        return self.chain[-1]

    @staticmethod
    def hash(block):
        # Hashing a block
        """
        SHA-256 hash of the block
        :param block: <dict> Block
        :return: <str> Hashed form of the block
        """

        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        """
        Simple Proof of work algorithm:
            - Find a number p such that hash(pp') contains leading 4 0s, where p is the previous p`
            - p is the previous proof, and p' is the new proof
        :param last_block: <dict> last Block
        :return: <int>
        """
        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the proof: Does hash(last_proof, proof) contain 4 leading zeros?
        :param last_hash: The hash of the previous block
        :param last_proof:
        :param proof:
        :return: <bool> True if correct, else False
        """
        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == "0000"

    def register_node(self, address):
        """
        Adds a new node to the list of nodes
        :param address: <str> Address of the node. Eg. 'http://192.168.0.5:5000'
        :return: None
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid or not
        :param chain: <list> The blockchain
        :return: <bool> True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n----------------\n")

            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of WOrk is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        Consensus Algorithm which resolves conflicts by replacing our chain with the longest chain in the network
        :return: <bool> True if our chain was replaced, False if not.
        """
        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Verifying with all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False
