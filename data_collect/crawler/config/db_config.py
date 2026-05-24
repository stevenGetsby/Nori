# -*- coding: utf-8 -*-


import os

# relation config
RELATION_DB_PWD = os.getenv("RELATION_DB_PWD", "123456")
RELATION_DB_USER = os.getenv("RELATION_DB_USER", "root")
RELATION_DB_HOST = os.getenv("RELATION_DB_HOST", "localhost")
RELATION_DB_PORT = int(os.getenv("RELATION_DB_PORT", 3306))
RELATION_DB_NAME = os.getenv("RELATION_DB_NAME", "media_crawler_pro")

# redis config
REDIS_DB_HOST = os.getenv("REDIS_DB_HOST", "127.0.0.1")  # your redis host
REDIS_DB_PWD = os.getenv("REDIS_DB_PWD", "123456")  # your redis password
REDIS_DB_PORT = os.getenv("REDIS_DB_PORT", 6379)  # your redis port
REDIS_DB_NUM = os.getenv("REDIS_DB_NUM", 0)  # your redis db num

# cache type
CACHE_TYPE_REDIS = "redis"
CACHE_TYPE_MEMORY = "memory"
USE_CACHE_TYPE = CACHE_TYPE_MEMORY # 本地开发用 memory，生产用 redis

# database type: "mysql" or "sqlite"
DB_TYPE = os.getenv("DB_TYPE", "sqlite")
# SQLite 数据库文件路径（DB_TYPE=sqlite 时生效）
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "./media_crawler.db")
