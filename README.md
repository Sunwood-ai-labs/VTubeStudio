# VTube Studio APIを使ったPythonデモ

このガイドでは、VTube StudioのAPIを使用して、PythonからVTube Studioを操作する基本的な方法を紹介します。ここでは、VTube Studioとの接続設定、認証プロセス、ホットキーの取得と実行などのデモを行います。
## 前提条件

このデモを実行する前に、以下のツールがインストールされていることを確認してください。
- Python 3.x
- websockets
- pygame

これらは以下のコマンドでインストールできます。

```shell
pip install websockets pygame
```


## デモの概要 
1. **API状態の確認** ：VTube StudioのAPIの状態を確認します。 
2. **認証プロセス** ：VTube Studioとの認証を行います。 
3. **ホットキーの取得** ：現在のモデルに設定されているホットキーのリストを取得します。 
4. **ホットキーのランダム実行** ：取得したホットキーの中からランダムに一つ選び、実行します。
## デモの実行
### デモ1: API状態の確認

ファイル名：`demo01_api_state_request.py`


実行コマンド：

```shell
(vts) C:\Prj\VTubeStudio>python demo\demo01_api_state_request.py
```



実行結果例：

```vbnet
Received: {"apiName":"VTubeStudioPublicAPI","apiVersion":"1.0","timestamp":1708940896655,"messageType":"APIStateResponse","requestID":"MyIDWithLessThan64Characters","data":{"active":true,"vTubeStudioVersion":"1.28.15","currentSessionAuthenticated":false}}
```


### デモ2: 認証プロセス

ファイル名：`demo02_vts_auth.py`


実行コマンド：

```shell
(vts) C:\Prj\VTubeStudio>python demo\demo02_vts_auth.py
```



実行結果例：

```vbnet
Token: f0986439e8c28e410d2fd3679945f5f85f2a61322ed662e2973998c167adac8e
Authenticated: True
```


### デモ3: ホットキーの取得

ファイル名：`demo03_get_hotkeys.py`


実行コマンド：

```shell
(vts) C:\Prj\VTubeStudio>python demo\demo03_get_hotkeys.py
```



実行結果例：

```vbnet
Authenticated: True
Received: {"apiName":"VTubeStudioPublicAPI","apiVersion":"1.0",...}
```


### デモ4: ホットキーのランダム実行

ファイル名：`demo04_rnd_hotkey.py`



実行コマンド：

```shell
(vts) C:\Prj\VTubeStudio>python demo\demo04_rnd_hotkey.py
```


実行結果例：

```css
Triggered Hotkey Response: {"apiName":"VTubeStudioPublicAPI","apiVersion":"1.0","timestamp":1708941090369,"messageType":"HotkeyTriggerResponse","requestID":"UniqueRequestIDForTriggering","data":{"hotkeyID":"c7695e263334443282c7ec92b5f47d88"}}
```
