# Blockchain in Python

This is simulation of a blockchain network and clients written in Python and HTML based on Udemy tutorial.
It consist of Python scripts that run backend of the blockchain network and clients, as well as HTML instances that display user interface (frontend).

project_root/

│

├── blockchain/              # Blockchain network source code (Backend & Frontend)

│ ├── static/                # Css and Js for Frontend

│ ├── templates/             # HTML for Frontend

│ └── blockchain.py          # Python script for Backend

├── blockchain_client/       # Blockchain user source code (Backend & Frontend)

│ ├── static/                # Css and Js for Frontend

│ ├── templates/             # HTML for Frontend

│ └── blockchain_client.py   # Python script for Backend

└── README


## Dependencies
- works with Python 3.7
- need to install:
  - binascii
  - hashlib
  - json
  - requests
  - flask
  - flask_cors
  - collections
  - time
  - Crypto
  - uuid
  - urllib

## How to run blockchain_py
Remember, this simulation runs on local computer therefore you need to start blockchain nodes and clients on different ports. You do need to worry about restricted resources on your local computer as there is CORS mechanism implemented.
1. To start a blockchain node, go to blockchain folder and execute the command below: python blockchain.py -p 5000
2. To add a new node to blockchain, execute the command with a port that is not already used. E.g., python blockchain.py -p 5001, python blockchain.py -p 5002, etc.
3. To start the blockchain client, go to blockchain_client folder and execute the command below: python blockchain_client.py -p 8080
4. To add a new blockchain client, execute the command with a port that is not already used. E.g., python blockchain_client.py -p 8081, python blockchain_client.py -p 8082, etc.
5. You can access the blockchain frontend and blockchain client dashboards from your browser by going to localhost:5000 and localhost:8080

## Task list
- [x] Finish basic blockchain network and users simulation
- [x] Implement coins exchange for FIAT currency (e.g. EURO) in cryptoATM

**This is just a prototype solution and need some fixing with regard to security.**
