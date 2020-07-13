# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: SaltFish
# @file: test.py
# @date: 2020/07/13
import os

if __name__ == "__main__":
    picture_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pictures")
    for picture in os.listdir(picture_dir):
        print(os.path.splitext(picture))
