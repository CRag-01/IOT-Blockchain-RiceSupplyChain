import binascii
import Crypto
import Crypto.Random
import json
import os
import requests
import urllib.request
from dotenv.main import load_dotenv
from twilio.rest import Client
from datetime import date, timedelta
from flask import *
# from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
from collections import OrderedDict, defaultdict
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from email_otp import *

# twilio configs
load_dotenv()

account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")
service = os.getenv("service")

client = Client(account_sid, auth_token)

# Ledger Configs


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
        private_key = RSA.import_key(
            binascii.unhexlify(self.sender_private_key))
        signer = PKCS1_v1_5.new(private_key)
        h = SHA256.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')


# Running the ledger (it keeps all balances)
ledger = Ledger()

# Running a node in Flask
app = Flask(__name__)
CORS(app)
app.secret_key = 'EmailAuthenticationByCRAG2021'

# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route('/wallet')
def wallet():
    return render_template('index.html', data=session['temp_dict'])


@app.route('/signup', methods=['POST'])
def submit():
    name = request.form['name']
    kishan_id = request.form['kishan_id']
    aadhaar_no = request.form['aad_no']
    print(aadhaar_no)
    email = request.form['email']
    phone = request.form['phone_no']
    verification = client.verify \
        .services(service) \
        .verifications \
        .create(to=phone, channel='sms')

    current_otp = sendEmailVerificationRequest(receiver=email)
    session['temp_dict']={
        'name': name,
        'kishan_id': kishan_id,
        'aadhaar_no': aadhaar_no,
        'email': email,
        'phone': phone,
    }
    #     'id': session['kishan_id'],
    #     'aadhaar_no': session['aad_no'],
    #     'email': session['email'],
    #     'phone': session['phone_no'],
    # }
    session['current_otp'] = current_otp
    session['phone_number'] = phone
    print(verification.status)
    print(current_otp)
    # print(verification2.status)
    print(name, kishan_id, aadhaar_no, email, phone)
    response = {'email': email,
                'phone': phone,
                'status': verification.status}
    # return redirect(request.referrer)
    # return render_template('signup2.ejs')
    return response, 200


@app.route('/verify', methods=['POST'])
def verify():
    phone_otp = request.form['phone_no2']
    email_otp = request.form['email_id2']
    current_phone_number = session['phone_number']
    print(phone_otp, email_otp)
    verification = client.verify \
        .services(service) \
        .verification_checks \
        .create(to=current_phone_number, code=phone_otp)
    print(verification.status)
    current_user_otp = session['current_otp']
    if int(current_user_otp) == int(email_otp) and verification.status == 'approved':
        response = {'status_email': 1,
                    'status_phone': 1}

    else:
        response = {'message': 'Invalid OTPs'}
        return response, 400
    return response, 200


@app.route('/generate/transaction', methods=['POST'])
def generate_transaction():
    sender_public_key = request.form['sender_public_key']
    sender_private_key = request.form['sender_private_key']
    recipient_public_key = request.form['recipient_public_key']
    amount = request.form['amount']

    transaction = Transaction(
        sender_public_key, sender_private_key, recipient_public_key, amount)

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


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/signupPage')
def signup():
    return render_template('signup2.ejs')


@app.route('/details')
def details():
    return render_template('details.html')


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

    response = {'coin_amount': coin_amount, 'amount_in_eur': round(
        amount_in_eur), 'amount_in_pln': round(amount_in_pln)}
    ledger.save_rates(response)

    return jsonify(response), 200


@app.route('/wallet/new')
def new_wallet():
    random_gen = Crypto.Random.new().read
    private_key = RSA.generate(1024, random_gen)
    public_key = private_key.publickey()

    session['public_key']=binascii.hexlify(public_key.export_key(format('DER'))).decode('ascii')

    response = {
        'private_key': binascii.hexlify(private_key.export_key(format('DER'))).decode('ascii'),
        'public_key': binascii.hexlify(public_key.export_key(format('DER'))).decode('ascii')
    }

    ledger.reward_new_wallet(response['public_key'])
    return jsonify(response), 200

@app.route('/addToNode' ,  methods=['POST'])
def addToNode():
    response={
        session['public_key']:session['temp_dict']
    }
    return response, 200

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8081,
                        type=int, help="port to listen to")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)
