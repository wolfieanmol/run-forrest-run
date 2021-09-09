import json

import websockets
import asyncio

from PersistanceLayer.redis_leaderboard import Leaderboard


class LeaderboardServer:
    def __init__(self, host="localhost", port=5555):
        self.host = host
        self.port = 5555
        self.server = None
        self.clients = set()
        self.client_username = []
        self.start_server()

    def start_server(self):
        self.server = websockets.serve(self.handler, host=self.host, port=self.port)
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()

    async def handler(self, websocket, path):
        print("connected: ", path)
        self.clients.add(websocket)
        try:
            if path == "/leaderboard/top":
                await self.top_leaderboards(websocket)
            elif path == "/leaderboard/rank":
                await self.get_rank(websocket)
            elif path == "/leaderboard/update-score":
                await self.update_score(websocket)
        except Exception as e:
            print("client disconnected", e)
            self.clients.remove(websocket)

    # async def top_leaderboards(websocket, path):
    #     pass

    async def top_leaderboards(self, websocket):
        l = Leaderboard()
        while True:
            await asyncio.sleep(2)
            top_scorers = l.get_top_n(5)
            top_scorers = [(x[0], [i + 1, x[1]]) for i, x in enumerate(top_scorers)]
            response = dict(top_scorers)
            response = json.dumps({"leaderboard": response})
            # print(response)
            for client in self.clients:
                await client.send(response)

    async def setup_username(self, websocket):
        async for message in websocket:
            # print(message, " receieved setup_username")
            username = message
            self.client_username.append((websocket, username))
            break

    async def get_rank(self, websocket):
        await self.setup_username(websocket)
        l = Leaderboard()
        while True:
            await asyncio.sleep(2)
            for client, username in self.client_username:
                if client in self.clients:
                    rank = l.get_rank(username)
                    score = l.get_score(username)
                    response = json.dumps({"rank": rank, "score": score})
                    print(response)
                    await client.send(response)

    async def update_score(self, websocket):
        async for message in websocket:
            # print(message, " update_score")
            username = message
            l = Leaderboard()
            l.update_score(username, 10)


if __name__ == '__main__':
    leaderboard_server = LeaderboardServer()
