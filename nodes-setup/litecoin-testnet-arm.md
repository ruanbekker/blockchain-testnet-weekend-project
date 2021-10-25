# Litecoin Testnet

This document demonstrates the installation of litecoin v0.18.1 running on the testnet for ARM linux, running on a RaspberryPi 3

## Notes

This is a testnet, therefore a weak username and password was chosen, please increase security when running mainnets.

## Preperation

Create the user:

```bash
sudo useradd -s /bin/bash -m crypto
```

Create the directories:

```bash
sudo mkdir -p /blockchain/litecoin/{data,scripts}
sudo mkdir -p /usr/local/litecoin/1.14.4/bin
sudo mkdir -p /home/crypto/.litecoin
```

Change the permissions:

```bash
sudo chown -R crypto:crypto /blockchain/litecoin
sudo chown -R crypto:crypto /home/crypto/.litecoin
```

## Installation

From [litecoin's releases](https://download.litecoin.org/) page, I fetched version [0.18.1](https://download.litecoin.org/litecoin-0.18.1/):

```bash
cd /tmp
wget https://download.litecoin.org/litecoin-0.18.1/linux/litecoin-0.18.1-arm-linux-gnueabihf.tar.gz
```

Extract the tarball:

```bash
tar -xvf litecoin-0.18.1-arm-linux-gnueabihf.tar.gz
```

Move the binaries to our created directories:

```bash
sudo mv litecoin-0.18.1/bin/litecoin* /usr/local/litecoin/0.18.1/bin/
```

Then create a symlink to `current` as that will be referenced from systemd:

```bash
sudo ln -s /usr/local/litecoin/1.14.4 /usr/local/litecoin/current
```

## Configuration

Create the configuration for litecoin in `/home/crypto/.litecoin/litecoin.conf` with the following content:

```
datadir=/blockchain/litecoin/data
printtoconsole=1
onlynet=ipv4
rpcallowip=127.0.0.1
rpcuser=user
rpcpassword=pass
rpcclienttimeout=300
testnet=1
prune=2500
walletnotify=/blockchain/litecoin/scripts/notify.sh %s %w
[test]
rpcbind=127.0.0.1
rpcport=19332
# uncomment after the wallet has been created
# wallet=main
```

Create the wallet notify script in `/blockchain/litecoin/scripts/notify.sh` with the content of:

```bash
#!/usr/bin/env bash
echo "[$(date +%FT%T)] $1 $2" >> /var/log/wallet-notify.log
```

Create the file where the wallet notify data will be written to:

```bash
sudo touch /var/log/wallet-notify.log
```

Change the permissions of the file so that the crypto user can write to it:

```bash
sudo chown crypto:crypto /var/log/wallet-notify.log
```

Make the script executable:

```bash
sudo chmod +x /blockchain/litecoin/scripts/notify.sh
```

Create the systemd unit file in `/etc/systemd/system/litecoind.service`:

```bash
[Unit]
Description=Litecoin Core Testnet
After=network.target

[Service]
User=crypto
Group=crypto
WorkingDirectory=/blockchain/litecoin/data
Type=simple
ExecStart=/usr/local/litecoin/current/bin/litecoind -conf=/home/crypto/.litecoin/litecoin.conf

[Install]
WantedBy=multi-user.target
```

Update the `PATH` variable to include bitcoin binaries in `/etc/profile.d/litecoind.sh` with the following content:

```bash
export PATH=$PATH:/usr/local/litecoin/current/bin
```

You can update your current session by running:

```bash
export PATH=$PATH:/usr/local/litecoin/current/bin
```

Ensure permissions are set:

```bash
sudo chown -R crypto:crypto /blockchain/litecoin
sudo chown -R crypto:crypto /home/crypto
```

Reload systemd:

```bash
sudo systemctl daemon-reload
```

## Start the IBD

Start litecoin so that the initial block download can happen:

```bash
sudo systemctl restart litecoind
```

This might take some time, but you can follow the progress by doing:

```bash
sudo journalctl -fu litecoind
```

A fully sync node should look like this:

```bash
# sudo journalctl -fu litecoind
Oct 05 14:29:58 rpi-03 litecoind[532]: 2021-10-05T14:29:58Z UpdateTip: new best=000000000000003b06a186bbd79909e1a338196b5cffcee1979d6c4fc90f67a9 height=2097621 version=0x20a00000 log2_work=74.510314 tx=61253790 date='2021-10-05T14:29:54Z' progress=1.000000 cache=0.4MiB(1477txo)
```

You can use the json-rpc as well:

```bash
curl -s -u "user:pass" -d '{"jsonrpc": "1.0", "id": "curl", "method": "getblockchaininfo", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:19332/  | python3 -m json.tool
```

## Wallets Setup

You can follow this guide to setup your wallet and send testnet funds to your address:

- [Litecoin JSON RPC Guide](https://github.com/ruanbekker/blockchain-testnet-weekend-project/blob/main/wallets-setup/litecoin-json-rpc-guide.md)
