import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

# g 是一个特殊对象，独立于每一个请求。在处理请求过程中，它可以用于储存可能多个函数都会用到的数据。
# 把连接储存于其中，可以多次使用，而不用在同一个请求中每次调用 get_db 时都创建一个新的连接。
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def execute_sql(sql, choice):
    """
    执行sql语句
    :param sql:
    :param choice: 'select'， 'update', 'insert', 'delete'
    :return:
    """
    my_db = get_db()
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


def get_user_id(**kwargs):
    sql_temp = ""
    for key, value in kwargs:
        sql_temp += f" {key} = '{value}' AND"
    sql_temp = sql_temp[:-3]
    sql = "SELECT id FROM user Where" + sql_temp
    return results


def get_username(user_id: int):
    sql = "SELECT username FROM user WHERE id = %d " % user_id
    results = execute_sql(sql, "select")
    return results


def get_user_info(user_id: int):
    sql = "SELECT * FROM user WHERE id = %d " % user_id
    results = execute_sql(sql, "select")
    return results


def add_user(username: str, phone_number: str, residence: str):
    sql = (
        "INSERT INTO user (username,phone_number,residence) VALUES ('%s','%s','%s')"
        % (username, phone_number, residence)
    )
    execute_sql(sql, "insert")


def remove_user(user_id: int):
    sql = "DELETE FROM user WHERE account = '%s'" % account
    execute_sql(sql, "delete")


def update_user(user_id: int, username: str, phone_number: str, residence: str):
    sql = (
        "UPDATE user SET username = '%s', phone_number = '%s', residence = '%s'  Where id = %d"
        % (username, phone_number, residence, user_id)
    )
    execute_sql(sql, "update")


def get_record(user_id: int):
    sql = "SELECT * FROM record WHERE user_id = %d " % user_id
    results = execute_sql(sql, "select")
    return results
