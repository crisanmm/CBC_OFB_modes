import socket
from config import cipher, initialization_vector, CBC, OFB

server_socket = socket.create_server(('', 5050))
nodeA, _ = server_socket.accept()

operation_block_mode = nodeA.recv(3).decode()

K_cipher = nodeA.recv(16)
K_plain = cipher.decrypt(K_cipher)

BlockMode = None
if operation_block_mode == 'CBC':
    BlockMode = CBC(initialization_vector, K_plain)
elif operation_block_mode == 'OFB':
    BlockMode = OFB(initialization_vector, K_plain)

blocks = []
nodeA.send(b'ok')
while cipher_block := nodeA.recv(16):
    plain_block = BlockMode.decrypt_block(cipher_block)
    blocks.append(plain_block)
nodeA.close()

last_block = blocks[-1]
del blocks[-1]
with open('NodeB_output.txt', "wb") as f:
    for block in blocks:
        f.write(block)
    f.write(last_block.rstrip())
