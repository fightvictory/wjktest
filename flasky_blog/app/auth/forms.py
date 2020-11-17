from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='email格式不合法'), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired('请填写密码')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')