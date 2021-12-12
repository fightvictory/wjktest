from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError, Email
from flask_pagedown.fields import PageDownField
from app.models import Role, User

class NameForm(FlaskForm):
    name = StringField('你叫什么名字？', validators=[DataRequired()])
    submit = SubmitField('提交')

class EditProfileForm(FlaskForm):
    name = StringField('姓名', validators=[Length(0, 64)])
    location = StringField('地址', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')

class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
            '用户名只能是字母、数字、点、下划线')])
    confirmed = BooleanField('已确认')
    role = SelectField('角色', coerce=int)
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('地址', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                            for role in Role.query.order_by(Role.name).all()]
        self.user = user
    
    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email已经注册')
    
    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经占用')

# class PostForm(FlaskForm):
#     title = StringField('标题', validators=[DataRequired()])
#     body = TextAreaField("发表说说", validators=[DataRequired()])
#     submit = SubmitField('提交')

class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    body = PageDownField("发表说说", validators=[DataRequired()])
    submit = SubmitField('提交')

class CommentForm(FlaskForm):
    body = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('提交评论')
