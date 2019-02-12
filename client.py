#!/usr/bin/env  python3

import socket
import sys


def main(argv):

    host = argv[0]
    port = argv[1]
    filename = argv[2]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((host, port))
        s.sendall(b'256')
        r_port = int(s.recv(8).decode('utf8'))

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((host, r_port))
        try:
            f = open(filename, 'rb')
        except OSError:
            print("{} not found".format(filename))
        else:
            with f:
                while True:
                    packet = f.read(4)
                    if not packet:
                        break
                    s.sendall(packet)


if __name__ == '__main__':
    main(sys.argv[1:])
