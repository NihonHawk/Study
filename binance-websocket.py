import websockets
import asyncio
import json
import requests 
from datetime import datetime as date


def get_current_max_price():
    end = json.loads(requests.get("https://api.binance.com/api/v3/time").text)['serverTime']
    start = int(end) - 60800 * 60
    url = f"https://api.binance.com/api/v3/klines?symbol=XRPUSDT&interval=1h&startTime={start}&endTime={end}"
    max_price = json.loads(requests.get(url).text)
    return float(max_price[0][2])


async def main(max_price):
    url = "wss://stream.binance.com:443/ws/xrpusdt@miniTicker"
    current_time = date.now().strftime("%H")
    async with websockets.connect(url) as client:
        while True:
            if current_time != date.now().strftime("%H"):  # обновление максимальной цены каждый час 
                current_time = date.now().strftime("%H")
                max_price = get_current_max_price()
            data = json.loads(await client.recv())
            if float(data['c']) * 100 / max_price <= 99:
                print(f"Цена упала на 1%: current = {float(data['c'])}; max = {max_price}")
            else:
                pass
                # print(f"current price - {float(data['c'])}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(get_current_max_price()))
