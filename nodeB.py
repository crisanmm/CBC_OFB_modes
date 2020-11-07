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

nodeA.send(b'ok')
with open('nodeB_output.txt', 'wb') as f:
    current_block = last_block = b''
    while cipher_block := nodeA.recv(16):
        if last_block != b'':
            f.write(last_block)
        last_block = current_block
        current_block = BlockMode.decrypt_block(cipher_block)
    f.write(last_block)
    # remove padding from last block
    current_block = current_block.rstrip()
    f.write(current_block)

nodeA.close()
