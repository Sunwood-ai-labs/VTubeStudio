import asyncio
import json
import websockets

import sys
import pprint

pprint.pprint(sys.path)


import os
import sys
import random
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../api'))

from api.authentication import request_authentication_token, authenticate_plugin

async def get_hotkeys(websocket):
    request = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "UniqueRequestIDForHotkeys",
        "messageType": "HotkeysInCurrentModelRequest",
        "data": {}
    }
    await websocket.send(json.dumps(request))
    response = await websocket.recv()
    response_json = json.loads(response)
    if "data" in response_json and "availableHotkeys" in response_json["data"]:
        return response_json["data"]["availableHotkeys"]
    return []

async def trigger_random_hotkey(websocket, hotkeys):
    if hotkeys:
        hotkey = random.choice(hotkeys)
        hotkey_id = hotkey.get("hotkeyID")
        if hotkey_id:
            request = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "UniqueRequestIDForTriggering",
                "messageType": "HotkeyTriggerRequest",
                "data": {
                    "hotkeyID": hotkey_id
                }
            }
            await websocket.send(json.dumps(request))
            response = await websocket.recv()
            print(f"Triggered Hotkey Response: {response}")

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
                # ホットキーのリスト取得
                hotkeys = await get_hotkeys(websocket)
                print(">>>> hotkeys >>>>")
                pprint.pprint(hotkeys)
                # ランダムにホットキーをトリガー
                await trigger_random_hotkey(websocket, hotkeys)

                time.sleep(5)

                await trigger_random_hotkey(websocket, hotkeys)
        else:
            print("Token request failed")

# asyncio.runを使用してメイン関数を実行
asyncio.run(main())
