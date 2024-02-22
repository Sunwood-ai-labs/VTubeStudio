import asyncio
import json
import websockets

async def request_token(websocket, plugin_name, plugin_developer, plugin_icon=None):
    request = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "TokenRequestID",
        "messageType": "AuthenticationTokenRequest",
        "data": {
            "pluginName": plugin_name,
            "pluginDeveloper": plugin_developer,
            "pluginIcon": plugin_icon
        }
    }

    await websocket.send(json.dumps(request))
    response = await websocket.recv()
    json_response = json.loads(response)
    
    if json_response["messageType"] == "AuthenticationTokenResponse":
        return json_response["data"]["authenticationToken"]
    else:
        return None

async def authenticate(websocket, plugin_name, plugin_developer, authentication_token):
    request = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "AuthenticationRequestID",
        "messageType": "AuthenticationRequest",
        "data": {
            "pluginName": plugin_name,
            "pluginDeveloper": plugin_developer,
            "authenticationToken": authentication_token
        }
    }

    await websocket.send(json.dumps(request))
    response = await websocket.recv()
    json_response = json.loads(response)

    if json_response["messageType"] == "AuthenticationResponse":
        return json_response["data"]["authenticated"]
    else:
        return False

async def main():
    uri = "ws://localhost:8001"
    async with websockets.connect(uri) as websocket:
        plugin_name = "My Cool Plugin"
        plugin_developer = "My Name"
        authentication_token = await request_token(websocket, plugin_name, plugin_developer)

        if authentication_token:
            print(f"Token: {authentication_token}")
            is_authenticated = await authenticate(websocket, plugin_name, plugin_developer, authentication_token)
            print(f"Authenticated: {is_authenticated}")
        else:
            print("Token request failed")

asyncio.get_event_loop().run_until_complete(main())