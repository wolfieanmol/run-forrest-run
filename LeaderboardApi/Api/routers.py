import logging

import flask_restful
from PersistanceLayer.redis_leaderboard import Leaderboard

from LeaderboardApi.Api import settings

logger = logging.getLogger(__name__)


class Resource(flask_restful.Resource):
    pass


class HealthCheck(Resource):
    def get(self):
        return None, 200


class Version(Resource):
    def get(self):
        return settings.version_endpoint_payload, 200


class GetRank(Resource):
    def get(self, user_id):
        try:
            l = Leaderboard()
            return l.get_rank(user_id)
        except Exception as e:
            logger.exception(repr(e))

            return {"message": "Failed to process request."}, 400


class GetTopLeaderboard(Resource):
    def get(self, num):
        try:
            l = Leaderboard()
            top_scorers = l.get_top_n(num)
            top_scorers = [(x[0], [i + 1, x[1]]) for i, x in enumerate(top_scorers)]
            return dict(top_scorers)
        except Exception as e:
            logger.exception(repr(e))

            return {"message": "Failed to process request."}, 400


class UpdateScore(Resource):
    def post(self, num):
        try:
            l = Leaderboard()
            l.update_score()
            top_scorers = l.get_top_n(num)
            top_scorers = [(x[0], [i + 1, x[1]]) for i, x in enumerate(top_scorers)]
            return dict(top_scorers)
        except Exception as e:
            logger.exception(repr(e))

            return {"message": "Failed to process request."}, 400


class CheckAndCreateUser(Resource):
    def put(self, user_id):
        try:
            l = Leaderboard()
            rank = l.get_rank(user_id)
            if rank:
                return {"message": "user exists"}
            else:
                l.add_user(user_id, 0)
                return {"message": "user created"}
        except Exception as e:
            logger.exception(repr(e))

            return {"message": "Failed to process request."}, 400
