# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: SaltFish
# @file: control.py
# @date: 2020/07/15
import os
import sqlite3
import time


database_dir = os.path.join(os.getcwd(), "instance", "database.sqlite")


def execute_sql(sql, choice):
    """
    执行sql语句
    :param sql:
    :param choice: 'select'， 'update', 'insert', 'delete'
    :return:
    """
    my_db = sqlite3.connect(database_dir)
    my_cursor = my_db.cursor()
    my_cursor.execute(sql)
    results = []
    if choice == "select":
        results = my_cursor.fetchall()
    else:
        my_db.commit()
    my_cursor.close()
    my_db.close()
    return results


def add_record(name):
    sql = "INSERT INTO record (username, create_time) VALUES ('%s','%s')" % (
        name,
        int(time.time()),
    )
    execute_sql(sql, "insert")
