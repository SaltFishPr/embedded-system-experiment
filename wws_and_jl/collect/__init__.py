# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: SaltFish
# @file: __init__.py
# @date: 2020/07/08
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
from wws_and_jl.collect import camera

bp = Blueprint(
    "collect",
    __name__,
    url_prefix="/",
    static_folder="static",
    template_folder="templates",
)


def gen(my_camera):
    """Video streaming generator function."""
    while True:
        frame = my_camera.get_frame()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@bp.route("/video_feed")
@login_required
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    # my_camera = camera.Camera()
    my_camera = camera.CameraTest()
    return Response(
        gen(my_camera), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@bp.route("/main.html")
@login_required
def main_page():
    return render_template("main.html")
