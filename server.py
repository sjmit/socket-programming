#!/usr/bin/env  python3

import socket
import random
import sys

HOST = 'localhost'


def main(argv):

    port = sys.argv[0]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, port))
        s.listen()
        conn, _ = s.accept()
        with conn:
            while True:
                msg = conn.recv(4)
                if msg == b'256':
                    break
            r_port = random.randint(1024, 65535)
            print("Negotiation has been detected. Please select your special random port", r_port)
            conn.sendall(str(r_port)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(0.1)
        s.bind((HOST, r_port))
        with open('output.txt', 'wb') as f:
            while True:
                try:
                    packet = s.recv(4)
                except socket.timeout:
                    break
                f.write(packet)
                if len(packet) < 4:
                    break


if __name__ == '__main__':
    main(sys.argv[1:])
