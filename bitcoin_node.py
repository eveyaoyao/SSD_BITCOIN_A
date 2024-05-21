# bitcoin_node.py
# Yueh-Yueh Yao D23125333
# This module handles the connection and communication with the Bitcoin node.

import socket
import struct
import time
import hashlib

# SHA-256 hashing.
def sha256d(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

# Connects to a Bitcoin node at the given IP and port.
# Returns a socket object if successful.
def connect_to_node(ip, port=8333):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        print(f"Connected to {ip}:{port}")
        return sock
    except Exception as e:
        print(f"Error connecting to node {ip}: {e}")
        return None

# Sends a version message to the connected Bitcoin node.
def send_version_payload(sock):
    version = 70015
    services = 0
    timestamp = int(time.time())
    addr_recv = b'\x00' * 26
    addr_from = b'\x00' * 26
    nonce = 0
    user_agent = b''
    start_height = 0
    relay = 1
    payload = struct.pack('<iQq26s26sQ?I?', version, services, timestamp, addr_recv, addr_from, nonce, len(user_agent), start_height, relay)
    magic = b'\xf9\xbe\xb4\xd9'
    command = b'version' + (b'\x00' * (12 - len(b'version')))
    length = struct.pack('<I', len(payload))
    checksum = sha256d(payload)[:4]
    message = magic + command + length + checksum + payload
    sock.sendall(message)
    print("Sent version payload")

# Sends a verack message to the connected Bitcoin node.
def send_verack_payload(sock):
    payload = b''
    magic = b'\xf9\xbe\xb4\xd9'
    command = b'verack' + (b'\x00' * (12 - len(b'verack')))
    length = struct.pack('<I', len(payload))
    checksum = sha256d(payload)[:4]
    message = magic + command + length + checksum + payload
    sock.sendall(message)
    print("Sent verack payload")

# Receives a message from the Bitcoin node.
# Returns the command and payload of the message.
def receive_message(sock):

    # Receives exactly n bytes from the socket.
    def recvall(sock, n):
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                raise ConnectionError("Connection lost")
            data += packet
        return data

    try:
        magic = recvall(sock, 4)
        command = recvall(sock, 12).strip(b'\x00')
        length = struct.unpack('<I', recvall(sock, 4))[0]
        checksum = recvall(sock, 4)
        payload = recvall(sock, length)
        print(f"Received command: {command}, length: {length}")
        return command, payload
    except Exception as e:
        print(f"Error receiving message: {e}")
        raise ConnectionError("Connection lost")

# Sends a getdata message to request specific data.
def send_getdata(sock, items):
    count = len(items)
    payload = struct.pack('<B', count)
    for item_type, item_hash in items:
        payload += struct.pack('<I', item_type) + item_hash
    magic = b'\xf9\xbe\xb4\xd9'
    command = b'getdata' + (b'\x00' * (12 - len(b'getdata')))
    length = struct.pack('<I', len(payload))
    checksum = sha256d(payload)[:4]
    message = magic + command + length + checksum + payload
    sock.sendall(message)
    print(f"Sent getdata payload for {count} items: {[item_hash.hex() for item_type, item_hash in items]}")

# Sends a pong message in response to a ping message.
def send_pong(sock, nonce):
    payload = nonce
    magic = b'\xf9\xbe\xb4\xd9'
    command = b'pong' + (b'\x00' * (12 - len(b'pong')))
    length = struct.pack('<I', len(payload))
    checksum = sha256d(payload)[:4]
    message = magic + command + length + checksum + payload
    sock.sendall(message)
    print("Sent pong payload")
