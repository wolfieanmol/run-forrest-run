# Run Forrest Online Multiplayer Game

##steps to setup:

###installing dependencies
- install python 3.8
- install redis
- install mysql

### setup python environment
- create virtual env
- go to game directory and run: <br> `pip install -r requirements.txt`
###Setup DB and redis
- export db (note if it is taking too long use `leaderboards_small.sql`):<br> `mysqldump -u [your_username] -p [your_database_name] < leaderboards.sql`
- run "export_to_redis" to transfer to redis cache: <br> `python export_to_redis.py`
- open config.py to change mysql and redis configuration
- can run `utils/create_mock_data.py` to add more entries in db
### Run server
`python run_server.py`
### Run game
`python game.py`

# How to play game
- press spaacebar to run
- press escape to quit
- Rank and Score is available on top left
- Top 5 leaderboards are available on top right