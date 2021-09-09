# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
# ====== END OF CONFIG SECTION ====== #

import flask
import flask_cors
import flask_restful

from LeaderboardApi.Api import routers
from LeaderboardApi.Api import settings

app = flask.Flask(__name__)
app.url_map.strict_slashes = False
cors = flask_cors.CORS(app, resources={r"/api/*": {"origins": "*"}})
api = flask_restful.Api(app)

router_route_pairs = (
    (routers.HealthCheck, "healthcheck"),
    (routers.Version, "version"),

    (routers.GetRank, "leaderboard/rank/<string:user_id>"),
    (routers.GetTopLeaderboard, "leaderboard/top/<string:num>"),
    (routers.UpdateScore, "leaderboard/update-score/<string:user_id>"),
    (routers.CheckAndCreateUser, "leaderboard/create-user/<string:user_id>"),

)

for router, route in router_route_pairs:
    api.add_resource(router, f"/api/v1/{route}")

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=settings.port)
