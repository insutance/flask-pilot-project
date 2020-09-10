"""
flaskr/mypage/views.py
"""
from flaskr import app, db
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
from flaskr.models import User, Data
from flaskr.decorator import session_check

"""mypage"""
@app.route('/mypage/<int:page>')
@session_check
def mypage(page):    
    username=session.get('id')
    datas = Data.query.filter_by(user_id=username).all()
    posts = Data.query.filter_by(user_id=username).order_by(Data.stored_time.desc()).paginate(page, 5, error_out=False)
    datas2 = Data.query.filter_by(user_id=username).order_by(Data.stored_time.desc())

    return render_template('mypage.html', datas_length=len(datas), posts=posts, datas=datas2)

"""delete_storedData"""
@app.route('/delete', methods=['POST'])
def delete_storedData():
    if request.method=='POST':
        username=session.get('id')
        json_data = request.get_json()
        data = Data.query.filter_by(news_id=json_data['index']).first()
        db.session.delete(data)
        db.session.commit()

        datas = Data.query.filter_by(user_id=username).order_by(Data.stored_time.desc())
        data_list = []
        for data in datas:
            data_list.append(data.get_json())

        return jsonify(result="success", datas = data_list)
