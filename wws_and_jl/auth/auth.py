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


@bp.route('/')
@bp.route("/login.html")
def login_page():
    return render_template("login.html")

@bp.route("/login", methods=["POST"])
def login():
    admin_confirm = request.form["admin_confirm"]
    print(admin_confirm)
    data = {
        'flag' : 0  # 0成功，其他失败
    }
    return data

@bp.route("/main.html")
def main_page():
    return render_template("main.html")



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
