# class Connection():
#     def __init__(self, selector, socket, address, fernet):
#         self.selector = selector
#         self.socket = socket
#         self.address = address
#         self.f = fernet
#         self._recv_buffer = b""
#         self._send_buffer = b""
#
#     def _read(self):
#         try:
#             # Should be ready to read
#             data = self.socket.recv(4096)
#             print(data)
#         except BlockingIOError:
#             # Resource temporarily unavailable (errno EWOULDBLOCK)
#             pass
#         else:
#             if data:
#                 self._recv_buffer += data
#             else:
#                 raise RuntimeError("Peer closed.")
#
#     def _write(self):
#         if self._send_buffer:
#             print("sending", repr(self._send_buffer), "to", self.address)
#             try:
#                 # Should be ready to write
#                 sent = self.socket.send(self._send_buffer)
#             except BlockingIOError:
#                 # Resource temporarily unavailable (errno EWOULDBLOCK)
#                 pass
#             else:
#                 self._send_buffer = self._send_buffer[sent:]
#
#     def process_events(self, mask):
#         if mask & selectors.EVENT_READ:
#             self._read()
#         if mask & selectors.EVENT_WRITE:
#             self._write()
#
#     def close(self):
#         print("closing connection to", self.address)
#         try:
#             self.selector.unregister(self.socket)
#         except Exception as e:
#             print(
#                 f"error: selector.unregister() exception for",
#                 f"{self.address}: {repr(e)}",
#             )
#
#         try:
#             self.socket.close()
#         except OSError as e:
#             print(
#                 f"error: socket.close() exception for",
#                 f"{self.address}: {repr(e)}",
#             )
#         finally:
#             # Delete reference to socket object for garbage collection
#             self.socket = None
#
# class Queue():
#     def __init__(self, capacity=None):
#         if capacity == None:
#             self.capacity = 20
#         else:
#             self.capacity = capacity
#         self.front = self.size = 0
#         self.rear = capacity - 1
#         self.array = []
#
#     def isFull(self):
#         return self.capacity == self.size
#
#     def isEmpty(self):
#         return self.size == 0
#
#     def enqueue(self, item):
#         self.size += 1
#         self.rear = (self.rear + 1) % self.capacity
#         self.array[self.rear] = item
#
#     def dequeue(self):
#         if self.isEmpty():
#             return None
#         item = self.array[self.front]
#         self.front = (self.front + 1) % self.capacity
#         self.size = self.size - 1
#         return item
#
#     def rear(self):
#         if self.isEmpty():
#             return None
#         return self.array[self.rear]
#
#     def front(self):
#         if self.isEmpty():
#             return None
#         return self.array[self.front]
#
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
# queue = Queue()
#
#
# auth_code = b'3m1lia<3'
# pass_phrase = b'coatrnae'
#
# HOST = '127.0.0.1'
# PORT = 12345
# states = {}
# keys = {"pre-auth": auth_code, "auth": ""}
#
# #functions
#
#
# def accept_connection(sock):
#     conn, addr = sock.accept()  # Should be ready to read
#     print("accepted connection from", addr)
#     conn.setblocking(False)
#     auth_kdf2 = PBKDF2HMAC(
#         algorithm=hashes.SHA256(),
#         length=32,
#         salt=salt,
#         iterations=100000,
#         backend=default_backend()
#     )
#     f = Fernet(base64.urlsafe_b64encode(auth_kdf2.derive(keys["pre-auth"])))
#     connection = Connection(sel, conn, addr, f)
#     states[connection] = "pre-auth"
#     sel.register(conn, selectors.EVENT_READ, data=connection)
#     queue.enqueue((connection, "pass-auth"))
#     queue.enqueue((connection, "conn-auth"))
#     # pass_check = f.decrypt(conn.recv(1024))
#     # print(pass_check)
#     # if pass_phrase == pass_check:
#     #     # set new key
#     #     keys[conn] = f.decrypt((conn.recv(1024)))
#     #     print("Connection Authorized")
#
# #setup server
# lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# lsock.bind((HOST, PORT))
# lsock.setblocking(False)
# lsock.listen(5)
# print("listening on", (HOST, PORT))
# sel.register(lsock, selectors.EVENT_READ, data=None)
#
# server_state = True
# try:
#     while server_state:
#         events = sel.select(timeout=None)
#         for key, mask in events:
#             if key.data is None:
#                 accept_connection(key.fileobj)
#             else:
#                 connection = key.data
#                 try:
#                     connection.process_events(mask)
#
#                 except Exception:
#                     print(
#                         "main: error: exception for",
#                         f"{connection.address}:\n{traceback.format_exc()}",
#                     )
#                     connection.close()
#         # f = Fernet(auth_key)
#         # conn, addr = lsock.accept()
#         # print("Accepted Connection from ", addr)
#         #
#         #     auth_kdf2 = PBKDF2HMAC(
#         #         algorithm=hashes.SHA256(),
#         #         length=32,
#         #         salt=salt,
#         #         iterations=100000,
#         #         backend=default_backend()
#         #     )
#         #     f = Fernet(base64.urlsafe_b64encode(auth_kdf2.derive(keys[conn])))
#         #     while True:
#         #         try:
#         #             msg = f.decrypt(conn.recv(1024))
#         #             print(msg)
#         #         except ConnectionResetError as e:
#         #             print("Client Closed Unnaturally")
#         #             conn.close()
#         #             break
#         #         if msg == b"stop":
#         #             print("Connection Closed by client")
#         #             conn.close()
#         #             break
#         #         if msg == b'close':
#         #             print("Connection Closed by client")
#         #             server_state = False
#         #             conn.close()
#         #             break
#         # else:
#         #     print("Connection Rejected")
#         #     conn.close()
#         #     break
# finally:
#     print("closing the server")
#     lsock.close()
#


import selectors
import socket

import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

def close_connection(connection):
    connection.close()
    mysel.unregister(connection)
    # num_of_connections -= 1

def read(connection, mask):
    try:
        client_address = connection.getpeername()
        # print('read({})'.format(client_address))
        data = connection.recv(1024)
        print(data)
        if connections[connection] == "auth":
            un_data = fernets[connection].decrypt(data)
            print(un_data)
        if (connections[connection] == "pre-auth"):
            un_data = main_fernet.decrypt(data)
            auth_kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            fernets[connection] = Fernet(base64.urlsafe_b64encode(auth_kdf.derive(un_data)))
            connections[connection] = "auth"
        if (connections[connection] == "pre-auth-pre-pass"):
            un_data = main_fernet.decrypt(data)
            print(un_data)
            if un_data == pass_phrase:
                connections[connection] = "pre-auth"
            else:
                close_connection(connection)
                print("Connection failed to authenticate!")



    except ConnectionResetError:
        print("Client closed forcefully")
        close_connection(connection)


def accept(sock, mask):
    "Callback for new connections"
    new_connection, addr = sock.accept()
    # num_of_connections += 1
    print('accept({})'.format(addr))
    new_connection.setblocking(False)
    connections[new_connection] = "pre-auth-pre-pass"
    mysel.register(new_connection, selectors.EVENT_READ, read)



mysel = selectors.DefaultSelector()
keep_running = True
connections = {}
fernets = {}
auth_code = b'em1lia<3'
pass_phrase = b'coatrnae'
# num_of_connections = 0
salt = b'\x81u\xfd\xcb\xe4f\x02\r\xba\x13\xb0\x1f\x88\xd2\xa78'
auth_kdf2 = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
main_fernet = Fernet(base64.urlsafe_b64encode(auth_kdf2.derive(auth_code)))
server_address = ('localhost', 10000)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server.bind(server_address)
server.listen(5)
mysel.register(server, selectors.EVENT_READ, accept)
print('server listening on {}:{}'.format(*server_address))

while keep_running:
    for key, mask in mysel.select(timeout=None):
        callback = key.data
        callback(key.fileobj, mask)

print('shutting down')
mysel.close()