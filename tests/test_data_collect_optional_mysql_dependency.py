from __future__ import annotations


def test_json_crawler_support_modules_import_without_mysql_driver():
    import data_collect.crawler.async_db as async_db
    import data_collect.crawler.db as db
    import data_collect.crawler.var as var

    assert async_db.AbstractAsyncDB is not None
    assert db.init_db is not None
    assert var.media_crawler_db_var is not None
