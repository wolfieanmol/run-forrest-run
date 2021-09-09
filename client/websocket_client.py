import _thread
import json
import threading
from queue import Queue

import websocket


class WebsocketClient:
    def __init__(self, host="localhost", port=5555):
        self.host = host
        self.port = port
        self.server_path = "ws://{host}:{port}".format(host=self.host, port=self.port)
        self.uri = ""

    def connect(self):
        ws = websocket.WebSocketApp(self.uri, on_open=self.on_open, on_close=self.on_close, on_message=self.on_message)
        wst = threading.Thread(target=ws.run_forever)
        wst.start()

    def on_open(self, ws):
        pass

    def on_message(self, ws, message):
        pass

    @staticmethod
    def on_close(ws):
        print("###closed###")


class WebsocketLeaderboard(WebsocketClient):
    def __init__(self):
        super(WebsocketLeaderboard, self).__init__()
        self.uri = f"{self.server_path}/leaderboard/top"
        self.top_leaderboard = {}
        self.connect()

    def on_message(self, ws, message):
        message = json.loads(message)
        if message.get("leaderboard") is not None:
            self.top_leaderboard = message["leaderboard"]


class WebsocketRank(WebsocketClient):
    def __init__(self, username):
        super(WebsocketRank, self).__init__()
        self.uri = f"{self.server_path}/leaderboard/rank"
        self.username = username
        self.message = None
        self.rank = ""
        self.score = ""
        self.connect()

    def on_message(self, ws, message):
        message = json.loads(message)

        if message.get("rank") is not None:
            self.rank = message["rank"]
            self.score = message["score"]

    def on_open(self, ws):
        ws.send(self.username)

    def send_message(self, message):
        self.message = message


class WebsocketUpdateScore(WebsocketClient):
    def __init__(self):
        super(WebsocketUpdateScore, self).__init__()
        self.uri = f"{self.server_path}/leaderboard/update-score"
        self.message = Queue()
        self.recv_message = None
        self.connect()

    def on_open(self, ws):
        def run(*args):
            while True:
                print("")
                if not self.message.empty():
                    ws.send(self.message.get())
                    # self.message.
        _thread.start_new_thread(run, ())

    def send_message(self, message):
        self.message.put(message)
