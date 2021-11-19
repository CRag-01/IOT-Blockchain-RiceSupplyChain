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

  - To start a blockchain node, go to blockchain folder and execute the command below: 
    ```bash 
      python blockchain.py -p 5000
    ```
  - To add a new node to blockchain, execute the command with a port that is not already used. E.g-
    ```bash 
      python blockchain.py -p 5001
    ```
   
    ```bash 
      python blockchain.py -p 5002
    ```
  - To start the blockchain client, go to blockchain_client folder and execute the command below: 
    ```bash 
      python blockchain_client.py -p 8080
    ```
  - To add a new blockchain client, execute the command with a port that is not already used. E.g- 
    ```bash
      python blockchain_client.py -p 8081
    ```
    ```bash
      python blockchain_client.py -p 8082
    ```
  - One can access the blockchain frontend and blockchain client dashboards from your browser by going to 
    ```bash
      localhost:5000
    ```
    ```bash
      localhost:8080
    ```




### Requirements/Extra Dependencies


```bash
  pip uninstall crypto
  pip uninstall pycrypto
  pip install pycryptodome
  pip install requests
  pip install flask
  pip install flask_cors
  pip install Flask-mail
  pip install twilio
```
