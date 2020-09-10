"""
flaskr/auth/forms.py
"""
from flask_wtf import FlaskForm
from wtforms import Form, TextField, PasswordField, SubmitField, validators
from wtforms.validators import EqualTo, Required, ValidationError
from flaskr import db,app
from flaskr.models import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
"""LoginForm"""
class LoginForm(FlaskForm):
    id = TextField('아이디', validators=[Required()])
    password = PasswordField('비밀번호', validators=[Required()])
    submit = SubmitField("로그인")

    def validate_id(self, id):
        user = User.query.filter_by(id=id.data).first()
        if user is None:
            raise ValidationError('아이디가 존재하지 않습니다.')
    
    def validate_password(self, password):
        user = User.query.filter_by(id=self.id.data).first()
        if user is None:
            raise ValidationError('아이디가 존재하지 않습니다.')

        if bcrypt.check_password_hash(user.password, password.data) == False:
            raise ValidationError('비밀번호가 틀립니다.')
        
"""RegisterForm"""
class RegisterForm(FlaskForm):
    id = TextField('아이디', validators=[Required()])
    password1 = PasswordField('비밀번호1', validators=[Required()])
    password2 = PasswordField('비밀번호2', validators=[Required(), EqualTo("password1", message="비밀번호 두개가 다릅니다.")])
    submit = SubmitField("회원가입")

    def validate_id(self, id):
        user = User.query.filter_by(id=id.data).first()
        if user is not None:
            raise ValidationError('아이디가 이미 존재합니다')

"""UpdateForm"""
class UpdateForm(FlaskForm):
    password1 = PasswordField('비밀번호1', validators=[Required()])
    password2 = PasswordField('비밀번호2', validators=[Required(), EqualTo("password1", message="비밀번호 두개가 다릅니다.")])
    submit = SubmitField("변경하기")