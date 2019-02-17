#!/usr/bin/env  python3

import socket
import sys


def main(argv):

    host = argv[0]
    filename = argv[2]

    # Check if port is an integer
    try:
        port = int(argv[1])
    except ValueError:
        print("Port is not an integer")
        return

    # Open IPv4/TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # Allows socket to be immediately reopened after closing
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((host, port))

        # Send arbitrary command
        # This function will resend in the event of an error
        s.sendall(b'256')

        # Recieve random port number
        r_port = int(s.recv(8).decode('utf8'))

    # Socket connection implicitly closes

    # Open IPv4/UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

        # Allows socket to be immediately reopened after closing
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((host, r_port))

        # Open file
        try:
            f = open(filename, 'rb')
        except OSError:
            print("{} not found".format(filename))
        else:
            with f:
                # Send packets of 4 until eof is reached
                while True:
                    packet = f.read(4)
                    if not packet:
                        s.send(b'\x04')  # EOT
                        break
                    s.sendall(packet)

                    # Prints the server's response
                    print(s.recv(4))


if __name__ == '__main__':
    main(sys.argv[1:])
