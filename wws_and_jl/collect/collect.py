# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: SaltFish
# @file: collection.py
# @date: 2020/07/08
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
from auth.auth import login_required
from wws_and_jl.db import get_db
from camera import Camera

bp = Blueprint(
    "collect", __name__, url_prefix="/", template_folder="templates"
)  #  url_prefix 会添加到所有与该蓝图关联的 URL 前面


@bp.route("/stream")
@login_required
def stream():
    """Video streaming home page."""
    return render_template("stream.html")


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@bp.route("/video_feed")
@login_required
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()), mimetype="multipart/x-mixed-replace; boundary=frame")
