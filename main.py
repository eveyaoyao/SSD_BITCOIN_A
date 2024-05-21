# main.py
# Yueh-Yueh Yao D23125333
# This is the main entry point for the Bitcoin Block Viewer application.

import threading
from bitcoin_node import connect_to_node, send_version_payload, send_verack_payload, receive_message, send_getdata, send_pong
from bitcoin_parser import parse_inv_payload, parse_block_payload, parse_transactions, parse_transaction
from bitcoin_gui import display_block_info, display_transaction_info, create_gui

# Handles a ping message by sending a pong response.
def handle_ping(sock, payload):
    nonce = payload[:8]
    send_pong(sock, nonce)
    print("Handled ping payload")

# Main function to start the Bitcoin Block Viewer application.
def main():
    ip = "84.247.182.229"  # The IP address of the Bitcoin node to connect to
    print(f"Connecting to Bitcoin node at {ip}")
    sock = connect_to_node(ip)
    if not sock:
        print("Failed to connect to Bitcoin node")
        return

    send_version_payload(sock)

    root, text_widget = create_gui()

    def receive_blocks():
        # Receives and processes messages
        while True:
            try:
                command, payload = receive_message(sock)
                if command == b'version':
                    print("Received version payload")
                    send_verack_payload(sock)
                elif command == b'verack':
                    print("Received verack payload")
                elif command == b'inv':
                    print("Received inv payload")
                    items = parse_inv_payload(payload)
                    block_requests = []
                    for item in items:
                        if item[0] == 2:  # 2 indicates a block
                            print(f"Block: {item[1].hex()}")
                            block_requests.append(item)
                        else:
                            print(f"Transaction: {item[1].hex()}")
                            display_transaction_info(item[1].hex(), text_widget)
                    if block_requests:
                        send_getdata(sock, block_requests)
                elif command == b'block':
                    print(f"Received block payload with length: {len(payload)}")
                    block_data = parse_block_payload(payload)
                    transactions = parse_transactions(payload)
                    display_block_info(block_data, transactions, text_widget)
                elif command == b'tx':
                    print("Received transaction payload")
                    tx_data = parse_transaction(payload)
                    display_transaction_info(tx_data['txid'], text_widget)
                elif command == b'sendcmpct':
                    print("Handling sendcmpct payload")
                elif command == b'ping':
                    handle_ping(sock, payload)
                elif command == b'feefilter':
                    print("Handling feefilter payload")
                else:
                    print(f"Unhandled command: {command}")
            except ConnectionError as e:
                print(f"Connection error: {e}")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                break

    threading.Thread(target=receive_blocks, daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    main()
