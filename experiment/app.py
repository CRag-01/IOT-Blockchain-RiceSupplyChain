#flask app
from os import name
from flask import *
from flask_cors import CORS
from flask_session import Session


app = Flask(__name__)
CORS(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/profile')
# def profile():
#     return render_template('profile.html')

@app.route('/signup' ,  methods=['POST'])
def signup():
    session['name']=request.form['name']
    session['kishan_id']=request.form['kishan_id']
    session['aadhaar_no']=request.form['aad_no']
    session['email']=request.form['email']
    session['phone']=request.form['phone_no']
    email = session['email']
    phone = session['phone']
    print(email, phone)
    response = {'email': email,
                'phone': phone}
    return response, 200

@app.route('/profilerequest')
def profilerequest():
    response={'name': session['name'],
                'kishan_id': session['kishan_id'],
                'aadhaar_no': session['aadhaar_no'],
                'email': session['email'],
                'phone': session['phone']}
    return render_template('profile.html', Response=response)


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8081,
                        type=int, help="port to listen to")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)