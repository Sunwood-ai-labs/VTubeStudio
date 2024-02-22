import asyncio
import json
import websockets

import sys
import pprint

pprint.pprint(sys.path)


import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../api'))

from api.authentication import request_authentication_token, authenticate_plugin


async def get_hotkeys(websocket, model_id=None, live2d_item_filename=None):
    request = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "UniqueRequestIDLessThan64Characters",
        "messageType": "HotkeysInCurrentModelRequest",
        "data": {}
    }

    if model_id is not None:
        request["data"]["modelID"] = model_id

    if live2d_item_filename is not None:
        request["data"]["live2DItemFileName"] = live2d_item_filename

    await websocket.send(json.dumps(request))
    response = await websocket.recv()
    print(f"Received: {response}")
    pprint.pprint(response)

async def main():
    uri = "ws://localhost:8001"
    async with websockets.connect(uri) as websocket:
        plugin_name = "My Cool Plugin"
        plugin_developer = "My Name"
        # 認証トークンの取得
        authentication_token = await request_authentication_token(websocket, plugin_name, plugin_developer)

        if authentication_token:
            print(f"Token: {authentication_token}")
            # 認証の実施
            is_authenticated = await authenticate_plugin(websocket, plugin_name, plugin_developer, authentication_token)
            print(f"Authenticated: {is_authenticated}")
            if is_authenticated:
                # ホットキーの取得
                await get_hotkeys(websocket)
        else:
            print("Token request failed")

# asyncio.runを使用してメイン関数を実行
asyncio.run(main())
