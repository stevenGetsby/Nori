# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-
# @Author  : relakkes@gmail.com
# @Time    : 2024/4/6 14:54
# @Desc    : mediacrawler db 管理（支持 MySQL 和 SQLite）
import asyncio

import aiofiles
import aiomysql

import data_collect.crawler.config as config
from data_collect.crawler.async_db import AbstractAsyncDB, AsyncMysqlDB, AsyncSQLiteDB
from data_collect.crawler.pkg.tools import utils
from data_collect.crawler.var import db_conn_pool_var, media_crawler_db_var


async def init_mediacrawler_db():
    """
    初始化 MySQL 数据库链接池对象，并将该对象塞给 media_crawler_db_var 上下文变量
    """
    pool = await aiomysql.create_pool(
        host=config.RELATION_DB_HOST,
        port=config.RELATION_DB_PORT,
        user=config.RELATION_DB_USER,
        password=config.RELATION_DB_PWD,
        db=config.RELATION_DB_NAME,
        autocommit=True,
    )
    async_db_obj = AsyncMysqlDB(pool)

    # 将连接池对象和封装的CRUD sql接口对象放到上下文变量中
    db_conn_pool_var.set(pool)
    media_crawler_db_var.set(async_db_obj)


async def init_sqlite_db():
    """
    初始化 SQLite 数据库连接对象，并将该对象塞给 media_crawler_db_var 上下文变量
    """
    async_db_obj = AsyncSQLiteDB(config.SQLITE_DB_PATH)
    await async_db_obj.connect()
    media_crawler_db_var.set(async_db_obj)


async def init_db():
    """
    初始化 db 连接，根据 DB_TYPE 配置选择 MySQL 或 SQLite
    """
    utils.logger.info(f"[init_db] start init mediacrawler db connect object, DB_TYPE={config.DB_TYPE}")
    if config.DB_TYPE == "sqlite":
        await init_sqlite_db()
    else:
        await init_mediacrawler_db()
    await init_table_schema()
    utils.logger.info("[init_db] end init mediacrawler db connect object")


async def close():
    """
    关闭数据库连接/连接池
    """
    utils.logger.info("[close] close mediacrawler db connection")
    if config.DB_TYPE == "sqlite":
        async_db_obj: AbstractAsyncDB = media_crawler_db_var.get(None)
        if async_db_obj is not None and isinstance(async_db_obj, AsyncSQLiteDB):
            await async_db_obj.close()
    else:
        db_pool = db_conn_pool_var.get(None)
        if db_pool is not None:
            db_pool.close()


async def init_table_schema():
    """
    初始化数据库表结构。首次运行时自动建表，已有表则跳过。
    支持 MySQL 和 SQLite 两种模式。
    调用前需已通过 init_db()/init_sqlite_db()/init_mediacrawler_db() 建立连接。
    """
    utils.init_logging_config()
    utils.logger.info(f"[init_table_schema] begin init db table schema, DB_TYPE={config.DB_TYPE} ...")

    # 使用已有连接，不重复初始化（避免连接泄漏）
    async_db_obj: AbstractAsyncDB = media_crawler_db_var.get()

    # 检查是否已经初始化过表结构（不同数据库使用不同的 check 语句）
    if config.DB_TYPE == "sqlite":
        check_sql = "SELECT name FROM sqlite_master WHERE type='table'"
    else:
        check_sql = "show tables"

    tables = await async_db_obj.query(check_sql)
    if len(tables) > 0:
        utils.logger.info(
            "[init_table_schema] db table schema already init, skip init table schema"
        )
        return

    # 根据数据库类型选择对应的 schema 文件
    if config.DB_TYPE == "sqlite":
        schema_file = "schema/sqlite_tables.sql"
    else:
        schema_file = "schema/tables.sql"

    async with aiofiles.open(schema_file, mode="r", encoding="utf-8") as f:
        schema_sql = await f.read()
        await async_db_obj.execute(schema_sql)
        utils.logger.info(
            "[init_table_schema] db table schema init successful"
        )


async def _standalone_init_table_schema():
    """仅供命令行直接运行 db.py 时使用，先建连接再建表"""
    if config.DB_TYPE == "sqlite":
        await init_sqlite_db()
    else:
        await init_mediacrawler_db()
    await init_table_schema()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(_standalone_init_table_schema())
