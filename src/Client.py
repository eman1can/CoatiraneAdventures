# import sys
# import socket
# import selectors
# import traceback
#
# import base64
# import os
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# from cryptography.fernet import Fernet
#
# #vars
# sel = selectors.DefaultSelector()
# salt = b'\x81u\xfd\xcb\xe4f\x02\r\xba\x13\xb0\x1f\x88\xd2\xa78'
#
# auth_code = '3m1lia<3'
# pass_phrase = b'coatrnae'
# pass_user = b'AlyssaVeronica'
#
# HOST = '127.0.0.1'
# PORT = 12345
# states = {}
# keys = {}
#
# #auth encryption
# auth_password = auth_code.encode()
# auth_kdf = PBKDF2HMAC(
#     algorithm=hashes.SHA256(),
#     length=32,
#     salt=salt,
#     iterations=100000,
#     backend=default_backend()
# )
# auth_kdf2 = PBKDF2HMAC(
#     algorithm=hashes.SHA256(),
#     length=32,
#     salt=salt,
#     iterations=100000,
#     backend=default_backend()
# )
# auth_key = base64.urlsafe_b64encode(auth_kdf.derive(auth_password)) # Can only use kdf once
#
#
# #setup client
# print("starting connection to ", (HOST, PORT))
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect_ex((HOST, PORT))
# print("Connection established")
# client_state = True
# while client_state:
#     f = Fernet(auth_key)
#     sock.send(f.encrypt(pass_phrase))
#     sock.send(f.encrypt(pass_user))
#     f = Fernet(base64.urlsafe_b64encode(auth_kdf2.derive(pass_user)))
#     while True:
#         msg = input()
#         sock.send(f.encrypt(msg.encode()))
#         if msg == "stop" or msg == "close":
#             sock.close()
#             client_state = False
#             break

import selectors
import socket
import threading

import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import time

mysel = selectors.DefaultSelector()
keep_running = True
outgoing = []
bytes_sent = 0
bytes_received = 0

def run_IO(bytes_sent, bytes_received):
    while True:
        # print('waiting for I/O')
        for key, mask in mysel.select(timeout=1):
            connection = key.fileobj
            client_address = connection.getpeername()
            # print('client({})'.format(client_address))

            if mask & selectors.EVENT_READ:
                # print('  ready to read')
                data = connection.recv(1024)
                if data:
                    # A readable client socket has data
                    # print('  received {!r}'.format(data))
                    bytes_received += len(data)

                # Interpret empty result as closed connection,
                # and also close when we have received a copy
                # of all of the data sent.
                keep_running = not (
                    data or
                    (bytes_received and
                     (bytes_received == bytes_sent))
                )

            if mask & selectors.EVENT_WRITE:
                # print('  ready to write')
                if not outgoing:
                    pass
                    # We are out of messages, so we no longer need to
                    # write anything. Change our registration to let
                    # us keep reading responses from the server.
                    # print('  switching to read-only')
                    # mysel.modify(sock, selectors.EVENT_READ)
                else:
                    # Send the next message.
                    next_msg = outgoing.pop(0)
                    print('  sending {!r}'.format(next_msg))
                    sock.sendall(next_msg)
                    bytes_sent += len(next_msg)
                    # time.sleep(.200)

def get_in():
    while True:
        outgoing.append(secondary_fernet.encrypt(input().encode()))
        time.sleep(.200)


# Connecting is a blocking operation, so call setblocking()
# after it returns.
auth_code = b'em1lia<3'
pass_phrase = b'coatrnae'
username = b'AlyssaVeronica'
salt = b'\x81u\xfd\xcb\xe4f\x02\r\xba\x13\xb0\x1f\x88\xd2\xa78'
auth_kdf2 = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
main_fernet = Fernet(base64.urlsafe_b64encode(auth_kdf2.derive(auth_code)))
auth_kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
secondary_fernet = Fernet(base64.urlsafe_b64encode(auth_kdf.derive(username)))
server_address = ('localhost', 10000)
print('connecting to {} port {}'.format(*server_address))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_address)
sock.setblocking(False)

# Set up the selector to watch for when the socket is ready
# to send data as well as when there is data to read.
mysel.register(
    sock,
    selectors.EVENT_READ | selectors.EVENT_WRITE,
)

outgoing.append(main_fernet.encrypt(pass_phrase))
outgoing.append(main_fernet.encrypt(b'AlyssaVeronica'))
outgoing.append(secondary_fernet.encrypt(b'Hi!'))
outgoing.append(secondary_fernet.encrypt(b'Hrllo!'))
outgoing.append(secondary_fernet.encrypt(b'Go away!'))

x = threading.Thread(target=run_IO, args=(bytes_sent, bytes_received))
y = threading.Thread(target=get_in)
x.start()
y.start()
# print('shutting down')
# mysel.unregister(connection)
# connection.close()
# mysel.close()