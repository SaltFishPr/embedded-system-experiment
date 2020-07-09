# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: SaltFish
# @file: __init__.py
# @date: 2020/07/02
import os
from flask import Flask, redirect, url_for
from wws_and_jl.auth import auth
from wws_and_jl.collect import collect
from . import db

print(os.getcwd())


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "database.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化数据库
    db.init_app(app)
    # 注册蓝图
    app.register_blueprint(auth.bp)
    app.register_blueprint(collect.bp)

    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, wws_and_jl!"

    @app.route("/")
    def index():
        return redirect("/auth/login.html")

    # 关联端点名称 'index' 和 URL "/"
    # 这样 url_for('index') 或 url_for('***.index') 都会有效
    # 会生成同样的 URL "/"
    app.add_url_rule("/", endpoint="index")

    return app
