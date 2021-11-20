#!/usr/bin/env python3
# https://support.blockdaemon.com/hc/en-us/articles/360024191871-Viewing-A-Bitcoin-Dedicated-Node-Transaction-with-ZMQ

import zmq
import sys
import time
import bitcoin

context = zmq.Context()
socket = context.socket(zmq.SUB)
# Connect to ZMQ
socket.connect("tcp://localhost:28332")

# Subscribe to all new raw transactions
#socket.setsockopt_string(zmq.SUBSCRIBE, 'rawtx')
socket.setsockopt_string(zmq.SUBSCRIBE, 'hashblock')

while True:
    # Wait for the next raw transaction
    msg = socket.recv_multipart()
    topic = msg[0]
    body = msg[1]

    # Convert the binary transaction into a simple dict
    tx = bitcoin.deserialize(body)

    # Calculate the total value of all outputs
    total_value = 0
    for out in tx['outs']:
        total_value += out['value']

    # Print the result
    if total_value / 100000000.0 > 10:
        print("")
        print("New transaction: {}".format(bitcoin.txhash(body)))
        print("Total value of all outputs: {} BTC".format(total_value / 100000000.0))
