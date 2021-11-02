# Block Chain for RiceSupply Chain and Agriculture Traceability

Project Under Development

### Folder: Building a BlockChain
Basic blockchain structure using Python to give us an understanding about - 
  - Mining
  - Transactions
  - Proof of Work
  - Consensus
 
 Authentication module - Twilio API used for Mobile Number verification.


### Steps to Run the Frontend 

How to run the flask application
This simulation runs on local computer therefore you need to start blockchain nodes and clients on different ports. You do need to worry about restricted resources on your local computer as there is CORS mechanism implemented.

  - To start a blockchain node, go to blockchain folder and execute the command below: python blockchain.py -p 5000
  - To add a new node to blockchain, execute the command with a port that is not already used. E.g., python blockchain.py -p 5001, python blockchain.py -p 5002, etc.
  - To start the blockchain client, go to blockchain_client folder and execute the command below: python blockchain_client.py -p 8080
  - To add a new blockchain client, execute the command with a port that is not already used. E.g., python blockchain_client.py -p 8081, python blockchain_client.py -p 8082, etc.
  - You can access the blockchain frontend and blockchain client dashboards from your browser by going to localhost:5000 and localhost:8080
