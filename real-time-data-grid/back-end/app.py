from quart import Quart, websocket

app = Quart(__name__)

# Store connected clients
clients = set()

@app.websocket('/ws')
async def ws():
    clients.add(websocket._get_current_object())
    try:
        while True:
            await websocket.receive()
    except:
        clients.remove(websocket._get_current_object())

async def broadcast(message):
    for client in clients:
        await client.send(message)

@app.route('/add_item', methods=['POST'])
async def add_item():
    item = await request.json()
    await broadcast(item)
    return '', 204

if __name__ == '__main__':
    app.run()

