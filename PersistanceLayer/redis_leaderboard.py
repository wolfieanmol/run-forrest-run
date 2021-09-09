import redis

from PersistanceLayer.db_handler import DbHandler
from config import Config


class Leaderboard:
    def __init__(self):
        self.__redis_host = Config.redis.host
        self.__redis_port = Config.redis.port
        self.__redis_password = Config.redis.password
        self.r = self.__connect()

    def __connect(self):
        try:
            r = redis.StrictRedis(host=self.__redis_host, port=self.__redis_port, password=self.__redis_password, decode_responses=True)
            return r
        except Exception as e:
            print(e)

    def configure_redis(self):
        self.__flush()
        self.__load_redis()

    def __flush(self):
        self.r.flushdb()

    def __load_redis(self):
        db = DbHandler()
        scores = db.get_total_scores()
        for user, score in scores:
            self.add_user(user, int(score))

    def add_user(self, user_id, score=0):
        self.r.zadd("leaderboard", {user_id: score})

    def update_score(self, user_id, inc_by=10):
        self.r.zincrby("leaderboard", inc_by, user_id)

    def get_top_n(self, n):
        x = self.r.zrevrange("leaderboard", 0, n, withscores=True)
        return x

    def get_rank(self, user_id):
        rank = self.r.zrevrank("leaderboard", user_id)
        if rank is not None:
            return rank + 1
        else:
            return -1

    def get_score(self, user_id):
        score = self.r.zscore("leaderboard", user_id)
        return score

if __name__ == '__main__':
    l = Leaderboard()
    l.get_score("anmol_3223")