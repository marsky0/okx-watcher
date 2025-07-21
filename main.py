import asyncio
import time
import traceback
from ping3 import ping
import okx.Trade as Trade

# --- Configuration ---
api_key = ""
secret_key = ""
passphrase = ""

flag = "0"  # live: "0", demo: "1"
inst_type = "SWAP"
server = ""  # IP or hostname to ping
ping_interval = 5  # seconds between pings

# --- Initialize OKX Trade API ---
tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)

# --- Ping the target server ---
async def is_server_alive():
    try:
        delay = ping(server, timeout=2)
        return delay is not None
    except Exception:
        return False

# --- Fetch all open orders with pagination ---
async def fetch_all_orders(instType="SWAP"):
    all_orders = []
    after = None

    while True:
        params = {"instType": instType, "limit": 100}
        if after:
            params["after"] = after

        resp = tradeAPI.get_order_list(**params)
        data = resp.get("data", [])
        if not data:
            break

        all_orders.extend(data)
        after = data[-1]["ordId"]

        if len(data) < 100:
            break

        await asyncio.sleep(0.05)  # wait briefly to avoid hitting rate limits

    return all_orders

# --- Cancel orders in batches (up to 20 at once) ---
async def cancel_orders_batch(orders):
    batch_size = 20
    for i in range(0, len(orders), batch_size):
        batch = orders[i:i + batch_size]
        orders_data = [{"instId": o["instId"], "ordId": o["ordId"]} for o in batch]
        try:
            response = tradeAPI.cancel_multiple_orders(orders_data)
            print(f"📦 Cancelled {len(orders_data)} orders →", response.get("msg", "success"))
        except Exception as e:
            print(f"⚠️ Error while cancelling batch:", e)
        await asyncio.sleep(0.1)  # avoid rate limits

# --- Main monitoring loop ---
async def monitor_and_cancel():
    while True:
        try:
            if await is_server_alive():
                print(f"[{time.strftime('%H:%M:%S')}] ✅ Server is reachable.")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] 🚨 Server is DOWN. Cancelling all orders...")
                orders = await fetch_all_orders(inst_type)
                print(f"🔍 Found {len(orders)} orders. Starting cancellation...")
                await cancel_orders_batch(orders)
            await asyncio.sleep(ping_interval)
        except Exception:
            traceback.print_exc()

# --- Entry point ---
if __name__ == "__main__":
    try:
        asyncio.run(monitor_and_cancel())
    except KeyboardInterrupt:
        print("⛔ Stopped manually.")
