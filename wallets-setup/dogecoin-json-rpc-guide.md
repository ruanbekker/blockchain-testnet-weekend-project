# Dogecoin JSON RPC Guide

This guide will show the basics on how to get your account setup and create a dogecoin address so that we can send funds to your account.

## Ensure Dogecoin is Running

Ensure that the dogecoin daemon is running, either using systemd:

```bash
$ sudo systemctl is-active dogecoind
active
```

or using netstat to see if the port that we assigned `44555` is listening:

```bash
$ sudo netstat -tulpn | grep dogecoind
tcp        0      0 0.0.0.0:44555           0.0.0.0:*               LISTEN      2170/dogecoind
tcp        0      0 127.0.0.1:44556         0.0.0.0:*               LISTEN      2170/dogecoind
```

## JSON RPC

The following calls will interact with the json-rpc interface

### GetInfo

First we can use the `getinfo` method to verify that we can get a response from dogecoin:

```bash
$ curl -s -u "user:pass" -d '{"jsonrpc": "1.0", "id": "curl", "method": "getinfo", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:44555/ | python3 -m json.tool
```

This should give a response more or less like the following:

```json
{
    "result": {
        "version": 1140400,
        "protocolversion": 70015,
        "walletversion": 130000,
        "balance": 0.0,
        "blocks": 1082322,
        "timeoffset": 0,
        "connections": 8,
        "proxy": "",
        "difficulty": 0.001734473137276158,
        "testnet": true,
        "keypoololdest": 1632237929,
        "keypoolsize": 100,
        "paytxfee": 1.0,
        "relayfee": 0.001,
        "errors": ""
    },
    "error": null,
    "id": "curl"
}
```

### GetNewAddress

Create a new account and get a new dogecoin address for that account, in this example I will name the account `main`:

```bash
$ curl -s -u "user:pass" -d '{"jsonrpc": "1.0", "id": "curl", "method": "getnewaddress", "params": ["main"]}' -H 'content-type: text/plain;' http://127.0.0.1:44555/ | python3 -m json.tool
```

The response should look more or less like this:

```json
{
    "result": "nqoZhrXxsd1ybMZbrSkZVmJuXcYDnRh7cz",
    "error": null,
    "id": "curl"
}
```

### ListAccounts

The following call will list all the accounts and it's balances:

```bash
$ curl -s -u "user:pass" -d '{"jsonrpc": "1.0", "id": "curl", "method": "listaccounts", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:44555/ | python3 -m json.tool
```

This should return 2 accounts, the default and the `main` account that we created:

```json
{
    "result": {
        "": 0.0,
        "main": 0.0
    },
    "error": null,
    "id": "curl"
}
```

### GetAddressesByAccount

If you would like to return the address for a specific account, in this case `main`:

```bash
$ curl -s -u "user:pass" -d '{"jsonrpc": "1.0", "id": "curl", "method": "getaddressesbyaccount", "params": ["main"]}' -H 'content-type: text/plain;' http://127.0.0.1:44555/
```

And the response should look more or less like this:

```json
{"result":["nXZiVUtpC3pURmMPuKsBzb9ett2WVS8t2e"],"error":null,"id":"curl"}
```

### GetBalance

To get only the balance from a specific account, in this case `main`:

```bash
curl -s -u "user:pass" -d '{"jsonrpc": "1.0", "id": "curl", "method": "getbalance", "params": ["main"]}' -H 'content-type: text/plain;' http://127.0.0.1:44555/
```

The response should look more or less like this:

```json
{"result":0.0,"error":null,"id":"curl"}
```

### SendFrom

We will be sending funds from our `main` wallet, but before we can do that we need to send funds to our account, you can either [mine](#mine) or you can claim tesnet doge from a [faucet](https://shibe.technology/)

Using the `sendfrom` method, we can send doge from our wallet, in this case `main`, to another address in this case `nhNZmirSu3aayp2CZU6SHf4AEjT8TkJcyV` and the 3rd parameter, the amount of doge we want to send:

```bash
curl -s -u "user:pass" -d '{"jsonrpc": "1.0", "id": "curl", "method": "sendfrom", "params": ["main", "nhNZmirSu3aayp2CZU6SHf4AEjT8TkJcyV", 10.0]}' -H 'content-type: text/plain;' http://127.0.0.1:44555/
```

The response should include the transaction id, like below:

```json
{"result":"2609c130566a3233a83a78a6394a33ecec91d5cecd1be5029de4db11b69d9cd1","error":null,"id":"curl"}
```

This transaction can be looked up on the [dogecoin testnet block explorer](https://blockexplorer.one/dogecoin/testnet/tx/2609c130566a3233a83a78a6394a33ecec91d5cecd1be5029de4db11b69d9cd1) to verify if the transaction went through, the number of confirmations, etc.

## Mine

If you would like to mine by using the `generatetoaddress` method using the dogecoin-cli and specifying our address for the rewards to be paid to:

```
$ /opt/dogecoin/current/bin/dogecoin-cli -conf=/blockchain/dogecoin/config/dogecoin.conf generatetoaddress 10 nXZiVUtpC3pURmMPuKsBzb9ett2WVS8t2e
```

