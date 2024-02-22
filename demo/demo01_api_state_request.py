import asyncio
import json
import websockets

async def send_request():
    uri = "ws://localhost:8001"

    async with websockets.connect(uri) as websocket:
        request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "MyIDWithLessThan64Characters",
            "messageType": "APIStateRequest"
        }

        await websocket.send(json.dumps(request))

        response = await websocket.recv()
        print(f"Received: {response}")

asyncio.get_event_loop().run_until_complete(send_request())