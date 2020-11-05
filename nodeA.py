import socket
import random
from config import cipher, initialization_vector, CBC, OFB

BLOCK_MODE = {'CBC', 'OFB'}
operation_block_mode, = random.sample(BLOCK_MODE, k=1)
print(f'Block mode chosen by node A: {operation_block_mode}')

nodeKM = socket.create_connection(('127.0.0.1', 5051))
K_cipher = nodeKM.recv(16)
nodeKM.close()

nodeB = socket.create_connection(('127.0.0.1', 5050))
nodeB.send(operation_block_mode.encode())
nodeB.send(K_cipher)

K_plain = cipher.decrypt(K_cipher)

BlockMode = None
if operation_block_mode == 'CBC':
    BlockMode = CBC(initialization_vector, K_plain)
elif operation_block_mode == 'OFB':
    BlockMode = OFB(initialization_vector, K_plain)

msg = nodeB.recv(2)
if msg == b'ok':
    with open('test.txt', 'rb') as f:
        while plain_block := f.read(cipher.block_size):
            if len(plain_block) < cipher.block_size:
                plain_block = plain_block + (b' ' * (cipher.block_size - len(plain_block)))
            cipher_block = BlockMode.encrypt_block(plain_block)
            nodeB.send(cipher_block)

nodeB.close()
