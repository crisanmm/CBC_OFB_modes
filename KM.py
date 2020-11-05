import socket
import Crypto.Random
from config import cipher

K_plain = Crypto.Random.get_random_bytes(cipher.block_size)
K_cipher = cipher.encrypt(K_plain)

server_socket = socket.create_server(('', 5051))
nodeA, _ = server_socket.accept()
bytes_sent = nodeA.send(K_cipher)
if bytes_sent == cipher.block_size:
    print('node KM: Successfully sent key to node A')
else:
    print('node KM: Failed sending key to node A')
nodeA.close()
