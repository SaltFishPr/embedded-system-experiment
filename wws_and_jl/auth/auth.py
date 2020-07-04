# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: SaltFish
# @file: auth.py
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
    "auth", __name__, url_prefix="/auth", template_folder="templates"
)  #  url_prefix 会添加到所有与该蓝图关联的 URL 前面


@bp.route("/index")
def index():
    return render_template("login.html")


@bp.route("/login", methods=["POST"])
def login():
    password = request.form["password"]
    db = get_db()
    if password == "wws_and_jl":
        session.clear()
        session["user_id"] = "admin"  # 存储cookie
        return redirect(url_for("index"))


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    """
    在其它视图中验证登陆
    """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view