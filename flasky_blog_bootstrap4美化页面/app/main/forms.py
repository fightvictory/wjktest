from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    name = StringField('你叫什么名字？', validators=[DataRequired(message='请输入你的名字')])
    submit = SubmitField('提交')