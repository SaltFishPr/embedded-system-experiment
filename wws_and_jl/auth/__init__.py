# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: SaltFish
# @file: __init__.py
# @date: 2020/07/04
import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from wws_and_jl.db import get_db

bp = Blueprint(
    "auth",  # 创建蓝图的名称
    __name__,  # 蓝图需要知道是在哪里定义的，因此把 __name__ 作为函数的第二个参数
    url_prefix="/auth",  # url_prefix 会添加到所有与该蓝图关联的 URL 前面
    static_folder="static",  # 静态文件目录（相对路径）
    template_folder="templates",  # 模板目录（相对路径）
)


@bp.route("/login.html")
def login_page():
    return render_template("login.html")


@bp.route("/login", methods=["POST"])
def login():
    admin_confirm = request.form["admin_confirm"]
    db = get_db()
    if admin_confirm == "wws_and_jl":
        session.clear()
        session["user_id"] = "admin"  # 存储cookie
        return {"flag": 0}
    else:
        return {"flag": 1}


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = "admin"


def login_required(view):
    """
    在其它视图中验证登陆
    """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect("/auth/login.html")
        return view(**kwargs)

    return wrapped_view
