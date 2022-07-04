# DASH JSON RPC Guide

This guide will show the basics on how to get your account setup and create a dash address so that we can send funds to your account.

## Pre-Requisites

Before you can continue you must have dash running and fully synced, the guide to do that can be found below:

- [DASH Full Node Setup on ARM](https://github.com/ruanbekker/blockchain-testnet-weekend-project/blob/main/nodes-setup/dash-testnet-arm.md)

## Ensure Dash is Running

Ensure that the dogecoin daemon is running, either using systemd:

```bash
$ sudo systemctl is-active dashd
active
```

or using netstat to see if the port that we assigned `18332` is listening:

```bash
$ sudo netstat -tulpn | grep dashd
tcp        0      0 127.0.0.1:19998         0.0.0.0:*               LISTEN      22206/dashd
tcp        0      0 0.0.0.0:19999           0.0.0.0:*               LISTEN      22206/dashd
tcp6       0      0 :::19999                :::*                    LISTEN      22206/dashd
```

## JSON RPC

The following calls will interact with the json-rpc interface

First get the jsonrpc user and password:

```
$ cat /home/crypto/.dashcore/dash.conf | grep -E '(rpcuser|rpcpassword)'
rpcuser=user
rpcpassword=pass
```

Because this is a test environment, we can set the username and password as an environment variable:

```
# the user and password might differ on your setup
$ export authstring="user:pass"
```

### Wallet Interaction

Create a wallet:

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "tutorial", "method": "createwallet", "params": ["test"]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/
{"result":{"name":"test","warning":""},"error":null,"id":"tutorial"}
```

List wallets:

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "tutorial", "method": "listwallets", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:19998/
{"result":["test"],"error":null,"id":"tutorial"}
```

If we inspect the `dash.conf` we will notice that we don't have the wallet loaded in our config:

```
$ cat /home/crypto/.dashcore/dash.conf | grep -c 'wallet='
0
```

But since we created the wallet, we can see the `wallet.dat` in our data directory:

```
$ find /blockchain/dashcore/data -type f -name wallet.dat
/blockchain/dashcore/data/testnet3/wallets/test/wallet.dat
```

Let's restart the `dashd` service and see if we can still list our wallet, first restart the service:

```
$ sudo systemctl restart dashd
```

Then wait a couple of seconds and list the wallets:

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "tutorial", "method": "listwallets", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:19998/
{"result":[],"error":null,"id":"tutorial"}
```

As you can see it's not loaded, due to it not being in the config. Let's update our config `/home/crypto/.dashcore/dash.conf`, and restart the service: 

```
# more wallets can be referenced by using another wallet= config
[test]
wallet=test
# which corresponds to datadir + walletdir
# /blockchain/dashcore/data/testnet3/wallets/wallet/wallet.dat
# /blockchain/dashcore/data/testnet3/wallets/wallet/db.log
```

When I restarted the `dashd` service, I checked the logs with `journalctl -fu dashd`, and I could see the wallet has been loaded:

```
Jul 04 13:50:04 node4.infra.ruan.dev dashd[28944]: 2022-07-04T11:50:04Z init message: Loading wallet...
Jul 04 13:50:04 node4.infra.ruan.dev dashd[28944]: 2022-07-04T11:50:04Z nKeysLeftSinceAutoBackup: 1000
```

When I list the wallets again:

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "tutorial", "method": "listwallets", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:19998/
{"result":["test"],"error":null,"id":"tutorial"}
```

Now that the wallet has been loaded, we can get wallet info:

```
$ curl -s -u "$authstring" -d '{"jsonrpc": "1.0", "id": "tutorial", "method": "getwalletinfo", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test | jq .
{
  "result": {
    "walletname": "test",
    "walletversion": 120200,
    "balance": 0,
    "coinjoin_balance": 0,
    "unconfirmed_balance": 0,
    "immature_balance": 0,
    "txcount": 0,
    "timefirstkey": 1656935102,
    "keypoololdest": 1656935102,
    "keypoolsize": 1000,
    "keys_left": 1000,
    "paytxfee": 0,
    "scanning": false
  },
  "error": null,
  "id": "tutorial"
}
```

Create another wallet, named `test-wallet`:

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "createwallet", "params": ["test-wallet"]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/
{"result":{"name":"test-wallet","warning":""},"error":null,"id":"curltest"}
```

After we created our wallet, list the wallets again:

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "listwallets", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:19998/
{"result":["wallet","test-wallet"],"error":null,"id":"curltest"}
```

Now that we have 2 wallets, we need to specify the wallet name, when we want to do a `getwalletinfo` method for a specific wallet, `test-wallet` in this case:

```
$ curl -s -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "getwalletinfo", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet | jq .
{
  "result": {
    "walletname": "test-wallet",
    "walletversion": 169900,
    "format": "bdb",
    "balance": 0,
    "unconfirmed_balance": 0,
    "immature_balance": 0,
    "txcount": 0,
    "keypoololdest": 1623333495,
    "keypoolsize": 1000,
    "hdseedid": "x",
    "keypoolsize_hd_internal": 1000,
    "paytxfee": 0,
    "private_keys_enabled": true,
    "avoid_reuse": false,
    "scanning": false,
    "descriptors": false
  },
  "error": null,
  "id": "curltest"
}
```

In order to understand where the data resides for our `test-wallet`, we can use `find`:

```
$ find /blockchain/ -type f -name wallet.dat | grep test-wallet
/blockchain/dashcore/data/testnet3/wallets/test-wallet/wallet.dat

$ find /blockchain/ -type f -name db.log | grep test-wallet
/blockchain/dashcore/data/testnet3/wallets/test-wallet/db.log
```

Include the wallet name in the config located at `/home/ruan/.dashcore/dash.conf`:

```
[test]
wallet=wallet
wallet=test-wallet
```

Then restart dashd:

```
$ sudo systemctl restart dashd
```

Now list our wallets again, and you should see they are being read from config and the wallets will persist if your node restarts:

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "listwallets", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:19998/
{"result":["wallet","test-wallet"],"error":null,"id":"curltest"}
```

To backup a wallet, the `test-wallet` in this case:

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "backupwallet", "params": ["test-wallet_bak.dat"]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet
{"result":null,"error":null,"id":"curltest"}
````

To check where the file was backed up:

```
$ find /blockchain/ -name test-wallet_bak.dat
/blockchain/dashcore/data/test-wallet_bak.dat
```

### Addresses

At this moment we have wallets, but we don't have any addresses associated to those wallets, we can verify this by listing wallet addresses using the `getaddressesbylabel` and passing a empty label as new addresses gets no labels assigned by default.

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "getaddressesbylabel", "params": [""]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet
{"result":{"":{"purpose":"receive"}},"error":null,"id":"curltest"}
```

Let's generate a new address for our `test-wallet`:

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "getnewaddress", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet
{"result":"tb1qr66hw59k958xrz008n679p8r9n2y7mjfr3tsjc","error":null,"id":"curltest"}
```

As you can see our address for `test-wallet` is `tb1qr66hw59k958xrz008n679p8r9n2y7mjfr3tsjc`, note that you can have multiple addresses per wallet.

To get address information for the wallet by using the `getaddressinfo` method and passing the wallet address as the parameter:

```
$ curl -s -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "getaddressinfo", "params": ["tb1qr66hw59k958xrz008n679p8r9n2y7mjfr3tsjc"]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet | jq .
{
  "result": {
    "address": "tb1qr66hw59k958xrz008n679p8r9n2y7mjfr3tsjc",
    "scriptPubKey": "x",
    "ismine": true,
    "solvable": true,
    "desc": "wpkh([05c34822/0'/0'/0']x)#x3x5vu3t",
    "iswatchonly": false,
    "isscript": false,
    "iswitness": true,
    "witness_version": 0,
    "witness_program": "1eb57750b62dxe284e32cd44f6e49",
    "pubkey": "023a1250c0d44751b604656x649357b5e530b9f8500f03ab5b",
    "ischange": false,
    "timestamp": 1623333494,
    "hdkeypath": "m/0'/0'/0'",
    "hdseedid": "x",
    "hdmasterfingerprint": "x",
    "labels": [
      ""
    ]
  },
  "error": null,
  "id": "curltest"
}
```

As before, we can view the address by label, to view the address for your wallet, we will now see our address:

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "getaddressesbylabel", "params": [""]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet
{"result":{"tb1qr66hw59k958xrz008n679p8r9n2y7mjfr3tsjc":{"purpose":"receive"}},"error":null,"id":"curltest"}
```

Get available wallet balance with at least 6 confirmations:

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "getbalance", "params": ["*", 6]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet
{"result":0.00000000,"error":null,"id":"curltest"}
```

Get balances (all balances) for the `test-wallet` wallet:

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "getbalances", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet
{"result":{"mine":{"trusted":0.00000000,"untrusted_pending":0.00000000,"immature":0.00000000}},"error":null,"id":"curltest"}
```

Create a new address:

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "getnewaddress", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet
{"result":"tb1qa7e0mmgsul6pnxhzx7rw49y9qf35enqqra47hh","error":null,"id":"curltest"}
```

List all addresses for the wallet:

```
# by default new addresses has no labels, therefore it returns both
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "getaddressesbylabel", "params": [""]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet
{"result":{"tb1qr66hw59k958xrz008n679p8r9n2y7mjfr3tsjc":{"purpose":"receive"},"tb1qa7e0mmgsul6pnxhzx7rw49y9qf35enqqra47hh":{"purpose":"receive"}},"error":null,"id":"curltest"}
```

### Labelling Addresses

Now we can label addresses on wallets, to label the first address as "green":

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "setlabel", "params": ["tb1qr66hw59k958xrz008n679p8r9n2y7mjfr3tsjc", "green"]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet
{"result":null,"error":null,"id":"curltest"}
```

Label the new address as "blue":

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "setlabel", "params": ["tb1qa7e0mmgsul6pnxhzx7rw49y9qf35enqqra47hh", "blue"]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet
{"result":null,"error":null,"id":"curltest"}
```

Now we can list addresses for our wallet by the label, "blue" in this example:

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "getaddressesbylabel", "params": ["blue"]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet
{"result":{"tb1qa7e0mmgsul6pnxhzx7rw49y9qf35enqqra47hh":{"purpose":"receive"}},"error":null,"id":"curltest"}
```

List addresses for our wallet by the label "green":

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "getaddressesbylabel", "params": ["green"]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet
{"result":{"tb1qr66hw59k958xrz008n679p8r9n2y7mjfr3tsjc":{"purpose":"receive"}},"error":null,"id":"curltest"}
```

Create another address for our test-walet:

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "getnewaddress", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet
{"result":"tb1qunk223dztk2j2zqswleyenwu3chfqt642vrp8z","error":null,"id":"curltest"}
```

Set the new address to the green label:

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "setlabel", "params": ["tb1qunk223dztk2j2zqswleyenwu3chfqt642vrp8z", "green"]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet
{"result":null,"error":null,"id":"curltest"}
```

List addresses by green label:

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "getaddressesbylabel", "params": ["green"]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet
{"result":{"tb1qr66hw59k958xrz008n679p8r9n2y7mjfr3tsjc":{"purpose":"receive"},"tb1qunk223dztk2j2zqswleyenwu3chfqt642vrp8z":{"purpose":"receive"}},"error":null,"id":"curltest"}
```

### Receive tBTC

You can receive free test btc, by using any of these testnet faucet websites to receive tBTC over testnet:

- https://testnet-faucet.dash.org/
- http://faucet.test.dash.crowdnode.io/
- https://testnet.help/en/dashfaucet/testnet

The transaction details for sending 0.001 tbtc to my `tb1qr66hw59k958xrz008n679p8r9n2y7mjfr3tsjc` address, we will receive the following information:

- TxID: `637ea98aca23411059ad79aca7ea36ae30b68a173d89e6644703a06a1a846c25`
- Destination Address: `tb1qr66hw59k958xrz008n679p8r9n2y7mjfr3tsjc`
- Amount: `0.001`

Then to list transactions:

```
$ curl -s -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "listtransactions", "params": ["*"]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet | jq .
{
  "result": [
    {
      "address": "tb1qr66hw59k958xrz008n679p8r9n2y7mjfr3tsjc",
      "category": "receive",
      "amount": 0.001,
      "label": "green",
      "vout": 1,
      "confirmations": 0,
      "trusted": false,
      "txid": "637ea98aca23411059ad79aca7ea36ae30b68a173d89e6644703a06a1a846c25",
      "walletconflicts": [],
      "time": 1623337058,
      "timereceived": 1623337058,
      "bip125-replaceable": "no"
    }
  ],
  "error": null,
  "id": "curltest"
}
```

As you can see at the time, there were 0 confirmations, we can see the same txid as well as other info. With the testnet, we require at least 1 confirmation before a transaction is confirmed, where the mainnet requires 6.

To get balances for our wallet:

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "getbalances", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet
{"result":{"mine":{"trusted":0.00000000,"untrusted_pending":0.00100000,"immature":0.00000000}},"error":null,"id":"curltest"}
```

As you can see as we don't have any confirmations yet, so therefore the trusted value is still 0.

Listing the transactions over time:

```
$ curl -s -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "listtransactions", "params": ["*"]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet | jq .
{
  "result": [
    {
      "address": "tb1qr66hw59k958xrz008n679p8r9n2y7mjfr3tsjc",
      "category": "receive",
      "amount": 0.001,
      "label": "green",
      "vout": 1,
      "confirmations": 0,
      "trusted": false,
      "txid": "637ea98aca23411059ad79aca7ea36ae30b68a173d89e6644703a06a1a846c25",
      "walletconflicts": [],
      "time": 1623337058,
      "timereceived": 1623337058,
      "bip125-replaceable": "no"
    }
  ],
  "error": null,
  "id": "curltest"
}
```

After a couple of minutes:

```
$ curl -s -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "listtransactions", "params": ["*"]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet | jq .
{
  "result": [
    {
      "address": "yhLkeGrR8DZVa32LKfJzr1XMjyAAd3pSm5",
      "category": "receive",
      "amount": 0.49,
      "label": "",
      "vout": 0,
      "confirmations": 3640,
      "instantlock": true,
      "instantlock_internal": false,
      "chainlock": true,
      "blockhash": "0000002ab09136c457e4ed32b73842cb5b8018f6cdd9fb71f67a160bd8052824",
      "blockindex": 1,
      "blocktime": 1656424788,
      "txid": "098baf4bdb562e583a3c127a76567d8247c57b6868588edaf0758e3f4ef5f498",
      "walletconflicts": [],
      "time": 1656424788,
      "timereceived": 1656934621
    }
  ],
  "error": null,
  "id": "curltest"
}
```

### Block Explorer

We can also use a blockchain explorer,  head over to a testnet blockchain explorer, such as:

* https://blockexplorer.one/dash/testnet

And provide the txid, in my case it was this one:

* https://blockexplorer.one/dash/testnet/tx/098baf4bdb562e583a3c127a76567d8247c57b6868588edaf0758e3f4ef5f498

This transaction was done a while ago, so the confirmations will be much more than from the output above, but you can see the confirmations, addresses involved and tbtc amount.

To only get the `trusted` balance, using the `getbalance` method and with at least 6 confirmations:

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "getbalance", "params": ["*", 6]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet
{"result":0.00100000,"error":null,"id":"curltest"}
```

Let's send another transaction, the list the transactions using the `listtransactions` method:

```
$ curl -s -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "listtransactions", "params": ["*"]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet | jq .
{
  "result": [
    {
      "address": "tb1qr66hw59k958xrz008n679p8r9n2y7mjfr3tsjc",
      "category": "receive",
      "amount": 0.001,
      "label": "green",
      "vout": 1,
      "confirmations": 4,
      "blockhash": "0000000000000000ba226ad21b51fe3998180dc354ec433ad7a4c4897e04d805",
      "blockheight": 2004280,
      "blockindex": 107,
      "blocktime": 1623337883,
      "txid": "637ea98aca23411059ad79aca7ea36ae30b68a173d89e6644703a06a1a846c25",
      "walletconflicts": [],
      "time": 1623337058,
      "timereceived": 1623337058,
      "bip125-replaceable": "no"
    },
    {
      "address": "tb1qr66hw59k958xrz008n679p8r9n2y7mjfr3tsjc",
      "category": "receive",
      "amount": 0.0111048,
      "label": "green",
      "vout": 0,
      "confirmations": 1,
      "blockhash": "000000000000002912e2da87e6e752c38965fc21e108aab439fcdcd82ba6e37a",
      "blockheight": 2004283,
      "blockindex": 4,
      "blocktime": 1623338496,
      "txid": "3cac023b088a2ddb2d601538edfc72cd1bff1bd2e1a1531518500c5b7a52e473",
      "walletconflicts": [],
      "time": 1623338453,
      "timereceived": 1623338453,
      "bip125-replaceable": "no"
    }
  ],
  "error": null,
  "id": "curltest"
}
```

After 12 hours, we can see that we have 102 confirmations for our first transaction and 99 transactions for the second transaction:

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "listtransactions", "params": ["*"]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet | jq .
{
  "result": [
    {
      "address": "tb1qr66hw59k958xrz008n679p8r9n2y7mjfr3tsjc",
      "category": "receive",
      "amount": 0.001,
      "label": "green",
      "vout": 1,
      "confirmations": 102,
      "blockhash": "0000000000000000ba226ad21b51fe3998180dc354ec433ad7a4c4897e04d805",
      "blockheight": 2004280,
      "blockindex": 107,
      "blocktime": 1623337883,
      "txid": "637ea98aca23411059ad79aca7ea36ae30b68a173d89e6644703a06a1a846c25",
      "walletconflicts": [],
      "time": 1623337058,
      "timereceived": 1623337058,
      "bip125-replaceable": "no"
    },
    {
      "address": "tb1qr66hw59k958xrz008n679p8r9n2y7mjfr3tsjc",
      "category": "receive",
      "amount": 0.0111048,
      "label": "green",
      "vout": 0,
      "confirmations": 99,
      "blockhash": "000000000000002912e2da87e6e752c38965fc21e108aab439fcdcd82ba6e37a",
      "blockheight": 2004283,
      "blockindex": 4,
      "blocktime": 1623338496,
      "txid": "3cac023b088a2ddb2d601538edfc72cd1bff1bd2e1a1531518500c5b7a52e473",
      "walletconflicts": [],
      "time": 1623338453,
      "timereceived": 1623338453,
      "bip125-replaceable": "no"
    },
    {
      "address": "tb1qr66hw59k958xrz008n679p8r9n2y7mjfr3tsjc",
      "category": "receive",
      "amount": 0.03521065,
      "label": "green",
      "vout": 5,
      "confirmations": 27,
      "blockhash": "000000000000004255a9d5af67b4649ff3f4d6a2f0c334261ca822cd9fbd00a9",
      "blockheight": 2004355,
      "blockindex": 43,
      "blocktime": 1623383177,
      "txid": "eb43868bd2c5abd97d4f5f11450952837bc3edc149478248e9453fdfb05c5187",
      "walletconflicts": [],
      "time": 1623382990,
      "timereceived": 1623382990,
      "bip125-replaceable": "no"
    }
  ],
  "error": null,
  "id": "curltest"
}
```

After 3 transactions, view the balance in the test wallet using the `getbalance` method:

```
$ curl -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curltest", "method": "getbalance", "params": ["*", 6]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet
{"result":0.04731545,"error":null,"id":"curltest"}
```

### Sending a raw transaction

A easier way to send a transaction is by using `sendtoaddress` and the source wallet will be in the request url, ie: `/wallet/wallet-name`

First we look if we have a address for our account that we are sending from, if not then we can create a wallet and a address, for this example, I have a address for the `wallet` wallet:

```
$ curl -s -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curl", "method": "getaddressesbylabel", "params": [""]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/wallet
{"result":{"tb1qks4tyrz52vvdh35kcx0ypvnj3fjdkl692pzfyc":{"purpose":"receive"}},"error":null,"id":"curl"}
```

Ensure that our source wallet has funds in it:

```
$ curl -s -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curl", "method": "getbalance", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/wallet | python -m json.tool
{
    "error": null,
    "id": "curl",
    "result": 0.01811929
}
```

We have enough funds to send, so we now have the source wallet name and we need to get the wallet address, where we want to send the funds to, which in this case is the address in `test-wallet` as the destination:

```
curl -s -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curl", "method": "getaddressesbylabel", "params": [""]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet
{"result":{"tb1qzxmefmcpq98z42v67a80gvug2fe979r5h768yv":{"purpose":"receive"}},"error":null,"id":"curl"}
```

Just to double check our current funds in the wallet that will receive funds:

```
$ curl -s -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curl", "method": "getbalance", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/test-wallet | python -m json.tool
{
    "error": null,
    "id": "curl",
    "result": 0.35572584
}
```

Now we will use the `sendtoaddress` method, with the recipient address and the amount to send as the parameters. To summarize:

- Source Wallet: `wallet`
- Destination Address:  `tb1qzxmefmcpq98z42v67a80gvug2fe979r5h768yv`
- Amount to send: `0.01.`

Sending the amount:

```
$ curl -s -u "$authstring"  -d '{"jsonrpc": "1.0", "id":"0", "method": "sendtoaddress", "params":["tb1qzxmefmcpq98z42v67a80gvug2fe979r5h768yv", 0.01]}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/wallet
{"result":"df087095ac79d678f9d98c8bf8ebface2ac62a20546d85e07a852feb2c3bea50","error":null,"id":"0"}
```

We will receive a transaction id, and if we list for transactions for our source wallet, we will see the transaction:

```
$ curl -s -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curl", "method": "listtransactions", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/wallet | python -m json.tool
{
    "error": null,
    "id": "curl",
    "result": [
        {
            "address": "tb1qks4tyrz52vvdh35kcx0ypvnj3fjdkl692pzfyc",
            "amount": 0.01811929,
            "bip125-replaceable": "no",
            "blockhash": "000000000000003c0ac4978ba815ff8f0d7f55da98923c686118c75461fb579e",
            "blockheight": 2091275,
            "blockindex": 1,
            "blocktime": 1630677226,
            "category": "receive",
            "confirmations": 1,
            "label": "",
            "time": 1630677177,
            "timereceived": 1630677177,
            "txid": "e44b45a309284e8044a15dca8c0a895a5c7072741882281038fb185cc0c1a0d9",
            "vout": 0,
            "walletconflicts": []
        },
        {
            "abandoned": false,
            "address": "tb1qzxmefmcpq98z42v67a80gvug2fe979r5h768yv",
            "amount": -0.01,
            "bip125-replaceable": "no",
            "category": "send",
            "confirmations": 0,
            "fee": -1.41e-06,
            "time": 1630677743,
            "timereceived": 1630677743,
            "trusted": true,
            "txid": "df087095ac79d678f9d98c8bf8ebface2ac62a20546d85e07a852feb2c3bea50",
            "vout": 0,
            "walletconflicts": []
        }
    ]
}
```

So when we look at the sender wallet, we will see the funds was deducted:

```
$ curl -s -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curl", "method": "getbalance", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/wallet | python -m json.tool
{
    "error": null,
    "id": "curl",
    "result": 0.00811788
}
```

And when we look at the receiver wallet, we can see that the account was received:

```
$ curl -s -u "$authstring" -d '{"jsonrpc": "1.0", "id": "curl", "method": "getbalance", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:19998/wallet/rpi01-main | python -m json.tool
{
    "error": null,
    "id": "curl",
    "result": 0.36572584
}
```
