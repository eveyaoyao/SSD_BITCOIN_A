# Bitcoin Block Viewer

Bitcoin Block Viewer is a Python application that connects to a Bitcoin node, receives blocks and transactions, and displays the information in a graphical user interface (GUI).

## Features

- Connect to a Bitcoin node
- Receive and display block information
- Receive and display transaction information
- Simple GUI for viewing block and transaction details

## File Descriptions

- `bitcoin_node.py`: Handles connection and communication with the Bitcoin node.

  - Functions for sending and receiving messages.
  - Functions for handling Bitcoin protocol commands such as `version`, `verack`, `ping`, and `getdata`.

- `bitcoin_parser.py`: Parses Bitcoin protocol messages.

  - Functions for parsing inventory (`inv`), block, and transaction payloads.
  - Functions for parsing detailed block and transaction information.

- `bitcoin_gui.py`: Creates and updates the GUI.

  - Functions for displaying block information and transaction information in a text widget.
  - Function for creating the main GUI window with a scrolled text widget.

- `main.py`: Main entry point for the application.
  - Handles the overall logic for connecting to the Bitcoin node, receiving messages, and updating the GUI.
  - Starts the application and GUI, and manages message handling in a separate thread.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/eveyaoyao/SSD_BITCOIN_A.git
   ```

2. **Install the required libraries**:
   Make sure you have `tkinter` and `struct` installed in your Python environment. These libraries are typically included with standard Python installations. If you're using a virtual environment, activate it before installing dependencies.

3. **Run the application**:
   ```bash
   python main.py
   ```

## Usage

1. Run `main.py` to start the application.
2. The application will connect to a Bitcoin node using a hardcoded IP address.
3. The GUI will display block and transaction information as they are received from the node.

## Code Overview

### `bitcoin_node.py`

This module handles the connection and communication with the Bitcoin node. It includes functions for sending and receiving messages, and various Bitcoin protocol commands.

### `bitcoin_parser.py`

This module handles the parsing of various Bitcoin protocol messages. It includes functions for parsing inventory (`inv`), block, and transaction payloads.

### `bitcoin_gui.py`

This module handles the creation and updating of the GUI for displaying Bitcoin block and transaction information. It includes functions for displaying block and transaction details in a text widget.

### `main.py`

This is the main entry point for the Bitcoin Block Viewer application. It handles the overall logic for connecting to the Bitcoin node, receiving messages, and updating the GUI.
