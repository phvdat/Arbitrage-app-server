from fastapi import FastAPI, WebSocket
import asyncio
from services.ws_manager import WSManager

app = FastAPI()
manager = WSManager()

@app.websocket("/ws/orderbook")
async def ws_orderbook(websocket: WebSocket):
    await websocket.accept()
    
    # Chờ app gửi exchange + symbol
    params = await websocket.receive_json()
    exchange = params["exchange"]
    symbol = params["symbol"]

    # Forward data từ ccxt.pro về app
    async for data in manager.stream(exchange, symbol):
        await websocket.send_json(data)
