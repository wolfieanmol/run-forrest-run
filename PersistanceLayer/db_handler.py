import mysql.connector
from config import Config
# from config import C


class DbHandler:
    def __init__(self):
        self.__host = Config.mysql.host
        self.__user = Config.mysql.user
        self.__password = Config.mysql.password
        self.__database = Config.mysql.database
        self.__conn = self.connect()
        self.__cursor = self.__conn.cursor()

    def connect(self):
        return mysql.connector.connect(
            host=self.__host,
            user=self.__user,
            passwd=self.__password,
            database=self.__database
        )

    def create_database(self):
        self.__cursor.execute("CREATE DATABASE leaderboards")

    def show_db(self):
        self.__cursor.execute("SHOW DATABASES")
        for db in self.__cursor:
            print(db)

    def create_table(self):
        query = "CREATE TABLE user_points (id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(20), points INT)"
        self.__cursor.execute(query)

    def insert_user_point(self, user_id: str, points: int = 10):
        query = "INSERT INTO user_points(username, points) VALUES('{}', {})".format(user_id, points)
        self.__cursor.execute(query)
        self.__conn.commit()

    def select_all(self):
        self.__cursor.execute("SELECT * FROM user_points")
        for d in self.__cursor:
            print(d)

    def get_total_scores(self):
        query = "SELECT username, SUM(points) AS score FROM user_points GROUP BY username ORDER BY score desc"
        self.__cursor.execute(query)
        rows = self.__cursor.fetchall()
        return rows