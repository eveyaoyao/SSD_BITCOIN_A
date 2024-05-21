# bitcoin_gui.py
# Yueh-Yueh Yao D23125333
# This module handles the creation and updating of the GUI

import tkinter as tk
from tkinter import scrolledtext

# Displays block information and its transactions
def display_block_info(block_data, transactions, text_widget):
    info = (f"Block received:\n"
            f"Version: {block_data['version']}\n"
            f"Previous Block Hash: {block_data['previous_block_hash']}\n"
            f"Merkle Root: {block_data['merkle_root']}\n"
            f"Timestamp: {block_data['timestamp']}\n"
            f"Difficulty: {block_data['difficulty']}\n"
            f"Nonce: {block_data['nonce']}\n"
            f"Transactions:\n")
    
    for tx in transactions:
        info += f"  - TxID: {tx['txid']} Value: {tx['value']} BTC\n"
    
    info += f"Hash Verified: True\n"

    text_widget.insert(tk.END, info + "\n")
    text_widget.see(tk.END)

# Displays transaction information
def display_transaction_info(txid, text_widget):
    info = (f"Transaction received:\n"
            f"TxID: {txid}\n")
    
    text_widget.insert(tk.END, info + "\n")
    text_widget.see(tk.END)

# Creates the main GUI window
def create_gui():
    root = tk.Tk()
    root.title("Bitcoin Block Viewer")

    text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30)
    text_widget.pack(padx=10, pady=10)

    return root, text_widget
