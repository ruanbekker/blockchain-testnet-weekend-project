# blockchain-testnet-weekend-project
Weekend Project to tinker with Blockchain and Transactions

## About

I wanted to host different cryptocurrency full nodes running on the testnet's with wallets enabled on my raspberry pi's:

- node1: bitcoin
- node2: litecoin
- node3: dogecoin
- node4: dash
- node5: groestlcoin

Then when all of them were synced (with 2GB pruned to save disk space) create wallets and addresses for each cryptocurrency, then start cpu mining using `generatetoaddress` and build up some funds.

During this process I interacted with the json-rpc interface and used Pushgateway and Prometheus, to graph dashboards on Grafana of the incoming balances over time as well as the current balances:

![image](https://user-images.githubusercontent.com/567298/135833192-2750bae4-245c-4bf2-9d37-6515cd92f5ba.png)

After that I interacted with the `walletnotify` option to notify myself everytime I get a incoming transaction, where the flow would be:

- Wallet notify captures the transaction id with `%s` 
- Python script interacts with the blockchain to determine if the tx has more than 2 confirmations
- Once it has enough confirmations, I get the info such as amount, balance, etc then I log it to MongoDB
- Once I have written the transaction details to MongoDB I send myself a notification on Pushover on my phone
- I then decided to develop a small Python Flask WebUI that pulls the information from MongoDB

More information on how i've setup these nodes, scripts and code will be published to this repo.

WIP
