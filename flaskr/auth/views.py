"""
flaskr/auth/views.py
"""
from flaskr import app, db
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from flask_bcrypt import Bcrypt
from flaskr.models import User, SearchedData
from flaskr.decorator import session_check
from flaskr.index import views
from .forms import LoginForm, RegisterForm, UpdateForm

bcrypt = Bcrypt(app)

"""register"""
@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method=='POST':
        if form.validate_on_submit():
            pw_hash = bcrypt.generate_password_hash(form.password2.data).decode('utf-8')
            new_user = User(id=form.id.data, password=pw_hash, pub_time=datetime.now())
            db.session.add(new_user)
            db.session.commit()
            flash('회원가입 성공')
            return redirect(url_for('login'))
        
        if form.id.errors:
            flash(form.id.errors[0])
        
        if form.password2.errors:
            flash(form.password2.errors[0])

        return redirect(url_for('register'))

    return render_template('register.html', form=form)

"""login"""
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
        #if form.validate():
            #user = User.query.filter_by(id=form.id.data).first()
            """
            if bcrypt.check_password_hash(user.password, form.password.data) == False:
                flash('비밀번호가 틀립니다.')
                return redirect(url_for('login'))
            """
            session['id'] = form.id.data
            return redirect(url_for('index'))
        
        if form.id.errors:
            flash(form.id.errors[0])
            return redirect(url_for('login'))

        if form.password.errors:
            flash(form.password.errors[0])
            return redirect(url_for('login'))

        """
        if form.id.errors:
            flash(form.id.errors[0])
            return redirect(url_for('login'))
        """
    return render_template('login.html', form = form)

"""logout"""
@app.route('/logout')
@session_check
def logout():
    db.session.query(SearchedData).delete()
    db.session.commit()
    session.pop('id', None)
    return redirect(url_for('index'))

"""user_confrim"""
@app.route('/user/confirm', methods=['GET','POST'])
@session_check
def user_confirm():
    if request.method=='GET':
        return render_template('user_confirm.html')
    else:
        user = session.get('id')
        password = request.form['input_ConfirmPassword']
        data = User.query.filter_by(id=user).first()
        if bcrypt.check_password_hash(data.password, password):
            return redirect(url_for('user_update'))
        else:
            flash("비밀번호가 틀렸습니다.")
            return redirect(url_for('user_confirm'))

"""user_update"""
@app.route('/user/update', methods=['GET','POST'])
@session_check
def user_update():
    form = UpdateForm()
    if request.method=='POST':
        id = session.get('id')
        user = User.query.filter_by(id=id).first()

        if form.validate_on_submit():
            if bcrypt.check_password_hash(user.password, form.password2.data):
                flash("기존의 비밀번호와 동입합니다. 다른 비밀번호를 입력하세요.")
                return redirect(url_for('user_update'))
            
            pw_hash = bcrypt.generate_password_hash(form.password2.data).decode('utf-8')
            user.password = pw_hash
            db.session.commit()
            flash("회원정보가 수정되었습니다. 다시 로그인해주세요.")
            return redirect(url_for('logout'))

        if form.password2.errors:
            flash(form.password2.errors[0])

        return redirect(url_for('user_update'))
    
    return render_template('user_update.html', form=form)