# okx-watcher

## Description

This script monitors the server where your automated trading runs.  
If the server becomes unresponsive, the script automatically cancels all open orders on OKX to prevent unwanted positions.

## How to install

1. Clone the repository:

```bash
   git clone https://github.com/marsky0/okx-watcher.git
   cd okx-watcher
````

2. Install the dependencies:

```bash
   pip install -r requirements.txt
```


## How to configure

Open the main script file (e.g., `main.py`) and fill in the parameters:

```python
api_key = "YOUR_API_KEY"
secret_key = "YOUR_SECRET_KEY"
passphrase = "YOUR_PASSPHRASE"
flag = "0"  # 0 — live mode, 1 — demo mode
inst_type = "SWAP"  # market type: SPOT, SWAP, FUTURES, etc.
server = "server_address_to_ping"
ping_interval = 5  # ping interval in seconds
```

## How to run

Run the script with:

```bash
python main.py
```

The script will start monitoring the server and cancel all open orders if the server becomes unreachable.
