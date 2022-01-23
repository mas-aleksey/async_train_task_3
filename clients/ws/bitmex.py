import aiohttp
import json


async def fetch_10() -> list[float]:
    result = []
    async with aiohttp.ClientSession() as session:
        ws = await session.ws_connect('wss://ws.bitmex.com/realtime?subscribe=instrument:XBTUSD')
        async for msg in ws:
            payload = json.loads(msg.data)
            data = payload.get('data', [])
            if not isinstance(data, list):
                continue
            for item in data:
                price = item.get('fairPrice')
                if price:
                    print('price', price)
                    result.append(price) 
            if len(result) >= 10:
                break
    return result
