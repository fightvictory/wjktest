from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    email = StringField('', render_kw={'placeholder': '请输入你的email'}, validators=[DataRequired(message='email格式不合法'), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired('请填写密码')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),Email()])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户必须是字母开头，可以包含数字、. 、下划线')])
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')]) 
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')