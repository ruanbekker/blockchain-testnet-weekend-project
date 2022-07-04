# DASH Testnet

This document demonstrates the installation of dash v0.17.0.3 running on the testnet for ARM linux, running on a RaspberryPi 3

## Notes

This is a testnet, therefore a weak username and password was chosen, please increase security when running mainnets.

## Preperation

Create the user:

```bash
sudo useradd -s /bin/bash -m crypto
```

Create the directories:

```bash
sudo mkdir -p /blockchain/dashcore/{data,scripts}
sudo mkdir -p /usr/local/dashcore/0.17.0/bin
sudo mkdir -p /home/crypto/.dashcore
```

Change the permissions:

```bash
sudo chown -R crypto:crypto /blockchain/dashcore
sudo chown -R crypto:crypto /home/crypto/.dashcore
```

## Installation

From [dash's releases](https://github.com/dashpay/dash/releases) page, I fetched version [0.17.0.3](https://github.com/dashpay/dash/releases/tag/v0.17.0.3):

```bash
cd /tmp
wget https://github.com/dashpay/dash/releases/download/v0.17.0.3/dashcore-0.17.0.3-arm-linux-gnueabihf.tar.gz 
```

Extract the tarball:

```bash
tar -xvf dashcore-0.17.0.3-arm-linux-gnueabihf.tar.gz
```

Move the binaries to our created directories:

```bash
sudo mv dashcore-0.17.0/bin/dash* /usr/local/dashcore/0.17.0/bin/
```

Then create a symlink to `current` as that will be referenced from systemd:

```bash
sudo ln -s /usr/local/dashcore/0.17.0 /usr/local/dashcore/current
```

## Configuration

Create the configuration for dash in `/home/crypto/.dashcore/dash.conf` with the following content:

```
datadir=/blockchain/dashcore/data
printtoconsole=1
onlynet=ipv4
rpcallowip=127.0.0.1
rpcuser=user
rpcpassword=pass
rpcclienttimeout=300
testnet=1
txindex=0
prune=1200
wallet=main
[test]
rpcbind=127.0.0.1
rpcport=19998
# uncomment after the wallet has been created
# wallet=main
```

Create the systemd unit file in `/etc/systemd/system/dashd.service`:

```bash
[Unit]
Description=Dashcore Testnet
After=network.target

[Service]
User=crypto
Group=crypto
WorkingDirectory=/blockchain/dashcore/data
Type=simple
ExecStart=/usr/local/dashcore/current/bin/dashd -conf=/home/crypto/.dashcore/dash.conf

[Install]
WantedBy=multi-user.target
```

Update the `PATH` variable to include bitcoin binaries in `/etc/profile.d/dashd.sh` with the following content:

```bash
export PATH=$PATH:/usr/local/dashcore/current/bin
```

You can update your current session by running:

```bash
export PATH=$PATH:/usr/local/dashcore/current/bin
```

Ensure permissions are set:

```bash
sudo chown -R crypto:crypto /blockchain/dashcore
sudo chown -R crypto:crypto /home/crypto
```

Reload systemd:

```bash
sudo systemctl daemon-reload
```

## Start the IBD

Start dash so that the initial block download can happen:

```bash
sudo systemctl restart dashd
```

This might take some time, but you can follow the progress by doing:

```bash
sudo journalctl -fu dashd
```

A fully sync node should look like this:

```bash
# sudo journalctl -fu dashd
Jul 04 13:22:34 node4.infra.ruan.dev dashd[8228]: 2022-07-04T11:22:34Z UpdateTip: new best=000000ab46dda23f77d5247ff635c6434968a77a80cb52161a2a2bda5766143a height=755289 version=0x20000000 log2_work=57.31213481 tx=5538819 date='2022-07-04T11:22:33Z' progress=1.000000 cache=31.0MiB(226139txo) evodb_cache=23.0MiB
```

You can use the json-rpc as well:

```bash
curl -s -u "user:pass" -d '{"jsonrpc": "1.0", "id": "curl", "method": "getblockchaininfo", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:19998/
```

## Wallets Setup

You can follow this guide to setup your wallet and send testnet funds to your address:

- [DASH JSON RPC Guide](https://github.com/ruanbekker/blockchain-testnet-weekend-project/blob/main/wallets-setup/dash-json-rpc-guide.md)
