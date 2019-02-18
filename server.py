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
        print("ERROR - Port is not an integer")
        return

    # Open IPv4/TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # Allows socket to be immediately reopened after closing
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, port))
        s.listen()

        # Blocking function call that waits for connection
        connection, _ = s.accept()
        with connection:

            # Waits for correct message
            while True:
                message = connection.recv(4)
                if message == b'256':
                    break
            # Generates random port in correct range
            r_port = random.randint(1024, 65535)
            print(("Negotiation has been detected. "
                   "Please select your special random port"), r_port)

            # Sends random port back to client
            connection.sendall(str(r_port).encode('utf8'))

    # Socket connection implicitly closes

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

        # Allows socket to be immediately reopened after closing
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(5)  # In seconds
        s.bind((HOST, r_port))

        # Opens file
        with open('output.txt', 'wb') as f:
            while True:
                try:
                    packet, address = s.recvfrom(4)
                except socket.timeout:
                    print("ERROR - Connection timed out")
                    break
                if packet == b'\x04':  # EOT
                    break
                f.write(packet)

                # Send ack back to client
                s.sendto(packet.upper(), address)


if __name__ == '__main__':
    main(sys.argv[1:])
