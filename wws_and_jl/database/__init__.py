# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: SaltFish
# @file: __init__.py
# @date: 2020/07/14
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    Response,
)
from werkzeug.security import check_password_hash, generate_password_hash
from wws_and_jl.auth import login_required
from wws_and_jl.db import get_db

bp = Blueprint("database", __name__, url_prefix="/data")


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


@bp.route("/get_user_id", methods=["POST"])  # url: /data/get_user_id
@login_required
def get_user_id(**kwargs):
    sql_temp = ""
    for key, value in kwargs:
        sql_temp += f" {key} = '{value}' AND"
    sql_temp = sql_temp[:-3]
    sql = "SELECT id FROM user Where" + sql_temp
    return results


@bp.route("/get_username", methods=["POST"])
@login_required
def get_username(user_id: int):
    sql = "SELECT username FROM user WHERE id = %d " % user_id
    results = execute_sql(sql, "select")
    return results


@bp.route("/get_user_info", methods=["POST"])
@login_required
def get_user_info(user_id: int):
    sql = "SELECT * FROM user WHERE id = %d " % user_id
    results = execute_sql(sql, "select")
    return results


@bp.route("/add_user", methods=["POST"])
@login_required
def add_user(username: str, phone_number: str, residence: str):
    sql = (
        "INSERT INTO user (username,phone_number,residence) VALUES ('%s','%s','%s')"
        % (username, phone_number, residence)
    )
    execute_sql(sql, "insert")


@bp.route("/remove_user", methods=["POST"])
@login_required
def remove_user(user_id: int):
    sql = "DELETE FROM user WHERE account = '%s'" % account
    execute_sql(sql, "delete")


@bp.route("/update_user", methods=["POST"])
@login_required
def update_user(user_id: int, username: str, phone_number: str, residence: str):
    sql = (
        "UPDATE user SET username = '%s', phone_number = '%s', residence = '%s'  Where id = %d"
        % (username, phone_number, residence, user_id)
    )
    execute_sql(sql, "update")


@bp.route("/get_record", methods=["POST"])
@login_required
def get_record(user_id: int):
    sql = "SELECT * FROM record WHERE user_id = %d " % user_id
    results = execute_sql(sql, "select")
    return results