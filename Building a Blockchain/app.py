
from uuid import uuid4
from flask import Flask, jsonify, request

from Authentication import Auth_Twilio

import blockchain

# Instantiate our node
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
bc = blockchain.Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # Running the proof of work algorithm to get the next proof..
    last_block = bc.last_block
    proof = bc.proof_of_work(last_block)

    # We must receive a reward for finding this proof.
    # The sender is "0" signify that this node has mined a new coin.

    bc.new_transaction(
        sender=0,
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = bc.hash(last_block)
    block = bc.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],

    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json(force=True)
    # Check whether the required fields are present in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = bc.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': bc.chain,
        'length': len(bc.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json(force=True)
    nodes = values.get('nodes')
    phone_num = values.get('phone')
    authentication_message = Auth_Twilio.phone_authentication(phone_num)
    append_message = ""

    if authentication_message == 'approved':
        append_message = "Phone verification successful"
    else:
        append_message = "Phone verification unsucessful"

    if nodes is None:
        return "Error: Please supply a valid list of nodes.", 400

    for node in nodes:
        bc.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(bc.nodes),
        'authentication_status': append_message
    }

    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = bc.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': bc.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': bc.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
