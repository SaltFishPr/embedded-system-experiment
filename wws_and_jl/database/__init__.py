# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: SaltFish
# @file: __init__.py
# @date: 2020/07/14
import json
import os

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

bp = Blueprint("data", __name__, url_prefix="/data")
collect_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "collect")
picture_dir = os.path.join(collect_dir, "pictures") + "/"


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
    return results


# @bp.route("/get_user_id", methods=["POST"])  # url: /data/get_user_id
# @login_required
# def get_user_id(**kwargs):
#     sql_temp = ""
#     for key, value in kwargs:
#         sql_temp += f" {key} = '{value}' AND"
#     sql_temp = sql_temp[:-3]
#     sql = "SELECT id FROM user Where" + sql_temp
#     return results
#
#
# @bp.route("/get_username", methods=["POST"])
# @login_required
# def get_username(user_id: int):
#     sql = "SELECT username FROM user WHERE id = %d " % user_id
#     results = execute_sql(sql, "select")
#     return results
#
#
# @bp.route("/get_user_info", methods=["POST"])
# @login_required
# def get_user_info(user_id: int):
#     sql = "SELECT * FROM user WHERE id = %d " % user_id
#     results = execute_sql(sql, "select")
#     return results
#
#
# @bp.route("/add_user", methods=["POST"])
# @login_required
# def add_user(username: str, phone_number: str, residence: str):
#     sql = (
#         "INSERT INTO user (username,phone_number,residence) VALUES ('%s','%s','%s')"
#         % (username, phone_number, residence)
#     )
#     execute_sql(sql, "insert")
#
#
# @bp.route("/remove_user", methods=["POST"])
# @login_required
# def remove_user(user_id: int):
#     sql = "DELETE FROM user WHERE account = '%s'" % account
#     execute_sql(sql, "delete")
#
#
# @bp.route("/update_user", methods=["POST"])
# @login_required
# def update_user(user_id: int, username: str, phone_number: str, residence: str):
#     sql = (
#         "UPDATE user SET username = '%s', phone_number = '%s', residence = '%s'  Where id = %d"
#         % (username, phone_number, residence, user_id)
#     )
#     execute_sql(sql, "update")
#
#
# @bp.route("/get_record", methods=["POST"])
# @login_required
# def get_record(user_id: int):
#     sql = "SELECT * FROM record WHERE user_id = %d " % user_id
#     results = execute_sql(sql, "select")
#     return results


@bp.route("/get_user_list", methods=["POST"])
@login_required
def get_user_list():
    sql = "SELECT * FROM user"
    results = execute_sql(sql, "select")

    user_list = []
    i = 0
    for result in results:
        user_list.append(
            {"user_name": result[1], "user_tel": result[2], "user_address": result[3], }
        )
    return {"user_list": user_list}


@bp.route("/add_user", methods=["POST"])
@login_required
def add_user():
    name = request.form["user_name"]
    tel = request.form["user_tel"]
    address = request.form["user_address"]
    sql = "SELECT * FROM user WHERE username = '%s'" % name
    results = execute_sql(sql, "select")
    if results != []:
        return {"flag": 1}

    pic = request.files["user_img"]
    pic.save(picture_dir + name + ".jpeg")
    sql = (
            "INSERT INTO user (username,phone_number,residence) VALUES ('%s','%s','%s')"
            % (name, tel, address)
    )
    execute_sql(sql, "insert")
    return {"flag": 0}


@bp.route("/update_user", methods=["POST"])
@login_required
def update_user():
    raw_name = request.form["raw_user_name"]
    name = request.form["user_name"]
    tel = request.form["user_tel"]
    address = request.form["user_address"]
    pic = request.form["file_flag"]
    if name != "":
        sql = "SELECT * FROM user WHERE username = '%s'" % name
        results = execute_sql(sql, "select")
        if results != []:
            return {"flag": 1}

    if pic != "":
        pic = request.files["user_img"]
        pic.save(picture_dir + raw_name + ".jpeg")
    if address != "":
        sql = "UPDATE user SET residence = '%s' WHERE username = '%s'" % (
            address,
            raw_name,
        )
        execute_sql(sql, "update")
    if tel != "":
        sql = "UPDATE user SET phone_number = '%s' WHERE username = '%s'" % (
            tel,
            raw_name,
        )
        execute_sql(sql, "update")
    if name != "":
        sql = "UPDATE user SET username = '%s' WHERE username = '%s'" % (name, raw_name)
        execute_sql(sql, "update")
        os.rename(
            picture_dir + raw_name + ".jpeg", picture_dir + name + ".jpeg",
        )
    return {"flag": 0}


@bp.route("/delete_user", methods=["POST"])
@login_required
def delete_user():
    name = request.form["user_name"]
    sql = "DELETE FROM user WHERE username = '%s'" % name
    execute_sql(sql, "update")
    os.remove(picture_dir + name + ".jpeg")
    return {"flag": 0}


# 请求返回照片 url为/data/picture/<username>，其中username作为变量
@bp.route("/picture/<username>")
@login_required
def get_user_picture(username: str):
    image = open(picture_dir + username + ".jpeg", "rb")
    return Response(image, mimetype="image/jpeg")
