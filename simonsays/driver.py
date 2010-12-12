#!/usr/bin/env python
# ---------------------------------------------------------------------------- #

import sys
from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.transport import THttpClient
from thrift.protocol import TBinaryProtocol
from simonsays import SimonSays
from simonsays.ttypes import *

def main():
    host = "thriftpuzzle.facebook.com"
    port = 9030
    socket = TSocket.TSocket(host, port)
    transport = TTransport.TBufferedTransport(socket)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = SimonSays.Client(protocol)
    transport.open()

    if solve(client):
        result_string = client.winGame()
        print result_string

    transport.close()

def solve(client):
    if not client.registerClient('mlbright@gmail.com'):
        sys.stderr.write("WTF: could not register\n")
        return False

    while True:
        colors = client.startTurn()
        for color in colors:
            if not client.chooseColor(color):
                sys.stderr.write("wtf: wrong color\n")
                break
        if client.endTurn():
            return True

    return False

if __name__ == "__main__":
    main()
