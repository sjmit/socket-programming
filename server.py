#!/usr/bin/env  python3

import socket
import random
import sys

HOST = 'localhost'


def main(argv):

    # Check if port is an integer
    try:
        port = int(argv[0])
    except ValueError:
        print("Port is not an integer")
        return

    # Open IPv4/TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # Allows socket to be immediately reopened after closing
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, port))
        s.listen()

        # Blocking function call that waits for connection
        conn, _ = s.accept()
        with conn:

            # Waits for correct message
            while True:
                msg = conn.recv(4)
                if msg == b'256':
                    break
            # Generates random port in correct range
            r_port = random.randint(1024, 65535)
            print(("Negotiation has been detected. "
                   "Please select your special random port"), r_port)

            # Sends random port back to client
            conn.sendall(str(r_port).encode('utf8'))

    # Socket connection implicitly closes

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        
        # Allows socket to be immediately reopened after closing
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, r_port))

        # Opens file
        with open('output.txt', 'wb') as f:
            while True:
                packet, address = s.recvfrom(4)
                if packet == b'\x04':  # EOT
                    break
                f.write(packet)

                # Send ack back to client
                s.sendto(packet.upper(), address)


if __name__ == '__main__':
    main(sys.argv[1:])
