import asyncio
import json
import os
import re
import random
import websockets
from pygame import mixer
import sys

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

# オーディオファイルを順に再生し、再生後にランダムなホットキーをトリガーする関数
async def play_audio_and_trigger_hotkeys(websocket, folder_path='audio/Word2Motion'):
    files = [file for file in os.listdir(folder_path) if file.endswith('.wav')]
    sorted_files = sorted(files, key=lambda file: int(re.search(r'\d+', file).group()) if re.search(r'\d+', file) else 0)

    mixer.init()  # pygameのmixerモジュールを初期化
    for file in sorted_files:
        file_path = os.path.join(folder_path, file)
        print(f"再生中: {file}")
        mixer.music.load(file_path)
        mixer.music.play()
        while mixer.music.get_busy():  # ファイルの再生が完了するのを待つ
            await asyncio.sleep(1)
        await trigger_random_hotkey(websocket, await get_hotkeys(websocket))  # 再生後にランダムなホットキーをトリガー

async def main():
    uri = "ws://localhost:8001"
    async with websockets.connect(uri) as websocket:
        plugin_name = "My Cool Plugin"
        plugin_developer = "My Name"
        authentication_token = await request_authentication_token(websocket, plugin_name, plugin_developer)
        if authentication_token:
            print(f"Token: {authentication_token}")
            is_authenticated = await authenticate_plugin(websocket, plugin_name, plugin_developer, authentication_token)
            print(f"Authenticated: {is_authenticated}")
            if is_authenticated:
                await play_audio_and_trigger_hotkeys(websocket)  # オーディオ再生とホットキーのトリガー

asyncio.run(main())
