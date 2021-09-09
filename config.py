from dataclasses import dataclass


@dataclass
class SqlConfig:
    host: str
    user: str
    password: str
    database: str


@dataclass
class RedisConfig:
    host: str
    port: str
    password: str


class Config:
    mysql = SqlConfig(
        host="localhost",
        user="anmol",
        password="123456789",
        database="leaderboards",
    )

    redis = RedisConfig(
        host="localhost",
        port="6379",
        password=""
    )
