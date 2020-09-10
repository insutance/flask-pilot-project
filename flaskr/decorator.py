"""
decorator.py
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps         # decorator 사용하기위해 import

"""Decoraotr"""
def session_check(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'id' in session:
            return func(*args, **kwargs)
        else:
            flash("로그인을 먼저 해주세요")
            return redirect(url_for('login'))
    return wrap