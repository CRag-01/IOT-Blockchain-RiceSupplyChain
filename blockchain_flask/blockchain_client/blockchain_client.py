"""
title           : blockchain_client.py
description     : A blockchain user backend implementation in Python that provides following features:
                  - wallet generator using public/private key encryption (based on RSA algorithm)
                  - making transaction with RSA encryption
                  - viewing transactions made
                  - exchanging coins for FIAT currency (e.g. EURO) in cryptoATM
author          : Roger Burek-Bors with instruction from Dr Zakwan Jaroucheh, the lecturer of <<Build a Blockchain &
                  Cryptocurrency using Python>> on Udemy
date_created    : 2020-12-22
version         : 0.2
usage           : The script runs locally therefore to simulate various nodes it needs a specified port to listen to.
                  You can run following instances:
                  - python blockchain_client.py
                  - python blockchain_client.py -p 8080
                  - python blockchain_client.py --port 8080
python_version  : 3.7
"""

import binascii
import Crypto
import Crypto.Random
import json
import requests
import urllib.request
from datetime import date, timedelta
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from collections import OrderedDict, defaultdict
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


class Ledger:

    def __init__(self):
        self.ledger = defaultdict(int)
        self.rates = defaultdict(int)

    def update_ledger(self, recipient_public_key, sender_public_key, amount):
        self.ledger[recipient_public_key] += int(amount)
        self.ledger[sender_public_key] -= int(amount)

    def withdrawal(self, public_key, amount):
        self.ledger[public_key] -= amount

    def reward_new_wallet(self, public_key):
        self.ledger[public_key] += 5

    def save_rates(self, all_rates):
        self.rates = all_rates


class Transaction:

    def __init__(self, sender_public_key, sender_private_key, recipient_public_key, amount):
        self.sender_public_key = sender_public_key
        self.sender_private_key = sender_private_key
        self.recipient_public_key = recipient_public_key
        self.amount = amount

    def to_dict(self):
        return OrderedDict({
            'sender_public_key': self.sender_public_key,
            'recipient_public_key': self.recipient_public_key,
            'amount': self.amount,
        })

    def sign_transaction(self):
        private_key = RSA.import_key(binascii.unhexlify(self.sender_private_key))
        signer = PKCS1_v1_5.new(private_key)
        h = SHA256.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')


# Running the ledger (it keeps all balances)
ledger = Ledger()

# Running a node in Flask
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate/transaction', methods=['POST'])
def generate_transaction():
    sender_public_key = request.form['sender_public_key']
    sender_private_key = request.form['sender_private_key']
    recipient_public_key = request.form['recipient_public_key']
    amount = request.form['amount']

    transaction = Transaction(sender_public_key, sender_private_key, recipient_public_key, amount)

    response = {'transaction': transaction.to_dict(),
                'signature': transaction.sign_transaction()}

    ledger.update_ledger(recipient_public_key, sender_public_key, int(amount))
    return jsonify(response), 200


@app.route('/generate/withdrawal', methods=['POST'])
def generate_withdrawal():
    your_public_key = request.form['your_public_key']
    your_private_key = request.form['your_private_key']
    amount = request.form['amount_withdraw']
    currency = request.form['currency_withdraw']

    response = {'your_public_key': your_public_key,
                'your_private_key': your_private_key,
                'amount': amount,
                'currency': currency}

    if int(response['amount']) <= ledger.ledger[response['your_public_key']]:
        ledger.withdrawal(your_public_key, int(amount))
        return jsonify(response), 200
    elif not ledger.ledger['public_key']:
        return 'Insufficient amount', 400
    else:
        return 'Insufficient amount', 400

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/make/transaction')
def make_transaction():
    return render_template('make_transaction.html')


@app.route('/view/transactions')
def view_transactions():
    return render_template('view_transactions.html')


@app.route('/view/balance')
def view_balance():
    return render_template('balance_exchange.html')


@app.route('/wallet/rates', methods=['GET'])
def get_rates():
    response = ledger.rates
    print(response)
    return response, 200


@app.route('/wallet/balance', methods=['POST'])
def check_balance():

    your_public_key = request.form['your_public_key1']
    coin_amount = ledger.ledger[your_public_key]

    # Check BTC-EUR rate (BTC is used as referencing coin)
    url = "https://api.bitbay.net/rest/trading/orderbook/BTC-EUR"
    headers = {'content-type': 'application/json'}
    response = requests.request("GET", url, headers=headers)
    response2 = response.json()
    btceur_exchange_rate = float(response2["buy"][0]['ra'])
    amount_in_eur = coin_amount * btceur_exchange_rate

    # Check EUR-PLN rate and apply to BTC (BTC is used as referencing coin)
    try:
        url = f'http://api.nbp.pl/api/exchangerates/rates/c/eur/{date.today()}/?format=json'
        with urllib.request.urlopen(url) as r:
            data = r.read()
        exchange = json.loads(data)['rates'][0]
        eurpln_exchange_rate = exchange['bid']
    except urllib.error.HTTPError:
        url = f'http://api.nbp.pl/api/exchangerates/rates/c/eur/{date.today() - timedelta(days=1)}/?format=json'
        with urllib.request.urlopen(url) as r:
            data = r.read()
        exchange = json.loads(data)['rates'][0]
        eurpln_exchange_rate = exchange['bid']
    amount_in_pln = coin_amount * btceur_exchange_rate * eurpln_exchange_rate

    response = {'coin_amount': coin_amount, 'amount_in_eur': round(amount_in_eur), 'amount_in_pln': round(amount_in_pln)}
    ledger.save_rates(response)

    return jsonify(response), 200


@app.route('/wallet/new')
def new_wallet():
    random_gen = Crypto.Random.new().read
    private_key = RSA.generate(1024, random_gen)
    public_key = private_key.publickey()

    response = {
        'private_key': binascii.hexlify(private_key.export_key(format('DER'))).decode('ascii'),
        'public_key': binascii.hexlify(public_key.export_key(format('DER'))).decode('ascii')
    }

    ledger.reward_new_wallet(response['public_key'])
    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8081, type=int, help="port to listen to")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)
