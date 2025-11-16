import ccxt.pro as ccxtpro
import asyncio

class WSManager:
    def __init__(self):
        self.exchanges = {
            "binance": ccxtpro.binance({'enableRateLimit': False}),
            "bingx": ccxtpro.bingx({'enableRateLimit': False}),
            "bitmart": ccxtpro.bitmart({'enableRateLimit': False}),
            "mexc": ccxtpro.mexc({'enableRateLimit': False}),
            "okx": ccxtpro.okx({'enableRateLimit': False}),
        }

    async def stream(self, exchange: str, symbol: str):
        ex = self.exchanges.get(exchange)
        if ex is None:
            raise Exception(f"Exchange {exchange} not supported")

        # Kết nối WebSocket từ sàn
        while True:
            try:
                ob = await ex.watch_order_book(symbol)

                yield {
                    "bids": ob["bids"][:10],
                    "asks": ob["asks"][:10],
                    "timestamp": ob.get("timestamp"),
                    "datetime": ob.get("datetime"),
                    "exchange": exchange,
                    "symbol": symbol,
                }

            except Exception as e:
                print("WS error:", e)
                await asyncio.sleep(1)  # retry
