import time
import requests
import csv
import asyncio
import websockets

def fetch_nifty50_price():
    headers = {
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'en-GB,en-IN;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
    }
    cookies = 'B6BFDA8E070252737167D55371ED3DD~YAAQNMMzuBEarvCNAQAAIQP0DBe4ndEc5z8Olwoq1BAtb2rOctJtccTiliLYtMNQ8knwr1QI8FkeboS1GIguADW20x1DXY4B20cUSQ5ItrU9J9F1zIstVprOWq6uvZfeJWd/txwEUEyGvTKxsDNCKhVOvcgeTGinWvejm2w++AW/4o6naq/6Kvk0gq0IjcsmqrY+i1u1YIl6uwSkqL+KIMcgWOphtAjnyRs/7gdRAUF2PDqhOV0d1sFLnKXv2/VnwDlv~1'
    url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050'
    response = requests.get(url, headers=headers, cookies={'cookie': cookies})
    if response.status_code == 200:
        data = response.json()
        timestamp = int(time.time())  # Current timestamp
        return {'timestamp': timestamp, 'price': data['data'][0]['lastPrice']}
    return None

async def serve_csv(websocket, path):
    while True:
        price_data = fetch_nifty50_price()
        if price_data is not None:
            await websocket.send(str(price_data['timestamp']) + ',' + str(price_data['price']))
        await asyncio.sleep(10)  

start_server = websockets.serve(serve_csv, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
