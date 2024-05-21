# bitcoin_parser.py
# Yueh-Yueh Yao D23125333
# This module handles the parsing of various Bitcoin protocol messages.

import struct
import time
import hashlib

# SHA-256 hashing.
def double_sha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

# Parses an inv payload, returns a list of items.
def parse_inv_payload(payload):
    count = struct.unpack('<B', payload[:1])[0]
    items = []
    offset = 1
    for _ in range(count):
        item_type = struct.unpack('<I', payload[offset:offset+4])[0]
        item_hash = payload[offset+4:offset+36]
        items.append((item_type, item_hash))
        if item_type == 1:
            print(f"Transaction: {item_hash.hex()}")
        elif item_type == 2:
            print(f"Block: {item_hash.hex()}")
        offset += 36
    print(f"Parsed {count} items from inv payload")
    return items

# Parses a block payload, returns a dictionary with block details.
def parse_block_payload(payload):
    block_data = {}
    block_data['version'] = struct.unpack('<I', payload[:4])[0]
    block_data['previous_block_hash'] = payload[4:36].hex()
    block_data['merkle_root'] = payload[36:68].hex()
    block_data['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(struct.unpack('<I', payload[68:72])[0]))
    block_data['difficulty'] = struct.unpack('<I', payload[72:76])[0]
    block_data['nonce'] = struct.unpack('<I', payload[76:80])[0]
    print("Parsed block payload")
    return block_data

# Parses transactions from a block payload, returns a list of transactions.
def parse_transactions(payload):
    transactions = []
    offset = 80  # Assume block header ends at offset 80
    tx_count = struct.unpack('<B', payload[offset:offset+1])[0]
    offset += 1
    print(f"Parsing {tx_count} transactions...")
    for _ in range(tx_count):
        txid = payload[offset:offset+32].hex()
        value = struct.unpack('<Q', payload[offset+32:offset+40])[0] / 1e8
        transactions.append({'txid': txid, 'value': value})
        offset += 40  # Assume each transaction has a fixed length of 40 bytes
    return transactions

# Parses a single transaction payload, returns a dictionary with transaction details.
def parse_transaction(payload):
    tx_data = {}
    tx_data['version'] = struct.unpack('<I', payload[:4])[0]
    offset = 4

    # Parse inputs
    tx_data['inputs'] = []
    num_inputs = payload[offset]
    offset += 1
    for _ in range(num_inputs):
        input_data = {}
        input_data['prev_txid'] = payload[offset:offset+32].hex()
        offset += 32
        input_data['prev_out_index'] = struct.unpack('<I', payload[offset:offset+4])[0]
        offset += 4
        script_len = payload[offset]
        offset += 1
        input_data['script'] = payload[offset:offset+script_len].hex()
        offset += script_len
        input_data['sequence'] = struct.unpack('<I', payload[offset:offset+4])[0]
        offset += 4
        tx_data['inputs'].append(input_data)

    # Parse outputs
    tx_data['outputs'] = []
    num_outputs = payload[offset]
    offset += 1
    for _ in range(num_outputs):
        output_data = {}
        output_data['value'] = struct.unpack('<Q', payload[offset:offset+8])[0] / 1e8
        offset += 8
        script_len = payload[offset]
        offset += 1
        output_data['script'] = payload[offset:offset+script_len].hex()
        offset += script_len
        tx_data['outputs'].append(output_data)

    tx_data['locktime'] = struct.unpack('<I', payload[offset:offset+4])[0]
    tx_data['txid'] = double_sha256(payload).hex()

    return tx_data
