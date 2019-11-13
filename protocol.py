import asyncio
import websockets

class ProtocolStateMachine:
    def __init__(self, name):
        self._name = name

class ProtocolV1:
    def __init__(self):
        self._connections = dict()
        print(f"LOG: CREATED PROTOCOL")

    async def initialize(self, websocket, path):
        print(f"LOG: INITIALIZING")
        await self.connect(websocket, path)

    async def connect(self, websocket, path):
        name = await websocket.recv()

        print(f"LOG: CLIENT NAME {name}")
        self._connections[name] = ProtocolStateMachine(name)

        await websocket.send("CONNECTED")

        await self.handle_message(websocket, path)

    async def handle_message(self, websocket, path):
        message = await websocket.recv()
        
        if message == "LIST":
            for i in range(4):
                await websocket.send(f"DEVICE {i}")

if __name__ == "__main__":
    protocol = ProtocolV1()
    start_server = websockets.serve(protocol.initialize, "localhost", 1234)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

