"""
flaskr/index/views.py
"""
from flaskr import app
from flask import Flask, render_template, session

"""index"""
@app.route('/', methods=['GET','POST'])
def index():
    if 'id' in session:
        id = session['id']
        return render_template('index.html', id = id)
    return render_template('index.html')
