# Dogecoin Testnet

This document demonstrates the installation of dogecoin v1.14.4 running on the testnet for ARM linux, running on a RaspberryPi 3

## Notes

This is a testnet, therefore a weak username and password was chosen, please increase security when running mainnets.

## Preperation

Create the user:

```bash
sudo useradd -s /bin/bash -m crypto
```

Create the directories:

```bash
sudo mkdir -p /blockchain/dogecoin/{data,scripts}
sudo mkdir -p /usr/local/dogecoin/1.14.4/bin
sudo mkdir -p /home/crypto/.dogecoin
```

Change the permissions:

```bash
sudo chown -R crypto:crypto /blockchain/dogecoin
sudo chown -R crypto:crypto /home/crypto/.dogecoin
```

## Installation

From [dogecoin's releases](https://github.com/dogecoin/dogecoin/releases) page, I fetched version [1.14.4](https://github.com/dogecoin/dogecoin/releases/tag/v1.14.4):

```bash
cd /tmp
wget https://github.com/dogecoin/dogecoin/releases/download/v1.14.4/dogecoin-1.14.4-arm-linux-gnueabihf.tar.gz
```

Extract the tarball:

```bash
tar -xvf dogecoin-1.14.4-arm-linux-gnueabihf.tar.gz
```

Move the binaries to our created directories:

```bash
sudo mv dogecoin-1.14.4/bin/dogecoin* /usr/local/dogecoin/1.14.4/bin/
```

Then create a symlink to `current` as that will be referenced from systemd:

```bash
sudo ln -s /usr/local/dogecoin/1.14.4 /usr/local/dogecoin/current
```

## Configuration

Create the configuration for bitcoin in `/home/crypto/.dogecoin/dogecoin.conf` with the following content:

```
datadir=/blockchain/dogecoin/data
printtoconsole=1
onlynet=ipv4
rpcallowip=127.0.0.1
rpcuser=user
rpcpassword=pass
rpcclienttimeout=300
testnet=1
prune=2500
walletnotify=/blockchain/dogecoin/scripts/notify.sh %s %w
[test]
rpcbind=127.0.0.1
rpcport=44555
# uncomment after the wallet has been created
# wallet=main
```

Create the wallet notify script in `/blockchain/dogecoin/scripts/notify.sh` with the content of:

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
sudo chmod +x /blockchain/dogecoin/scripts/notify.sh
```

Create the systemd unit file in `/etc/systemd/system/dogecoind.service`:

```bash
[Unit]
Description=Dogecoin Core Testnet
After=network.target

[Service]
User=crypto
Group=crypto
WorkingDirectory=/blockchain/dogecoin/data
Type=simple
ExecStart=/usr/local/dogecoin/current/bin/dogecoind -conf=/home/crypto/.dogecoin/dogecoin.conf

[Install]
WantedBy=multi-user.target
```

Update the `PATH` variable to include bitcoin binaries in `/etc/profile.d/dogecoind.sh` with the following content:

```bash
export PATH=$PATH:/usr/local/dogecoin/current/bin
```

You can update your current session by running:

```bash
export PATH=$PATH:/usr/local/dogecoin/current/bin
```

Ensure permissions are set:

```bash
sudo chown -R crypto:crypto /blockchain/dogecoin
sudo chown -R crypto:crypto /home/crypto
```

Reload systemd:

```bash
sudo systemctl daemon-reload
```

## Start the IBD

Start dogecoin so that the initial block download can happen:

```bash
sudo systemctl restart dogecoind
```

This might take some time, but you can follow the progress by doing:

```bash
sudo journalctl -fu dogecoind
```

A fully sync node should look like this:

```bash
# sudo journalctl -fu bitcoind
Oct 05 14:29:58 rpi-03 dogecoind[532]: 2021-10-05T14:29:58Z UpdateTip: new best=000000000000003b06a186bbd79909e1a338196b5cffcee1979d6c4fc90f67a9 height=2097621 version=0x20a00000 log2_work=74.510314 tx=61253790 date='2021-10-05T14:29:54Z' progress=1.000000 cache=0.4MiB(1477txo)
```

You can use the json-rpc as well:

```bash
curl -s -u "user:pass" -d '{"jsonrpc": "1.0", "id": "curl", "method": "getblockchaininfo", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:44555/  | python3 -m json.tool
```
